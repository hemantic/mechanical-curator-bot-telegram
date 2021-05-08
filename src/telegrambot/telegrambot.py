import logging
from datetime import datetime, timedelta

from django.conf import settings
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from adapters.fatsecret.services import AuthService as FatsecretAuthService
from adapters.fatsecret.services import CalculationService, FatsecretAuthException
from users.models import FatsecretUser
from users.services import GetTelegramUserByUpdate

logger = logging.getLogger("telegrambot")

logger.setLevel(logging.INFO)


def start(update: Update, context: CallbackContext):
    telegram_user = GetTelegramUserByUpdate(update=update)()

    context.bot.sendMessage(update.message.chat_id, text="Hi!")


def help(update: Update, context: CallbackContext):
    telegram_user = GetTelegramUserByUpdate(update=update)()

    context.bot.sendMessage(update.message.chat_id, text="Help!")


def check(update: Update, context: CallbackContext):
    telegram_user = GetTelegramUserByUpdate(update=update)()

    try:
        fatsecret_user = telegram_user.curator_user.fatsecret_user
    except FatsecretUser.DoesNotExist:
        fs_auth_link = "https://fatsecret.com"

        return context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Похоже, что ты еще не привязал свой Fatsecret аккаунт. Давай сделаем это сейчас. Перейди по ссылке {fs_auth_link}, авторизуйся и пришли в ответ на это сообщение код авторизации.",
        )

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=update.message.text,
    )


def fs_info(update: Update, context: CallbackContext):
    telegram_user = GetTelegramUserByUpdate(update=update)()

    try:
        fs = FatsecretAuthService(
            curator_user=telegram_user.curator_user, update=update
        )()

        profile_info = fs.profile_get()

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=profile_info,
        )
    except FatsecretAuthException as e:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=str(e),
        )
    except Exception as e:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Произошла какая-то ошибка ({str(e)})",
        )


def today(update: Update, context: CallbackContext):
    telegram_user = GetTelegramUserByUpdate(update=update)()

    try:
        fs = FatsecretAuthService(
            curator_user=telegram_user.curator_user, update=update
        )()

        today_info = CalculationService(fs)()

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=today_info,
        )

    except Exception as e:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Произошла какая-то ошибка ({str(e)})",
        )


def yesterday(update: Update, context: CallbackContext):
    telegram_user = GetTelegramUserByUpdate(update=update)()

    try:
        fs = FatsecretAuthService(
            curator_user=telegram_user.curator_user, update=update
        )()

        today_info = CalculationService(fs, day=datetime.now() - timedelta(days=1))()

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=today_info,
        )

    except Exception as e:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Произошла какая-то ошибка ({str(e)})",
        )


def error(update: Update, context: CallbackContext, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def set_handlers(dp):
    logger.info("Loading handlers for telegram bot")

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("fs_info", fs_info))

    dp.add_handler(CommandHandler("today", today))
    dp.add_handler(CommandHandler("yesterday", yesterday))

    dp.add_handler(MessageHandler(Filters.text, check))

    dp.add_error_handler(error)

    return dp


def get_updater():
    updater = Updater(token=settings.TELEGRAM_BOT_TOKEN, use_context=True)

    set_handlers(updater.dispatcher)

    return updater
