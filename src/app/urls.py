from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from telegrambot.views import TelegramBotWebhookView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        f"{settings.TELEGRAM_BOT_TOKEN}", csrf_exempt(TelegramBotWebhookView.as_view())
    ),
]
