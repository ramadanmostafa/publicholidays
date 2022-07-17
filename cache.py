import json
from datetime import datetime
from redis import StrictRedis


# settings
REDIS_URL = 'redis://redis:6379'
LAST_UPDATED_AT_KEY_POSTFIX = '_last_updated_at'
DEFAULT_CACHE_IN_SECONDS = 86400  # 1 day


redis_conn = StrictRedis.from_url(REDIS_URL)


def get_data_from_cache(key):
    data = redis_conn.get(key)
    if data:
        return json.loads(data)


def save_data_to_cache(key, data, expire_in_sec=DEFAULT_CACHE_IN_SECONDS):
    redis_conn.set(key, json.dumps(data), ex=expire_in_sec)
    redis_conn.set(key + LAST_UPDATED_AT_KEY_POSTFIX, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ex=expire_in_sec)


def invalidate_cache_for_key(key):
    redis_conn.delete(key)
    redis_conn.delete(key + LAST_UPDATED_AT_KEY_POSTFIX)
