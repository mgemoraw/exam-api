# models/user.py
from sqlalchemy import ForeignKey, Integer, String, Boolean, Column, DateTime, UniqueConstraint, func 
from sqlalchemy import Enum as SQLEnum

from sqlalchemy.orm import Mapped, mapped_column
from typing import List, Optional
from sqlalchemy.orm import relationship
import uuid
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


from app.infrastructure.base import Base
# from ..auth.models import RefreshToken
# from ..exam.models import ExamAttempt 
# from ..news.models import News

from datetime import datetime
from enum import Enum


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Add relationship
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        "RefreshToken", 
        back_populates="user",
        cascade="all, delete-orphan", # Optional: deletes tokens when user is deleted
    )
    
    exam_attempts: Mapped[List['ExamAttempt']] = relationship('ExamAttempt', back_populates="user", )

    # relationships
    user_roles: Mapped[List['UserRole']] = relationship('UserRole', back_populates='user', cascade="all, delete-orphan", foreign_keys="UserRole.user_id",)
    assigned_roles: Mapped[List['UserRole']] = relationship('UserRole', back_populates='assigner', foreign_keys="UserRole.assigned_by", cascade="all, delete-orphan",)
    profile: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user', cascade="all, delete-orphan", uselist=False)
    refresh_tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user', cascade="all, delete-orphan")

    student_profile: Mapped['Student'] = relationship('Student', back_populates='user', cascade="all, delete-orphan")
    created_exams: Mapped[List['Exam']] = relationship('Exam', back_populates='user', foreign_keys='Exam.created_by')

    news_items: Mapped[List['News']] = relationship('News', back_populates='creator', foreign_keys='News.created_by')
    
    def __repr__(self):
        return f"{self.id}-{self.username}"


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=False
    )

    fname: Mapped[str] = mapped_column(String(100), nullable=True)
    mname: Mapped[str] = mapped_column(String(100), nullable=True)
    lname: Mapped[str] = mapped_column(String(100), nullable=True)
    bio: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str] = mapped_column(String(255), nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    website: Mapped[str] = mapped_column(String(255), nullable=True)
    birth_date: Mapped[str] = mapped_column(String(10), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    social_links: Mapped[str] = mapped_column(String(255), nullable=True)
    preferences: Mapped[str] = mapped_column(String(255), nullable=True)
    settings: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(String(30), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(String(30), nullable=False)

    # relationship
    user: Mapped['User'] = relationship('User', back_populates='profile', foreign_keys=[user_id])

    def __repr__(self):
        return f"{self.fname} {self.mname} {self.lname}"
    

class Student(Base):
    __tablename__ = "students"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=False
    )
    enrollment_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    program_id: Mapped[str] = mapped_column(String(36), ForeignKey('programes.id'))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    user: Mapped['User'] = relationship('User', back_populates='student_profile', foreign_keys=[user_id],)
    program: Mapped['Program'] = relationship('Program', back_populates='students', foreign_keys=[program_id])
    
    courses: Mapped[List['Course']] = relationship('Course', secondary="student_courses", back_populates='students')
    
    student_courses: Mapped[List['StudentCourse']] = relationship('StudentCourse', back_populates='student', cascade="all, delete-orphan")

    profile: Mapped[Optional['StudentProfile']] = relationship('StudentProfile', back_populates='student')


    def __repr__(self):
        return f"<Student enrollment_number={self.enrollment_number}>"
    

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    student_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey('students.enrollment_number'),
        nullable=False,
    )
    fname: Mapped[str] = mapped_column(
        String(100)
    )
    mname: Mapped[str] = mapped_column(
        String(100)
    )
    lname: Mapped[str] = mapped_column(
        String(100)
    )
    
    dob: Mapped[str] = mapped_column(String(10), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    enrolled_year:Mapped[int] = mapped_column(Integer, nullable=False)
    graduation_year:Mapped[int] =mapped_column(Integer, nullable=False)

    student = relationship('Student', back_populates='profile')
    

    @property
    def full_name(self) -> str:
        return f"{self.fname} {self.mname} {self.lname}"


    @property
    def graduation_year(self, program_year):
        return self.enrolled_year + program_year 
