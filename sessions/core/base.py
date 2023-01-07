import os
from aioredis import Redis, from_url
# from redis import asyncio as aioredis


from typing import Optional

# TODO перейти на более современную либу?
class RedisCache:

    def __init__(self):
        self.redis_cache: Optional[Redis] = None
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

    async def init_cache(self):
        self.redis_cache = from_url(self.redis_url,  decode_responses=True)

    async def keys(self, pattern):
        return await self.redis_cache.keys(pattern)

    async def hkeys(self, name):
        return await self.redis_cache.hkeys(name)

    async def set(self, key, value, ex=None):
        """set string"""
        return await self.redis_cache.set(key, value, ex=ex)

    async def hset(self, name, key=None, value=None, mapping=None):
        """set dict"""
        return await self.redis_cache.hset(name, key, value, mapping)

    async def hget(self, name, key):
        return await self.redis_cache.hget(name, key)

    async def hgetall(self, key):
        raw = await self.redis_cache.hgetall(key)
        if not raw:
            return
        return raw

    async def get(self, key):
        raw = await self.redis_cache.get(key)
        if not raw:
            return
        # redis return bytes object, change this to clear data
        return raw.decode('utf-8')

    async def expire(self, name, time):
        await self.redis_cache.expire(name, time)

    async def delete(self, key):
        await self.redis_cache.delete(key)

    async def hdel(self, name, key):
        await self.redis_cache.hdel(name, key)

    async def close(self):
        await self.redis_cache.close()
        await self.redis_cache.wait_closed()


redis_cache = RedisCache()




