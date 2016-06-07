import logging
import redis
import os


class RedisClient():
    def __init__(self):
        self.redis = redis.StrictRedis(host=os.environ['DB_PORT_6379_TCP_ADDR'],
                                  port=os.environ['DB_PORT_6379_TCP_PORT'],
                                  db=0)

    def insert(self, news):
        key = news['url']
        self.redis.hset(key, 'url', news['url'])
        self.redis.hset(key, 'headline_selector', news['headline_selector'])
        self.redis.hset(key, 'wayback_url', news['wayback_url'])
        logging.info('inserted news with url: {}'.format(news['url']))

    def exists(self, key):
        return self.redis.exists(key)
