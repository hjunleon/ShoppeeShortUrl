from typing import Optional, Tuple


class UrlsTabAccessor:

    def create(self, short_key: str, url: str) -> int:
        raise NotImplementedError

    def find_last_by_short_key(self, short_key: str) -> Optional[str]:
        raise NotImplementedError

    def find_match_by_url(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        raise NotImplementedError
