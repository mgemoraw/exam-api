from typing import List
from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.exam import Exam, ExamQuestion, Question, Option, UserAnswer, ExamAttempt

from app.core.database import get_db
from app.api.deps.user import get_user, get_current_user
from app.schemas.exam import ExamCreateRequest, ExamResponse 


exam_router = APIRouter(
	prefix="/exams",
	tags=['Exam'],
	)


@exam_router.get("/")
async def greetings(user: User = Depends(get_current_user), db:Session=Depends(get_db)):
	exams = db.query(Exam).all()
     
	return {
			"message": "Hello Examination",
			"data": exams
           }	

@exam_router.post("/", response_model=ExamResponse)
async def create_exam(data: ExamCreateRequest, db:Session=Depends(get_db), user:User=Depends(get_current_user)):
	exam = Exam(
		id = str(uuid4()),
        title = data.title,
		duration_minutes=data.duration_minutes,
		maximum_marks=data.maximum_marks,
		created_at = datetime.utcnow(),
		updated_at = datetime.utcnow(),
		# questions=data.questions
	)
	return exam 

@exam_router.post("/{exam_id}/questions")
async def add_questions_to_exam(exam_id: str, question_ids: List[str], db: Session = Depends(get_db)):
    for q_id in question_ids:
        link = ExamQuestion(exam_id=exam_id, question_id=q_id)
        db.add(link)
    db.commit()
    return {"message": "Questions allocated successfully"}


@exam_router.put("/{exam_id}/visibility")
async def set_exam_visibility(exam_id: str, visible: bool, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    exam.is_visible = visible
    db.commit()
    return {"message": f"Exam visibility set to {visible}"}


@exam_router.put("/{exam_id}/schedule")
async def schedule_exam(exam_id: str, start_time: datetime, end_time: datetime, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    exam.start_time = start_time
    exam.end_time = end_time
    db.commit()
    return {"message": "Exam scheduled successfully"}
@exam_router.get("/available", response_model=List[ExamResponse])
async def get_available_exams(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    exams = db.query(Exam).filter(
        Exam.is_visible == True,
        Exam.start_time <= now,
        Exam.end_time >= now
    ).all()
    return exams