from django.core.management.base import BaseCommand

from telegrambot.telegrambot import get_updater


class Command(BaseCommand):
    help = "Run telegram bot in polling mode"
    can_import_settings = True

    def handle(self, *args, **options):
        updater = get_updater()

        updater.start_polling()
