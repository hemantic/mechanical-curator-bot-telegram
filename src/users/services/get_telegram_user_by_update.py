from users.models import TelegramUser, User


class GetTelegramUserByUpdate:
    def __init__(self, update):
        self.update = update
        self.message = (
            self.update.message
            if self.update.message
            else self.update.callback_query.message
        )

    def __call__(self):
        full_name = self.get_full_name()

        try:
            telegram_user_instance = TelegramUser.objects.get(
                chat_id=self.message.chat.id
            )
        except TelegramUser.DoesNotExist:
            user_instance = User.objects.create_user(username=self.get_username())

            telegram_user_instance, created = TelegramUser.objects.get_or_create(
                chat_id=self.message.chat.id,
                defaults={
                    "chat_id": self.message.chat.id,
                    "user_name": self.message.chat.username,
                    "full_name": full_name,
                    "curator_user": user_instance,
                },
            )

        return telegram_user_instance

    def get_username(self):
        return f"telegram_{self.message.chat.id}"

    def get_full_name(self):
        full_name = ""

        if self.message.chat.first_name:
            full_name += self.message.chat.first_name
        if self.message.from_user.last_name:
            full_name += " " + self.message.chat.last_name

        return full_name
