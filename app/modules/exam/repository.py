from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from .models import Exam


class ExamRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, exam_id: UUID) -> Exam | None:
        return self.db.get(Exam, exam_id)

    def get_by_title(self, title: str) -> Exam | None:
        stmt = select(Exam).where(Exam.title == title)
        return self.db.scalar(stmt)

    def list(self, skip: int = 0, limit: int = 20):
        stmt = select(Exam).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()

    def create(self, exam: Exam) -> Exam:
        self.db.add(exam)
        return exam

    def delete(self, exam: Exam):
        self.db.delete(exam)