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


def post_with_image_in_social_media(provider, text, image_path, **kwargs):
    if provider == 'telegram':
        telegram_post_with_image(text, image_path, **kwargs)
    elif provider == 'vk':
        vk_post_with_image(text, image_path, **kwargs)
    elif provider == 'facebook':
        facebook_post_with_image(text, image_path, **kwargs)
    else:
        raise SocialException('Social platform has not been implemented yet!')


def telegram_post_with_image(
    text, image_path, telegram_token, telegram_chat_id, **kwargs
):
    try:
        bot = telegram.Bot(token=telegram_token)
    except TelegramError as e:
        raise SocialException(
            f'An error has occurred during connection to telegram: {e}'
        )

    try:
        bot.send_message(chat_id=telegram_chat_id, text=text)
    except TelegramError as e:
        raise SocialException(f'An error has occurred during sending message: {e}')

    try:
        bot.send_photo(chat_id=telegram_chat_id, photo=open(image_path, 'rb'))
    except TelegramError as e:
        raise SocialException(f'An error has occurred during attaching the photo: {e}')


def vk_post_with_image(
    text, image_path, vk_login, vk_app_id, vk_token, vk_album_id, vk_group_id, **kwargs
):
    _vk_session = vk_api.VkApi(login=vk_login, app_id=vk_app_id, token=vk_token)
    _vk_api = _vk_session.get_api()
    _vk_upload_api = vk_api.VkUpload(_vk_session)

    try:
        photo = _vk_upload_api.photo(
            image_path, album_id=vk_album_id, group_id=vk_group_id
        )
    except VkApiError as e:
        raise SocialException(
            f'An error has occurred during posting photo to vk album: {e}'
        )

    try:
        photo_id = photo[0]['id']
        photo_path = 'photo-{}_{}'.format(vk_group_id, photo_id)
        _vk_api.wall.post(
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
