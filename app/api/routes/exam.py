from fastapi import APIRouter, Depends
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.exam import Exam, Question, Option, UserAnswer, ExamAttempt

from app.core.database import get_db
from app.api.deps.user import get_user
from app.schemas.exam import ExamCreateRequest, ExamResponse 


exam_router = APIRouter(
	prefix="/exams",
	tags=['Exam'],
	)


@exam_router.get("/")
async def greetings(user: User = Depends(get_user)):
	return {"message": "Hello Examination"}

@exam_router.post("/", response_model=ExamResponse)
async def create_exam(data: ExamCreateRequest, db:Session=Depends(get_db), user:User=Depends(get_user)):
	exam = Exam(
		id = uuid4(),
		duration_minutes=data.duration_minutes,
		maximum_marks=data.maximum_marks,
		created_at = datetime.utcnow(),
		updated_at = datetime.utcnow(),
		# questions=data.questions
	)
	return exam 

