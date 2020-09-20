from managers import AbstractShortKeyGenerator
import hashlib
import base64
import struct
import random

from managers.generators import UniqueShortKeyGenerator
from utils import base36
from utils.redis import redis_client

def fnv64(data):
    hash_ = 0xcbf29ce484222325
    for b in data:
        hash_ *= 0x100000001b3
        hash_ &= 0xffffffffffffffff
        hash_ ^= b
    return hash_
    
class ShortKeyGenerator(AbstractShortKeyGenerator):
    KEY = 'shortkey:gen:autoinc'
    MAX_STEP = 1000

    DEFAULT_INIT = 1599647941
    cur_int = 0

    def __init__(self, init_value=DEFAULT_INIT, random_step=0):
        redis = redis_client()
        redis.setnx(self.KEY, init_value)
        self.random_step = 0#min(max(1, random_step), self.MAX_STEP)
        self._init_value = init_value

    def generate(self, url) -> str:
        redis = redis_client()
        step = 1 #if self.random_step <= 1 else random.randint(1, self.random_step)
        uid = redis.incr(self.KEY, step)
        #self.cur_int += 1
        return base36.encode(uid)
