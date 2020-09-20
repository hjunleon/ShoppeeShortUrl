"""
snowflake id generator

copied from:
https://github.com/twitter-archive/snowflake/blob/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala\
"""
import atexit
import threading
import time

import redis_lock

from utils.redis import redis_client


class SnowflakeClient:
    WORKER_ID_BITS = 5
    DATA_CENTER_ID_BITS = 0
    SEQUENCE_BITS = 9

    WORKER_SHIFT_BITS = SEQUENCE_BITS
    DATA_CENTER_SHIFT_BITS = WORKER_ID_BITS + SEQUENCE_BITS
    TIMESTAMP_SHIFT_BITS = DATA_CENTER_ID_BITS + WORKER_ID_BITS + SEQUENCE_BITS

    SEQUENCE_MASK = (1 << SEQUENCE_BITS) - 1

    TWEPOCH = 1599636698000

    def __init__(self, data_center_id: int, worker_id: int):
        self._lock = threading.Lock()
        self._last_timestamp = -1
        self._sequence = 0
        self.data_center_id = data_center_id
        self.worker_id = worker_id
        self._worker_uid = (
                (self.data_center_id << self.DATA_CENTER_SHIFT_BITS) |
                (self.worker_id << self.WORKER_SHIFT_BITS)
        )
        self._worker_lock = redis_lock.Lock(redis_client(), self.worker_identity)
        self.register()

    @property
    def worker_identity(self):
        return f'snowflake-{self.data_center_id}-{self.worker_id}'

    def unregister(self):
        try:
            self._worker_lock.release()
        except:
            pass

    def register(self):
        atexit.register(self.unregister)
        self._worker_lock.acquire(blocking=False)

    def next_id(self) -> int:
        with self._lock:
            timestamp = self._timestamp()
            if timestamp < self._last_timestamp:
                raise Exception(
                    'Clock moved backwards, refuse to generate id for %s ms' % (timestamp - self._last_timestamp)
                )
            elif timestamp == self._last_timestamp:
                self._sequence = (self._sequence + 1) & self.SEQUENCE_MASK
                if self._sequence == 0:
                    timestamp = self._til_next_millis(self._last_timestamp)
                else:
                    self._sequence = 0
            else:
                self._sequence = 0

            self._last_timestamp = timestamp

            return ((timestamp - self.TWEPOCH) << self.TIMESTAMP_SHIFT_BITS) | self._worker_uid | self._sequence

    @classmethod
    def _timestamp(cls) -> int:
        return int(1000 * time.time())

    @classmethod
    def _til_next_millis(cls, lts) -> int:
        ts = cls._timestamp()
        while ts <= lts:
            ts = cls._timestamp()
        return ts
