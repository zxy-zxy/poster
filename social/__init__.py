from social.providers.telegram import TelegramServiceBuilder
from social.providers.vk import VKServiceBuilder
from social.providers.facebook import FacebookServiceBuilder


class SocialPlatformObjectFactory:
    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        return builder(**kwargs)


social_platform_object_factory = SocialPlatformObjectFactory()
social_platform_object_factory.register_builder('telegram', TelegramServiceBuilder())
social_platform_object_factory.register_builder('vk', VKServiceBuilder())
social_platform_object_factory.register_builder('facebook', FacebookServiceBuilder())
