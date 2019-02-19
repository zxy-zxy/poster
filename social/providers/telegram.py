import telegram
from telegram.error import TelegramError

from social.providers.base import SocialException, AbstractSocialService


class TelegramService(AbstractSocialService):
    def __init__(self, telegram_token):
        try:
            self.bot = telegram.Bot(token=telegram_token)
        except TelegramError as e:
            raise SocialException(
                f'An error has occurred during connection to telegram: {e}'
            )

    def post_with_image_in_social_media(
        self, text, image_path, telegram_chat_id, **ignored
    ):
        try:
            self.bot.send_message(chat_id=telegram_chat_id, text=text)
        except TelegramError as e:
            raise SocialException(f'An error has occurred during sending message: {e}')

        try:
            self.bot.send_photo(chat_id=telegram_chat_id, photo=open(image_path, 'rb'))
        except TelegramError as e:
            raise SocialException(
                f'An error has occurred during attaching the photo: {e}'
            )


class TelegramServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, telegram_token, **ignored):
        if not self._instance:
            self._instance = TelegramService(telegram_token)
        return self._instance
