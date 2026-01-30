import uuid
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional, List

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Float, Text, Enum as SQLEnum

from datetime import datetime
from app.models.base import Base
from enum import Enum


class ExamTypeEnum(str, Enum):
    MODEL_EXIT_EXAM = 'model exit exam'
    HOLISTIC_EXAM = 'holistic exam'
    ENTRANCE_EXAM = 'entrance exam'

EXAM_TYPE_LABELS = {
    ExamTypeEnum.MODEL_EXIT_EXAM: "MEE",
    ExamTypeEnum.HOLISTIC_EXAM: "HE",
    ExamTypeEnum.ENTRANCE_EXAM: "EE",
}


class Exam(Base):
    __tablename__ = "exam"
    id: Mapped[UUID] = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[int] = Column(String, nullable=False)
    maximum_marks: Mapped[int] = Column(Integer, default=100, nullable=False)
    duration_minutes: Mapped[int] = Column(Integer, nullable=False)
    exam_type = Column(SQLEnum(ExamTypeEnum), server_default=ExamTypeEnum.MODEL_EXIT_EXAM.value, nullable=False)

    description: Optional[str] = Column(String, nullable=True)
    is_visible = Column(Boolean, default=False)
    start_time = Column(DateTime, nullable=True) # when exam becomes visible
    end_time = Column(DateTime, nullable=True)   # when exam closes
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    # relationships
    exam_questions: Mapped[List["ExamQuestion"]] = relationship("ExamQuestion", back_populates="exam", cascade="all, delete-orphan")
    attempts: Mapped[List['ExamAttempt']] = relationship('ExamAttempt', back_populates='exam', foreign_keys='ExamAttempt.exam_id')

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[UUID] = Column(String, primary_key=True, index=True,default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[UUID] = Column(String, ForeignKey('exam.id'), nullable=False)
    content: Mapped[str] = Column(String, nullable=False)
    marks: Mapped[int] = Column(Integer, default=1)

    # relationships
    options: Mapped[List['Option']] = relationship('Option', back_populates='question')

    exam_questions: Mapped[List["ExamQuestion"]] = relationship("ExamQuestion", back_populates="question", cascade="all, delete-orphan")
    attempt_questions :Mapped['AttemptQuestion'] = relationship('AttemptQuestion', back_populates='question')
    user_answers: Mapped['UserAnswer']=relationship('UserAnswer', back_populates='question', cascade='all, delete-orphan')


class Option(Base):
    __tablename__ = "choices"
    id: Mapped[UUID] = Column(String, primary_key=True, index=True, default=lambda:str(uuid.uuid4()))
    question_id: Mapped[UUID] = Column(String, ForeignKey('questions.id'), nullable=False)
    content: Mapped[str] = Column(String, nullable=False)
    is_correct: Mapped[bool] = Column(Boolean, default=False)

    # relationships
    question:Mapped['Question'] = relationship('Question', back_populates='options')
    user_answers:Mapped[List['UserAnswer']] = relationship('UserAnswer', back_populates='selected_option', cascade='all, delete-orphan')
    


class ExamQuestion(Base):
    __tablename__ = "exam_questions"
    id: Mapped[UUID] = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = Column(String, ForeignKey("exam.id"), primary_key=True)
    question_id: Mapped[UUID] = Column(String, ForeignKey("questions.id"), primary_key=True)


    # relationships
    question: Mapped['Question'] = relationship('Question', back_populates='exam_questions')
    exam: Mapped['Exam'] = relationship('Exam', back_populates='exam_questions')

class ExamAttempt(Base):
    __tablename__ = "exam_attempt"
    id: Mapped[UUID] = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = Column(String, ForeignKey('users.id'), nullable=False)
    exam_id: Mapped[str] = Column(String, ForeignKey('exam.id'), nullable=False)
    started_at: Mapped[DateTime] = Column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[DateTime]  = Column(DateTime, nullable=False)
    score: Mapped[Optional[float]] = Column(Float, nullable=True)
    
    is_completed: Mapped[bool] = Column(Boolean, default=False)
    is_passed: Mapped[Optional[bool]] = Column(Boolean, nullable=True)
    is_expired: Mapped[bool] = Column(Boolean, default=False)
    is_graded: Mapped[bool] = Column(Boolean, default=False)

    completed_at: Mapped[Optional[DateTime]] = Column(DateTime, nullable=True)
    status: Mapped[str] = Column(String, nullable=False) # IN_PROGRESS, COMPLETED, EXPIRE

    # relationships
    user = relationship('User', back_populates='exam_attempts')
    exam:Mapped['Exam'] = relationship('Exam', back_populates='attempts', foreign_keys=[exam_id])
    questions = relationship('AttemptQuestion', back_populates='attempt', cascade="all, delete-orphan")
    user_answers:Mapped[List['UserAnswer']] = relationship('UserAnswer', back_populates='attempt', cascade="all, delete-orphan")


class AttemptQuestion(Base):
    __tablename__ = "attempt_question"
    id: Mapped[UUID] = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    attempt_id: Mapped[UUID] = Column(String, ForeignKey('exam_attempt.id'), nullable=False)
    question_id: Mapped[UUID] = Column(String, ForeignKey('questions.id'), nullable=False)
    order_index: Mapped[int] = Column(Integer, nullable=False)

    # relationshoips
    attempt:Mapped['ExamAttempt'] = relationship('ExamAttempt', back_populates='questions')
    question :Mapped['Question'] = relationship('Question', back_populates='attempt_questions')
    user_answer:Mapped['UserAnswer'] = relationship('UserAnswer', back_populates='attempt_question', uselist=False)


class UserAnswer(Base):
    __tablename__ = "user_answers"
    id: Mapped[UUID] = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    attempt_id: Mapped[UUID] = Column(String, ForeignKey('exam_attempt.id'), nullable=False)    
    question_id: Mapped[UUID] = Column(String, ForeignKey('questions.id'), nullable=False)
    attempt_question_id: Mapped[UUID] = Column(String, ForeignKey('attempt_question.id'), nullable=True)
    selected_option_id: Mapped[UUID] | None = Column(String, ForeignKey('choices.id'), nullable=True)    

    # relationships
    attempt: Mapped['ExamAttempt'] = relationship('ExamAttempt', back_populates='user_answers')
    question:Mapped['Question'] = relationship('Question', back_populates='user_answers')
    selected_option: Mapped['Option'] = relationship('Option', back_populates='user_answers', foreign_keys=[selected_option_id])
    attempt_question: Mapped['AttemptQuestion'] = relationship('AttemptQuestion', back_populates='user_answer')



""" example queries
attempt = db.query(ExamAttempt).filter_by(id=attempt_id).first()
for aq in attempt.questions:
    print(aq.order_index, aq.question.text, aq.user_answer.selected_option_id)

user_attempts = db.query(ExamAttempt).filter_by(user_id=user_id).all()
"""