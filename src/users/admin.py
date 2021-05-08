from django.contrib import admin

from users.models import FatsecretUser, TelegramUser, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(FatsecretUser)
class FatsecretUserAdmin(admin.ModelAdmin):
    pass


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass
