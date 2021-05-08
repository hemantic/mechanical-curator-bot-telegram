from django.core.management.base import BaseCommand
from django.conf import settings

from telegrambot.telegrambot import get_updater


class Command(BaseCommand):
    help = "Set webhooks for telegram API"
    can_import_settings = True

    def handle(self, *args, **options):
        updater = get_updater()

        updater.bot.delete_webhook()

        updater.bot.set_webhook(url=settings.BACKEND_URL + '/' + settings.TELEGRAM_BOT_TOKEN)
