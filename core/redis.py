import aioredis
from fakeredis.aioredis import FakeRedis

from core.config import REDIS_DB, REDIS_HOST, REDIS_PORT, TESTING

redis_connection = FakeRedis() if TESTING else \
    aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}").client()
