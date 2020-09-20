from accessors import UrlsTabAccessor
from common.exceptions import ShortUrlException
from managers.generators import AbstractShortKeyGenerator


class ShortUrlManager:

    def __init__(self, urls_tab_accessor: UrlsTabAccessor, short_key_generator: AbstractShortKeyGenerator):
        self.urls_tab_accessor = urls_tab_accessor
        self.short_key_generator = short_key_generator

    def resolve(self, short_key: str) -> str:
        """
        Return the latest source url for the short key.
        """
        raise NotImplementedError

    def create(self, url: str) -> str:
        """
        Return a short key for the url.
        """
        raise NotImplementedError


class NotFoundException(ShortUrlException):
    pass
