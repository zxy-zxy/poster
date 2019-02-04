import vk_api
from vk_api.exceptions import VkApiError

from social.providers.base import AbstractSocial, SocialException


class VkSocial(AbstractSocial):
    def __init__(self, vk_login, vk_app_id, vk_token):

        self.vk_session = vk_api.VkApi(login=vk_login, app_id=vk_app_id, token=vk_token)

        self.vk_api = self.vk_session.get_api()

        self.vk_upload_api = vk_api.VkUpload(self.vk_session)

    def post_with_image_in_social_media(self, album_id, group_id, text, image_path):
        try:
            photo = self.vk_upload_api.photo(
                image_path, album_id=album_id, group_id=group_id
            )
        except VkApiError as e:
            raise SocialException(
                f"An error has occurred during posting photo to vk album: {e}"
            )

        try:
            photo_id = photo[0]["id"]
            photo_path = "photo-{}_{}".format(group_id, photo_id)
            self.vk_api.wall.post(
                owner_id=f"-{group_id}", message=text, attachments=[photo_path]
            )
        except VkApiError as e:
            raise SocialException(
                f"An error has occurred during posting post with photo to vk: {e}"
            )
