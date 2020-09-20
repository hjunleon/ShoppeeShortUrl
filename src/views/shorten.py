from flask import request

from common.exceptions import ShortUrlException
from conf import Conf
from managers import ShortUrlManager, NotFoundException
from utils.validators import is_valid_url


class ShortUrlsView:
    _SITE = Conf['app']['site']

    def __init__(self, short_url_manager: ShortUrlManager):
        self.short_url_manager = short_url_manager

    def create_short_url(self):
        data = request.get_json()
        url = data.get('url', None)
        if not is_valid_url(url):
            raise ShortUrlException('invalid source url')

        short_key = self.short_url_manager.create(url)
        short_url = self._build_url(short_key)

        return {'short_url': short_url}

    def get_short_url(self, short_key):
        try:
            url = self.short_url_manager.resolve(short_key)
            return {'url': url}
        except NotFoundException as e:
            return {'error': e.message}, 404

    def _build_url(self, short_key: str) -> str:
        return f'{self._SITE}/{short_key}'
