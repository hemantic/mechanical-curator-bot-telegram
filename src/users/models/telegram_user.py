from django.db import models


class TelegramUser(models.Model):
    chat_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(blank=True, max_length=255)
    full_name = models.CharField(blank=True, max_length=255)
    curator_user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="telegram_user"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Telegram bot user"
        verbose_name_plural = "Telegram bot users"

        indexes = [
            models.Index(fields=["user_name"]),
            models.Index(fields=["full_name"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]
