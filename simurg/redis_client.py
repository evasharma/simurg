import redis
import os


def get_redis_client():
    return redis.StrictRedis(
        host=os.environ['DB_PORT_6379_TCP_ADDR'],
        port=os.environ['DB_PORT_6379_TCP_PORT'],
        db=0)
