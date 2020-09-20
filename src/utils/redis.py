import redis

from conf import Conf

redis_connection_pool = redis.ConnectionPool(**Conf['redis'])


def redis_client():
    return redis.StrictRedis(connection_pool=redis_connection_pool)
