from aioredis import Redis, from_url

from decouple import config

from typing import Optional


class RedisCache:

    def __init__(self):
        self.redis_cache: Optional[Redis] = None

    async def init_cache(self):
        # self.redis_cache = await create_redis_pool(config('REDIS_URL'))
        self.redis_cache = from_url("redis://localhost")

    async def keys(self, pattern):
        return await self.redis_cache.keys(pattern)

    async def set(self, key, value, ex=None):
        return await self.redis_cache.set(key, value, ex=ex)

    async def get(self, key):
        raw = await self.redis_cache.get(key)
        if not raw:
            return
        # redis return bytes object, change this to clear data
        return raw.decode('utf-8')

    async def delete(self, key):
        await self.redis_cache.delete(key)

    async def close(self):
        await self.redis_cache.close()
        await self.redis_cache.wait_closed()


redis_cache = RedisCache()




