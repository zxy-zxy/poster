import requests
from requests import RequestException
import telegram
from telegram.error import TelegramError
import vk_api
from vk_api.exceptions import VkApiError


class SocialException(Exception):
    """
    Base exception for all test classes
    """


def initialize_telegram_bot(telegram_token):
    try:
        bot = telegram.Bot(token=telegram_token)
    except TelegramError as e:
        raise SocialException(
            f'An error has occurred during connection to telegram: {e}'
        )
    return bot


def initialize_vk_api(vk_login, vk_app_id, vk_token):
    _vk_session = vk_api.VkApi(login=vk_login, app_id=vk_app_id, token=vk_token)
    _vk_api = _vk_session.get_api()
    _vk_upload_api = vk_api.VkUpload(_vk_session)
    return _vk_api, _vk_upload_api


def telegram_post_with_image(
        bot, text, image_path, telegram_chat_id, **kwargs
):
    try:
        bot.send_message(chat_id=telegram_chat_id, text=text)
    except TelegramError as e:
        raise SocialException(f'An error has occurred during sending message: {e}')

    try:
        bot.send_photo(chat_id=telegram_chat_id, photo=open(image_path, 'rb'))
    except TelegramError as e:
        raise SocialException(f'An error has occurred during attaching the photo: {e}')


def vk_post_with_image(
        vk_api_, vk_upload_api_, text, image_path, vk_album_id, vk_group_id, **kwargs
):
    try:
        photo = vk_upload_api_.photo(
            image_path, album_id=vk_album_id, group_id=vk_group_id
        )
    except VkApiError as e:
        raise SocialException(
            f'An error has occurred during posting photo to vk album: {e}'
        )

    try:
        photo_id = photo[0]['id']
        photo_path = 'photo-{}_{}'.format(vk_group_id, photo_id)
        vk_api_.wall.post(
            owner_id=f'-{vk_group_id}', message=text, attachments=[photo_path]
        )
    except VkApiError as e:
        raise SocialException(
            f'An error has occurred during posting post with photo to vk: {e}'
        )


def facebook_post_with_image(
        text, image_path, facebook_api_token, facebook_group_id, **kwargs
):
    facebook_page = f'https://graph.facebook.com/v3.2/{facebook_group_id}/photos/'

    files = {'file': open(image_path, 'rb')}
    try:
        response = requests.post(
            facebook_page,
            data={'caption': text, 'access_token': facebook_api_token},
            files=files,
        )
    except RequestException as e:
        raise SocialException(f'An error has occurred during posting to facebook {e}:')

    if not response.ok:
        raise SocialException(
            f'An error has occurred during posting to facebook {response.text}:'
        )
