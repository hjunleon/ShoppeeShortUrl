import hashlib
from typing import Optional, Tuple

from sqlalchemy import desc

from accessors import UrlsTabAccessor
from db import session_ctx
from db.tables import UrlsTab
from utils.cache import RedisCache
from utils.time import current_timestamp


class CachedMysqlUrlsTabAccessor(UrlsTabAccessor):
    _NULL = 'null'

    def __init__(self):
        self._short_key_mapping_cache = RedisCache(space='short_key')

    def create(self, short_key: str, url: str) -> int:
        """
        :return: id of the created record
        """
        record = UrlsTab(
            url=url,
            short_key=short_key,
            hashed_url=self._url_hash(url),
            ctime=current_timestamp()
        )
        with session_ctx() as session:
            session.add(record)
        self._short_key_mapping_cache.set(short_key, url)
        return record.id

    def find_last_by_short_key(self, short_key: str) -> Optional[str]:
        url = self._get_from_cache(short_key)

        if url is not None:
            return url

        with session_ctx() as session:
            record = (
                session.query(UrlsTab)
                    .filter(UrlsTab.short_key == short_key)
                    .order_by(desc(UrlsTab.ctime))
                    .first()
            )
            url = record.url if record else None

        self._short_key_mapping_cache.set(short_key, url or self._NULL, nx=True)

        return url

    def _get_from_cache(self, short_key) -> Optional[str]:
        url = self._short_key_mapping_cache.get(short_key)
        if url == self._NULL:
            return None
        return url

    def find_match_by_url(self, url: str) -> Optional[Tuple[str, str]]:
        url_hash = self._url_hash(url)
        with session_ctx() as session:
            records = (
                session.query(UrlsTab)
                .filter(UrlsTab.hashed_url == url_hash)
                .order_by(desc(UrlsTab.ctime))
                .all()
            )
        match = next((record for record in records if record.url == url), None)
        if match is not None:
            return match.short_key, url
        return None, None

    @staticmethod
    def _url_hash(url):
        return bytearray.fromhex(hashlib.sha1(str.encode(url)).hexdigest())
