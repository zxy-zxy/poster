from social.providers.facebook import FacebookSocial
from social.providers.vk import VkSocial
from social.providers.telegram import TelegramSocial


class SocialFactory:
    _social_classes = {
        "facebook": FacebookSocial,
        "vk": VkSocial,
        "telegram": TelegramSocial,
    }

    @staticmethod
    def get_social_platform(name):
        social_class = SocialFactory._social_classes.get(name.lower(), None)

        if social_class is None:
            raise NotImplementedError(
                f"The requested social platform {name} has not been implemented"
            )

        return social_class
