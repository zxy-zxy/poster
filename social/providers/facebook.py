import requests
from requests.exceptions import RequestException

from social.providers.base import AbstractSocial, SocialException


class FacebookSocial(AbstractSocial):
    def __init__(self, facebook_api_token):
        self.facebook_api_token = facebook_api_token

    def post_with_image_in_social_media(self, group_id, text, image_path):
        facebook_page = f"https://graph.facebook.com/v3.2/{group_id}/photos/"

        files = {"file": open(image_path, "rb")}
        try:
            response = requests.post(
                facebook_page,
                data={"caption": text, "access_token": self.facebook_api_token},
                files=files,
            )
        except RequestException as e:
            raise SocialException(
                f"An error has occurred during posting to facebook {e}:"
            )

        if not response.ok:
            raise SocialException(
                f"An error has occurred during posting to facebook {response.text}:"
            )
