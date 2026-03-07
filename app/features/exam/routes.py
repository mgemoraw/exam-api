from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.infrastructure.database import get_db
from .services import ExamService
from .schemas import ExamCreateRequest, ExamResponse, ExamUpdateRequest
from .exception import ExamNotFoundError, ExamAlreadyExistsError

router = APIRouter(prefix="/exams", tags=["Exams"])




@router.post("/", response_model=ExamResponse)
def create_exam(
    payload: ExamCreateRequest,
    db: Session = Depends(get_db)
):
    service = ExamService(db)

    try:
        exam = service.create_exam(payload)
        return exam

    except ExamAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exam already exists"
        )


@router.get("/all", response_model=List[ExamResponse])
def get_exams(skip=False, limit=20, db:Session=Depends(get_db)):
    try:
        service = ExamService(db)
        exams = service.get_exams(skip=skip, limit=limit)
        return exams 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {str(e)}"
        )
    

@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam(exam_id: UUID, db: Session = Depends(get_db)):
    service = ExamService(db)

    try:
        return service.get_exam(exam_id)

    except ExamNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )

@router.put("/{exam_id}", response_model=ExamResponse)
def update_exam(exam_id: UUID, exam_data: ExamUpdateRequest, db:Session=Depends(get_db)):
    service = ExamService(db)

    try:
        return service.update_exam(exam_id, exam_data=exam_data)

    except ExamNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )

@router.post("/{exam_id}/add-questions")
def add_exam_questions(exam_id: UUID, questions: List[str], db:Session=Depends(get_db)):
    try:
        service = ExamService(db)

        return service.add_questions(questions)

    except ExamNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error - {str(e)}"
        )