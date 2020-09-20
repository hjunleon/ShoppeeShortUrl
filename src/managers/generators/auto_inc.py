import random

from managers.generators import UniqueShortKeyGenerator
from utils import base62
from utils.redis import redis_client


class AutoIncShortKeyGenerator(UniqueShortKeyGenerator):
    KEY = 'shortkey:gen:autoinc'
    MAX_STEP = 1000

    DEFAULT_INIT = 1599647941

    def __init__(self, init_value=DEFAULT_INIT, random_step=0):
        redis = redis_client()
        redis.setnx(self.KEY, init_value)
        self.random_step = min(max(1, random_step), self.MAX_STEP)
        self._init_value = init_value

    def generate(self, url) -> str:
        redis = redis_client()
        step = 1 if self.random_step <= 1 else random.randint(1, self.random_step)
        uid = redis.incr(self.KEY, step)
        return base62.encode(uid)
