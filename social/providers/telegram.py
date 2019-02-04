import telegram
from telegram.error import TelegramError

from social.providers.base import AbstractSocial, SocialException


class TelegramSocial(AbstractSocial):
    def __init__(self, telegram_token):
        try:
            self.bot = telegram.Bot(token=telegram_token)
        except TelegramError as e:
            raise SocialException(
                f"An error has occurred during connection to telegram: {e}"
            )

    def post_with_image_in_social_media(self, chat_id, text, image_path):

        try:
            self.bot.send_message(chat_id=chat_id, text=text)
        except TelegramError as e:
            raise SocialException(f"An error has occurred during sending message: {e}")

        try:
            self.bot.send_photo(chat_id=chat_id, photo=open(image_path, "rb"))
        except TelegramError as e:
            raise SocialException(
                f"An error has occurred during attaching the photo: {e}"
            )
