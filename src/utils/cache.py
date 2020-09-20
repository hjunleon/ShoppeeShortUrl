from utils.redis import redis_client


class RedisCache:
    _SPACE = 'short'
    SEP = ':'

    def __init__(self, space):
        self.space = space

    @property
    def cache(self):
        return redis_client()

    def set(self, k: str, v: str, nx: bool = False):
        self.cache.set(self._wrap(k), v, nx=nx)

    def get(self, k: str) -> str:
        return self.cache.get(self._wrap(k))

    def _wrap(self, k: str) -> str:
        return self.SEP.join([self._SPACE, self.space, k])
