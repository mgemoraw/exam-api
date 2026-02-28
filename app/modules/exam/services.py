from app.infrastructure.cache_manager import CacheManager
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from app.infrastructure.redis import redis_client
from app.infrastructure.cache_utils import serialize, deserialize
from .repository import ExamRepository
from .models import Exam
from .exceptions import ExamNotFoundError, ExamAlreadyExistsError
from .schemas import ExamResponse, ExamCreateRequest
class ExamService:

    CACHE_TTL = 300  # 5 minutes

    def __init__(self, db: Session):
        self.db = db
        self.repo = ExamRepository(db)

    def _cache_key(self, exam_id: uuid.UUID) -> str:
        return f"exam:{exam_id}"
    

    # def __init__(self, repo, cache: CacheManager):
    #     self.repo = repo
    #     self.cache = cache

    # def get_exam(self, exam_id: UUID) -> Exam:
    #     cache_key = self._cache_key(exam_id)

    #     # 1️⃣ Check Redis
    #     cached = redis_client.get(cache_key)
    #     if cached:
    #         return deserialize(cached)

    #     # 2️⃣ Fallback to DB
    #     exam = self.repo.get_by_id(exam_id)
    #     if not exam:
    #         raise ExamNotFoundError()

    #     # 3️⃣ Store in cache
    #     redis_client.setex(
    #         cache_key,
    #         self.CACHE_TTL,
    #         serialize({
    #             "id": str(exam.id),
    #             "title": exam.title,
    #             "total_marks": exam.total_marks,
    #         })
    #     )

    def get_exam(self, exam_id: uuid.UUID) -> ExamResponse:
        cache_key = self._cache_key(exam_id)

        cached = redis_client.get(cache_key)
        if cached:
            return ExamResponse.model_validate_json(cached)

        exam = self.repo.get_by_id(exam_id)
        if not exam:
            raise ExamNotFoundError()

        response = ExamResponse.model_validate(exam)

        redis_client.setex(
            cache_key,
            self.CACHE_TTL,
            response.model_dump_json()
        )

        return response
    
    def delete_exam(self, exam_id: uuid.UUID):
        exam = self.repo.get_by_id(exam_id)
        if not exam:
            raise ExamNotFoundError()

        self.repo.delete(exam)
        self.db.commit()

        redis_client.delete(self._cache_key(exam_id))


    def create_exam(self, exam_data: ExamCreateRequest) -> Exam:
        # 🔹 1. Business validations

        if exam_data.maximum_marks <= 0:
            raise ValueError("Maximum marks must be greater than zero.")

        if exam_data.duration_minutes <= 0:
            raise ValueError("Duration must be greater than zero.")

        if exam_data.start_time and exam_data.end_time:
            if exam_data.end_time <= exam_data.start_time:
                raise ValueError("End time must be after start time.")

        # 🔹 2. Prevent duplicate title (optional but recommended)
        existing = self.repo.get_by_title(exam_data.title)
        if existing:
            raise ExamAlreadyExistsError()


        # 🔹 3. Create Exam entity
        exam = Exam(
            id=uuid.uuid4(),  # if UUID primary key
            title=exam_data.title,
            maximum_marks=exam_data.maximum_marks,
            duration_minutes=exam_data.duration_minutes,
            is_visible=exam_data.is_visible,
            exam_type=exam_data.exam_type,
            description=exam_data.description,
            start_time=exam_data.start_time,
            end_time=exam_data.end_time,
            created_at=datetime.now(timezone.utc),
        )

        try:
            # 🔹 4. Persist
            self.repo.create(exam)
            self.db.commit()
            self.db.refresh(exam)

            return exam
        except Exception as e:
            self.db.rollback()
            raise


    # async def get_exam(self, exam_id):
    #     cache_key = f"exam:{exam_id}"

    #     cached = await self.cache.get(cache_key)
    #     if cached:
    #         return cached

    #     exam = await self.repo.get_exam(exam_id)
    #     await self.cache.set(cache_key, exam.json(), ttl=600)
    #     return exam
    

    