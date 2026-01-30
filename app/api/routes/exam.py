import re
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
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
        exam_type=data.exam_type,
        description=data.description,
        maximum_marks=data.maximum_marks,
        is_visible=False,
        start_time=data.start_time,
        end_time=data.end_time,
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow(),
        # questions=data.questions
    )
        
    try:
        db.add(exam)
        db.commit()
        db.refresh(exam)

        return exam 
    except Exception as e:
        db.rollback()
        raise e
        raise HTTPException(status_code=500, detail="Internal server error")



@exam_router.post("/{exam_id}/questions")
async def add_questions_to_exam(exam_id: str, question_ids: List[str], db: Session = Depends(get_db)):
    for q_id in question_ids:
        link = ExamQuestion(exam_id=exam_id, question_id=q_id)
        db.add(link)
    db.commit()
    return {"message": "Questions allocated successfully"}

@exam_router.post("/upload-questions", )
async def import_mcq(file: UploadFile=File(...), db:Session=Depends(get_db)):
    # import a utility function
    from app.core.utils import  parse_text_mcq

    if file.content_type != "text/plain":
        raise HTTPException(
            status_code=400, 
            detail="Only .text files allowed",
        )
    
    text = (await file.read()).decode('utf-8')
    blocks = text.strip().split('\r\n\r\n')
    questions =  parse_text_mcq(blocks)
    

    # return {
    #     'count': len(questions),
    #     'questions': questions,
    # } 
    return questions


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
async def get_available_exams(start_time: datetime = None, end_time:datetime=None, db: Session = Depends(get_db)):
    now = datetime.utcnow()
    
    if start_time is not None and end_time is not None:

        exams = db.query(Exam).filter(
            Exam.is_visible == True,
            Exam.start_time <= start_time,
            Exam.end_time >= end_time
        ).all()

    if start_time is not None:
        exams = db.query(Exam).filter(
            Exam.is_visible == True,
            Exam.start_time <= start_time,
        ).all()
    
    if end_time is not None:
        exams = db.query(Exam).filter(
            Exam.is_visible == True,
            Exam.end_time <= end_time,
        ).all()

    if start_time is None and end_time is None:
        exams = db.query(Exam).filter(
                Exam.is_visible == True,
            ).all()
    
    return exams



@exam_router.post("/{exam_id}/attempts")
async def start_exam_attempt(exam_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    # Check if user has already started an attempt
    existing_attempt = db.query(ExamAttempt).filter(
        ExamAttempt.exam_id == exam_id,
        ExamAttempt.user_id == str(user.id),
        ExamAttempt.is_completed == False
    ).first()
    if existing_attempt:
        raise HTTPException(status_code=400, detail="You have already started this exam attempt")
    
    attempt = ExamAttempt(
        id=str(uuid4()),
        exam_id=exam_id,
        user_id=str(user.id),
        start_time=datetime.utcnow(),
        is_completed=False
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    return {"message": "Exam attempt started", "attempt_id": attempt.id}