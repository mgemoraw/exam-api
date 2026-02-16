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
from app.schemas.exam import AddQuestionsRequest, ExamCreateRequest, ExamResponse, AnswerSubmitRequest


exam_router = APIRouter(
	prefix="/exams",
	tags=['Exam'],
	)


@exam_router.get("/", response_model=List[ExamResponse])
async def greetings(user: User = Depends(get_current_user), db:Session=Depends(get_db)):
	exams = db.query(Exam).all()
     
	return exams	

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
        create_exam_by = str(user.id),
        updated_at = datetime.utcnow(),
        # questions=data.questions,
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
async def add_questions_to_exam(
    exam_id: str,
    data: AddQuestionsRequest,
    db: Session = Depends(get_db),
):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    for index, question_id in enumerate(data.question_ids):
        link = ExamQuestion(
            exam_id=exam_id,
            question_id=question_id,
            order=index + 1,
        )
        db.add(link)

    db.commit()

    return {"message": "Questions added successfully"}



# POST /exams/{exam_id}/start
@exam_router.post("/{exam_id}/start")
async def student_start_exam(
    exam_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    # Check visibility
    if not exam.is_visible:
        raise HTTPException(status_code=403, detail="Exam not available")

    # Check time window
    now = datetime.utcnow()
    if exam.start_time and now < exam.start_time:
        raise HTTPException(status_code=403, detail="Exam has not started yet")

    if exam.end_time and now > exam.end_time:
        raise HTTPException(status_code=403, detail="Exam has ended")

    # Prevent duplicate attempt
    existing_attempt = (
        db.query(ExamAttempt)
        .filter(
            ExamAttempt.exam_id == exam_id,
            ExamAttempt.student_id == user.id,
            ExamAttempt.is_completed == False
        )
        .first()
    )

    if existing_attempt:
        return existing_attempt

    attempt = ExamAttempt(
        exam_id=exam_id,
        student_id=user.id,
        start_time=now,
        is_completed=False,
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt

# GET /attempts/{attempt_id}/questions
@exam_router.get("/attempts/{attempt_id}/questions")
async def student_exam_attempted_questions(
    attempt_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    attempt = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.id == attempt_id)
        .first()
    )

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    # Ownership validation
    if attempt.student_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    if attempt.is_completed:
        raise HTTPException(status_code=400, detail="Exam already submitted")

    # Timer validation
    exam = db.query(Exam).filter(Exam.id == attempt.exam_id).first()

    now = datetime.utcnow()
    elapsed = (now - attempt.start_time).total_seconds() / 60

    if elapsed > exam.duration_minutes:
        raise HTTPException(status_code=400, detail="Time expired")

    # Get questions
    exam_questions = (
        db.query(ExamQuestion)
        .filter(ExamQuestion.exam_id == exam.id)
        .order_by(ExamQuestion.order)
        .all()
    )

    question_ids = [eq.question_id for eq in exam_questions]

    questions = (
        db.query(Question)
        .filter(Question.id.in_(question_ids))
        .all()
    )

    # Remove correct answers before sending
    response = []
    for q in questions:
        response.append({
            "id": q.id,
            "content": q.content,
            "options": q.options,  # assuming JSON field
        })

    return response


# POST /attempts/{attempt_id}/answer
@exam_router.post("/attempts/{attempt_id}/answer")
async def student_exam_attempted_answers(
    attempt_id: str,
    data: AnswerSubmitRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    attempt = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.id == attempt_id)
        .first()
    )

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    if attempt.student_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if attempt.is_completed:
        raise HTTPException(status_code=400, detail="Exam already submitted")

    exam = db.query(Exam).filter(Exam.id == attempt.exam_id).first()

    # Timer validation
    now = datetime.utcnow()
    elapsed = (now - attempt.start_time).total_seconds() / 60

    if elapsed > exam.duration_minutes:
        raise HTTPException(status_code=400, detail="Time expired")

    # Check if question belongs to exam
    link = (
        db.query(ExamQuestion)
        .filter(
            ExamQuestion.exam_id == exam.id,
            ExamQuestion.question_id == data.question_id
        )
        .first()
    )

    if not link:
        raise HTTPException(status_code=400, detail="Invalid question")

    # Check if answer already exists
    existing_answer = (
        db.query(UserAnswer)
        .filter(
            UserAnswer.attempt_id == attempt_id,
            UserAnswer.question_id == data.question_id
        )
        .first()
    )

    if existing_answer:
        existing_answer.selected_option = data.selected_option
    else:
        answer = UserAnswer(
            attempt_id=attempt_id,
            question_id=data.question_id,
            selected_option=data.selected_option,
        )
        db.add(answer)

    db.commit()

    return {"message": "Answer saved"}


@exam_router.post("/attempts/{attempt_id}/submit")
async def submit_exam_attempt(
    attempt_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    attempt = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.id == attempt_id)
        .first()
    )

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    # Ownership check
    if attempt.student_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Prevent double submission
    if attempt.is_completed:
        raise HTTPException(status_code=400, detail="Exam already submitted")

    exam = db.query(Exam).filter(Exam.id == attempt.exam_id).first()

    now = datetime.utcnow()
    elapsed = (now - attempt.start_time).total_seconds() / 60

    # Optional: allow submit even if time exceeded
    if elapsed > exam.duration_minutes:
        # You may allow forced submit instead of blocking
        pass

    # Fetch exam questions
    exam_questions = (
        db.query(ExamQuestion)
        .filter(ExamQuestion.exam_id == exam.id)
        .all()
    )

    question_ids = [eq.question_id for eq in exam_questions]

    questions = (
        db.query(Question)
        .filter(Question.id.in_(question_ids))
        .all()
    )

    question_map = {q.id: q for q in questions}

    # Fetch student answers
    student_answers = (
        db.query(UserAnswer )
        .filter(UserAnswer.attempt_id == attempt_id)
        .all()
    )

    answer_map = {a.question_id: a for a in student_answers}

    total_score = 0

    for question_id in question_ids:
        question = question_map.get(question_id)
        answer = answer_map.get(question_id)

        if not question:
            continue

        if answer:
            if answer.selected_option == question.correct_option:
                answer.is_correct = True
                answer.marks_awarded = question.marks
                total_score += question.marks
            else:
                answer.is_correct = False
                answer.marks_awarded = 0
        else:
            # Student didn't answer
            new_answer = UserAnswer(
                attempt_id=attempt_id,
                question_id=question_id,
                selected_option=None,
                is_correct=False,
                marks_awarded=0,
            )
            db.add(new_answer)

    attempt.score = total_score
    attempt.is_completed = True
    attempt.end_time = now

    db.commit()
    db.refresh(attempt)

    return {
        "message": "Exam submitted successfully",
        "score": total_score,
        "maximum_marks": exam.maximum_marks,
        "completed_at": attempt.end_time,
    }


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