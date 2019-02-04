import os
import argparse

from dotenv import load_dotenv

from social import SocialFactory
from social.providers.base import SocialException


def create_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", type=str, help="Text to be posted.")
    parser.add_argument("image_path", type=str, help="Image to be posted.")
    return parser


if __name__ == "__main__":
    load_dotenv()

    argument_parser = create_argument_parser()
    args = argument_parser.parse_args()

    image_path = args.image_path
    text = args.text

    VK_LOGIN = os.getenv("VK_LOGIN")
    VK_APP_ID = os.getenv("VK_APP_ID")
    VK_TOKEN = os.getenv("VK_TOKEN")

    VK_ALBUM_ID = os.getenv("VK_ALBUM_ID")
    VK_GROUP_ID = os.getenv("VK_GROUP_ID")

    try:
        vk_social_class = SocialFactory.get_social_platform("vk")
        vk_social = vk_social_class(
            vk_login=VK_LOGIN, vk_app_id=VK_APP_ID, vk_token=VK_TOKEN
        )
        vk_social.post_with_image_in_social_media(
            VK_ALBUM_ID, VK_GROUP_ID, text, image_path
        )
        print("VK post has been successfully created.")
    except (NotImplementedError, SocialException) as e:
        print(f"Cannot post content to vk: {e}")

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    try:
        telegram_social_class = SocialFactory.get_social_platform("telegram")
        telegram_social = telegram_social_class(telegram_token=TELEGRAM_TOKEN)
        telegram_social.post_with_image_in_social_media(
            TELEGRAM_CHAT_ID, text, image_path
        )
        print("Telegram post has been successfully created.")
    except (NotImplementedError, SocialException) as e:
        print(f"Cannot post content to telegram: {e}")

    FACEBOOK_TOKEN = os.getenv("FACEBOOK_TOKEN")
    FACEBOOK_GROUP_ID = os.getenv("FACEBOOK_GROUP_ID")

    try:
        facebook_social_class = SocialFactory.get_social_platform("facebook")
        facebook_social = facebook_social_class(facebook_api_token=FACEBOOK_TOKEN)
        facebook_social.post_with_image_in_social_media(
            FACEBOOK_GROUP_ID, "text", "test.jpg"
        )
        print("Facebook post has been successfully created.")
    except (NotImplementedError, SocialException) as e:
        print(f"Cannot post content to facebook: {e}")
