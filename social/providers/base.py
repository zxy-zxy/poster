from abc import ABCMeta, abstractmethod


class SocialException(Exception):
    """
    Base exception for all social classes
    """

    pass


class AbstractSocial(metaclass=ABCMeta):
    """Base social provider class"""

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """
        Abstract init method
        """
        pass

    @abstractmethod
    def post_with_image_in_social_media(self, *args, **kwargs):
        """
        Abstract posting method
        """
        pass
