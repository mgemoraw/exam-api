# models/user.py
from sqlalchemy import ForeignKey, String, Boolean, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import List, Optional
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app.models.auth import RefreshToken

# from app.models.auth import RefreshToken
from .base import Base
from datetime import datetime


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

class UserRoles(Base):
    __tablename__ = 'user_roles'
    id: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("users.id"),
    nullable=False
    )
    role_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('user_roles.id'),
        nullable=False
    )
    assigned_by: Mapped[UUID]  = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("users.id"),
    nullable=False
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow(),
    )

class Permission(Base):
    __tablename__ = 'permissions'
    id: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
    )


class RolePermission(Base):
    __tablename__ = 'role_permissions'
    id: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    role_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('user_roles.id'),
        nullable=False
    )
    permission_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('role_permissions.id'),
        nullable=False
    )

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
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

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("users.id"),
    nullable=False
    )

    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
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

    created_at: Mapped[str] = mapped_column(String(30), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(30), nullable=False)