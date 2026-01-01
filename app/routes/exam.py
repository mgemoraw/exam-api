from fastapi import APIRouter, Depends
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timedelta


from models.user import User
from models.exam import Exam, Question, Option, Answer, ExamAttempt

# from model import User, Exam, Question, Option, ExamAttempt, AttemptQuestion, Answer
from core.database import get_db
from core.deps import get_user



router = APIRouter(
	prefix="/exams",
	)


@router.get("/")
async def greetings(user: User = Depends(get_user)):
	return {"message": "Hello Examination"}
