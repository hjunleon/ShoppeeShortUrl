from accessors import UrlsTabAccessor
from managers import ShortUrlManager, NotFoundException
from managers.generators import UniqueShortKeyGenerator


class DefaultShortUrlManager(ShortUrlManager):

    def __init__(self, urls_tab_accessor: UrlsTabAccessor, short_key_generator: UniqueShortKeyGenerator):
        super().__init__(urls_tab_accessor, short_key_generator)

    def resolve(self, short_key: str) -> str:
        """
        Return the latest source url for the short key.
        """
        url = self.urls_tab_accessor.find_last_by_short_key(short_key)
        if url is None:
            raise NotFoundException(f'url not found for short_key: {short_key}')
        return url

    def create(self, url: str) -> str:
        """
        Return a short key for the url.
        """
        short_key, matched = self.urls_tab_accessor.find_match_by_url(url)
        if matched == url:
            return short_key

        # just create a new short_key
        return self._generate_new_short_key(url)

    def _generate_new_short_key(self, url):
        short_key = self.short_key_generator.generate(url)
        self.urls_tab_accessor.create(short_key, url)
        return short_key
