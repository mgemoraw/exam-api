from app.infrastructure.cache_manager import CacheManager

class ExamService:
    def __init__(self, repo, cache: CacheManager):
        self.repo = repo
        self.cache = cache

    async def get_exam(self, exam_id):
        cache_key = f"exam:{exam_id}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        exam = await self.repo.get_exam(exam_id)
        await self.cache.set(cache_key, exam.json(), ttl=600)
        return exam