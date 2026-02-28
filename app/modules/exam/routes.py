from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.infrastructure.database import get_db
from .services import ExamService
from .schemas import ExamCreateRequest, ExamResponse
from .exceptions import ExamNotFoundError, ExamAlreadyExistsError

router = APIRouter(prefix="/exams", tags=["Exams"])


@router.post("/", response_model=ExamResponse)
def create_exam(
    payload: ExamCreateRequest,
    db: Session = Depends(get_db)
):
    service = ExamService(db)

    try:
        exam = service.create_exam(
            title=payload.title,
            total_marks=payload.total_marks
        )
        return exam

    except ExamAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exam already exists"
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