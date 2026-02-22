class CacheManager:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str, ttl: int = 300):
        await self.redis.set(key, value, ex=ttl)
    