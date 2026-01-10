from fastapi import APIRouter, Depends
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timedelta


from app.models.user import User
from app.models.exam import Exam, Question, Option, Answer, ExamAttempt

from app.core.database import get_db
from app.core.deps import get_user



router = APIRouter(
	prefix="/exams",
	)


@router.get("/")
async def greetings(user: User = Depends(get_user)):
	return {"message": "Hello Examination"}
