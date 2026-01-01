from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Float

from datetime import datetime
from models.base import Base


class Exam(Base):
    __tablename__ = "exam"
    id: UUID = Column(String, primary_key=True, index=True)
    title: str = Column(String, nullable=False)
    duration_minutes: int = Column(Integer, nullable=False)
    description: Optional[str] = Column(String, nullable=True)

class Question(Base):
    __tablename__ = "question"
    id: UUID = Column(String, primary_key=True, index=True)
    exam_id: UUID = Column(String, ForeignKey('exam.id'), nullable=False)
    text: str = Column(String, nullable=False)


class Option(Base):
    __tablename__ = "option"
    id: UUID = Column(String, primary_key=True, index=True)
    question_id: UUID = Column(String, ForeignKey('question.id'), nullable=False)
    text: str = Column(String, nullable=False)
    is_correct: bool = Column(Boolean, default=False)


class ExamAttempt(Base):
    __tablename__ = "exam_attempt"
    id: UUID = Column(String, primary_key=True, index=True)
    user_id: UUID = Column(String, ForeignKey('users.id'), nullable=False)
    exam_id: UUID = Column(String, ForeignKey('exam.id'), nullable=False)
    started_at: datetime = Column(DateTime, default=datetime.utcnow)
    expires_at: datetime = Column(DateTime, nullable=False)
    score: Optional[float] = Column(Float, nullable=True)
    completed_at: Optional[str] = Column(String, nullable=True)
    status: str = Column(String, nullable=False) # IN_PROGRESS, COMPLETED, EXPIRE

class AttemptQuestion(Base):
    __tablename__ = "attempt_question"
    id: UUID = Column(String, primary_key=True, index=True)
    attempt_id: UUID = Column(String, ForeignKey('exam_attempt.id'), nullable=False)
    question_id: UUID = Column(String, ForeignKey('question.id'), nullable=False)
    order_index: int = Column(Integer, nullable=False)

class Answer(Base):
    __tablename__ = "answer"
    id: UUID = Column(String, primary_key=True, index=True)
    attempt_id: UUID = Column(String, ForeignKey('exam_attempt.id'), nullable=False)    
    question_id: UUID = Column(String, ForeignKey('question.id'), nullable=False)
    selected_option_id: UUID | None = Column(String, ForeignKey('option.id'), nullable=True)    
