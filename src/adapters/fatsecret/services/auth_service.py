from django.conf import settings
from fatsecret import Fatsecret
from telegram import Update

from users.models.fatsecret_user import FatsecretUser
from users.models.user import User


class FatsecretAuthException(Exception):
    pass


class AuthService:
    def __init__(self, curator_user: User, update: Update):
        self.curator_user = curator_user
        self.telegram_update = update

        self.instance = None
        self.fatsecret_user = None

    def __call__(self):
        # Если у пользователя нет ФС, вернуть исключение
        # Если у пользователя нет oAuth ключей, вернуть исключение

        # Если все ок, вернуть инстанс

        self.validate_fatsecret_user()

        return self.auth_user()

    def validate_fatsecret_user(self):
        try:
            self.fatsecret_user = self.curator_user.fatsecret_user
        except FatsecretUser.DoesNotExist as e:
            raise FatsecretAuthException(
                "У тебя еще не настроен пользователь Fatsecret"
            ) from e

    def validate_fatsecret_credentials(self):
        if (
            not self.fatsecret_user.access_token
            and self.fatsecret_user.access_token_secret
        ):
            raise FatsecretAuthException(
                "Не получены ключи авторизации для API Fatsecret"
            )

    def auth_user(self):
        return Fatsecret(
            settings.FATSECRET["consumer_key"],
            settings.FATSECRET["consumer_secret"],
            session_token=(
                self.fatsecret_user.access_token,
                self.fatsecret_user.access_token_secret,
            ),
        )

    def get_fatsecret_user(self):
        return self.curator_user.fatsecret_user

    @property
    def system_fatsecret_instance(self):
        return Fatsecret(
            settings.FATSECRET["consumer_key"], settings.FATSECRET["consumer_secret"]
        )
