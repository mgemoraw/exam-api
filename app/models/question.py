import uuid
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional, List
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Float, Text, Enum as SQLEnum, JSON

from datetime import datetime
from enum import Enum

from .base import Base
from .school import Department





class Question(Base):
    __tablename__ = "questions"
    id: Mapped[str] = Column(String(36), primary_key=True, index=True,default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = Column(String(36), ForeignKey('exam.id'), nullable=False)
    content: Mapped[str] = Column(JSON, nullable=False)
    marks: Mapped[int] = Column(Integer, default=1)

    department_id: Mapped[str] = Column(String(36), ForeignKey('departments.id'), nullable=True)
    course_id: Mapped[str] = Column(String(36), ForeignKey('courses.id'), nullable=True)
    module_id: Mapped[str] = Column(String(36), ForeignKey('modules.id'), nullable=True)

    # relationships
    options: Mapped[List['Option']] = relationship('Option', back_populates='question', cascade="all, delete",
    passive_deletes=True)

    exam_questions: Mapped[List["ExamQuestion"]] = relationship("ExamQuestion", back_populates="question", cascade="all, delete-orphan")
    attempt_questions :Mapped['AttemptQuestion'] = relationship('AttemptQuestion', back_populates='question')
    user_answers: Mapped['UserAnswer']=relationship('UserAnswer', back_populates='question', cascade='all, delete-orphan')

    # optional relationships to categorize question
    department: Mapped[Optional['Department']] = relationship('Department', back_populates='questions', foreign_keys=[department_id])
    course: Mapped[Optional['Course']] = relationship('Course', back_populates='questions', foreign_keys=[course_id])
    module: Mapped[Optional['Module']] = relationship('Module', back_populates='questions', foreign_keys=[module_id])



class Option(Base):
    __tablename__ = "choices"
    id: Mapped[str] = Column(String(36), primary_key=True, index=True, default=lambda:str(uuid.uuid4()))
    question_id: Mapped[str] = Column(String(36), ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    label: Mapped[str] = Column(String(5), nullable=False) # A, B, C, D
    content: Mapped[str] = Column(JSON, nullable=False)
    is_correct: Mapped[bool] = Column(Boolean, default=False)

    # relationships
    question:Mapped['Question'] = relationship('Question', back_populates='options')
    user_answers:Mapped[List['UserAnswer']] = relationship('UserAnswer', back_populates='selected_option', cascade='all, delete-orphan')
    
