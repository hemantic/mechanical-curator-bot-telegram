from django.db import models


class FatsecretUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    curator_user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="fatsecret_user"
    )
    access_token = models.CharField(blank=True, null=True, default=None, max_length=255)
    access_token_secret = models.CharField(
        blank=True, null=True, default=None, max_length=255
    )
    pin = models.IntegerField(blank=True, null=True, default=None)
    authorize_url = models.CharField(blank=True, max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fatsecret user"
        verbose_name_plural = "Fatsecret users"

        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]
