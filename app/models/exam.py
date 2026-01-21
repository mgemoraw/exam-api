from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional, List

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Float

from datetime import datetime
from app.models.base import Base


class Exam(Base):
    __tablename__ = "exam"
    id: UUID = Column(String, primary_key=True, index=True)
    title: str = Column(String, nullable=False)
    maximum_marks: int = Column(Integer, default=100, nullable=False)
    duration_minutes: int = Column(Integer, nullable=False)
    description: Optional[str] = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())


class Question(Base):
    __tablename__ = "questions"
    id: UUID = Column(String, primary_key=True, index=True)
    exam_id: UUID = Column(String, ForeignKey('exam.id'), nullable=False)
    text: str = Column(String, nullable=False)

    # relationships
    choices:Mapped[List['Option']] = relationship('Option', back_populates='question')


class Option(Base):
    __tablename__ = "choices"
    id: UUID = Column(String, primary_key=True, index=True)
    question_id: UUID = Column(String, ForeignKey('questions.id'), nullable=False)
    text: str = Column(String, nullable=False)
    is_correct: bool = Column(Boolean, default=False)

    # relationships
    question = relationship('Question', back_populates='choices')


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

    # relationships
    user = relationship('User', back_populates='exam_attempts')
    questions = relationship('AttemptQuestion', back_populates='attempt')

class AttemptQuestion(Base):
    __tablename__ = "attempt_question"
    id: UUID = Column(String, primary_key=True, index=True)
    attempt_id: UUID = Column(String, ForeignKey('exam_attempt.id'), nullable=False)
    question_id: UUID = Column(String, ForeignKey('questions.id'), nullable=False)
    order_index: int = Column(Integer, nullable=False)

    # relationshoips
    attempt = relationship('ExamAttempt', back_populates='questions')


class UserAnswer(Base):
    __tablename__ = "user_answers"
    id: UUID = Column(String, primary_key=True, index=True)
    attempt_id: UUID = Column(String, ForeignKey('exam_attempt.id'), nullable=False)    
    question_id: UUID = Column(String, ForeignKey('questions.id'), nullable=False)
    selected_option_id: UUID | None = Column(String, ForeignKey('choices.id'), nullable=True)    
