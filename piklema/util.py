import os
from contextlib import contextmanager
import redis


@contextmanager
def create_redis_client(host):
    redis_client = redis.Redis(host=host, port=os.getenv("REDIS_PORT"), db=0)
    yield redis_client
    redis_client.close()
