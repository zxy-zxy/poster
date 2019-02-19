from abc import ABCMeta, abstractmethod


class SocialException(Exception):
    '''
    Base exception for all test classes
    '''

    pass


class AbstractSocialService(metaclass=ABCMeta):
    '''Base test provider class'''

    @abstractmethod
    def __init__(self, *args, **kwargs):
        '''
        Abstract init method
        '''
        pass

    @abstractmethod
    def post_with_image_in_social_media(self, text, image_path, **ignored):
        '''
        Abstract posting method
        '''
        pass
