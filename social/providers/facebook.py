import requests
from requests.exceptions import RequestException

from social.providers.base import AbstractSocialService, SocialException


class FacebookService(AbstractSocialService):
    def __init__(self, facebook_api_token):
        self.facebook_api_token = facebook_api_token

    def post_with_image_in_social_media(
        self, text, image_path, facebook_group_id, **ignored
    ):
        facebook_page = f'https://graph.facebook.com/v3.2/{facebook_group_id}/photos/'

        files = {'file': open(image_path, 'rb')}
        try:
            response = requests.post(
                facebook_page,
                data={'caption': text, 'access_token': self.facebook_api_token},
                files=files,
            )
        except RequestException as e:
            raise SocialException(
                f'An error has occurred during posting to facebook {e}:'
            )

        if not response.ok:
            raise SocialException(
                f'An error has occurred during posting to facebook {response.text}:'
            )


class FacebookServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, facebook_api_token, **ignored):
        if not self._instance:
            self._instance = FacebookService(facebook_api_token)
        return self._instance
