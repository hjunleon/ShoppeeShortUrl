from typing import Optional

from validator_collection import checkers


def is_valid_url(s: Optional[str]) -> bool:
    return checkers.is_url(s, allow_special_ips=True)
