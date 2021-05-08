import json
import logging

from django.http import JsonResponse
from django.views import View
from telegram import Update

from telegrambot.telegrambot import get_updater

logger = logging.getLogger(__name__)


def index(request):
    return JsonResponse({"error": "..."})


class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):
        updater = get_updater()

        updater.dispatcher.process_update(
            Update.de_json(json.loads(request.body), updater.bot)
        )

        return JsonResponse({"ok": "POST request processed"})
