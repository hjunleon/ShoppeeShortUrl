import unittest
from typing import Optional, Tuple

from accessors import UrlsTabAccessor
from managers.default import DefaultShortUrlManager
from managers.generators import AbstractShortKeyGenerator


class MockUrlsTabAccessor(UrlsTabAccessor):

    def __init__(self):
        self.short_key_mapping = {}
        self.url_mapping = {}
        self.counter = 0

    def create(self, short_key: str, url: str) -> int:
        self.short_key_mapping.update({short_key: url})
        self.url_mapping.update({url: short_key})
        self.counter += 1
        return self.counter

    def find_last_by_short_key(self, short_key: str) -> Optional[str]:
        return self.short_key_mapping.get(short_key, None)

    def find_match_by_url(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        short_key = self.url_mapping.get(url, None)
        return (short_key, self.short_key_mapping.get(short_key)) if short_key else (None, None)


class MockShortKeyGenerator(AbstractShortKeyGenerator):
    def __init__(self):
        self.uid = 0

    def generate(self, url) -> str:
        self.uid += 1
        return str(self.uid)


class TestDefaultShortenManager(unittest.TestCase):
    URLS = [
        'http://localhost',
        'http://127.0.0.1/',
        'https://stackoverflow.com/questions/14668348/python-random-url-choice',
        'https://www.google.com/webhp?hl=zh-CN&sa=X&ved=0ahUKEwj0reCtw8zrAhVWfSsKHekFBysQPAgI',
    ]

    def setUp(self) -> None:
        mock_urls_tab_accessor = MockUrlsTabAccessor()
        mock_short_key_generator = MockShortKeyGenerator()
        self.shorten_manager = DefaultShortUrlManager(mock_urls_tab_accessor, mock_short_key_generator)

    def test_shorten_resolve(self):
        for url in self.URLS:
            short_key = self.shorten_manager.create(url)
            resolved = self.shorten_manager.resolve(short_key)
            self.assertEqual(url, resolved)
