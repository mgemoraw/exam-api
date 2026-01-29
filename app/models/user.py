# models/user.py
from sqlalchemy import ForeignKey, String, Boolean, Column, DateTime, UniqueConstraint
from sqlalchemy import Enum as SQLEnum

from sqlalchemy.orm import Mapped, mapped_column
from typing import List, Optional
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app.models.auth import RefreshToken

# from app.models.auth import RefreshToken
from .base import Base
from datetime import datetime
from enum import Enum

class RoleName(str, Enum):
    ADMIN = "admin"
    QA_DIRECTOR="qa_director"
    DEAN="dean"
    APO='apo'
    QA_OFFICER="qa_officer"
    CHAIR_HOLDER="chair_holder"
    COURSE_CHAIR="course_chair"
    EDITOR = "editor"
    STUDENT = "student"
    

class PermissionName(str, Enum):
    CREATE_EXAM = "create_exam"
    ASSIGN_ROLE = "assign_role"
    VIEW_RESULT = "view_result"
    GENERATE_REPORT = "generate_report"
    CREATE_ANNOUNCEMENT='create_announcement'


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    name: Mapped[RoleName] = mapped_column(SQLEnum(RoleName, name="role_name_enum", native_enum=False), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    # relationships
    user_roles: Mapped[List['UserRole']] = relationship('UserRole', back_populates='role', cascade='all, delete-orphan')
    user_role_permissions: Mapped[List['RolePermission']] = relationship('RolePermission', back_populates='role', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Role name={self.name}>"



class UserRole(Base):
    __tablename__ = 'user_roles'
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_role"),)

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
    nullable=False,
    )
    role_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('roles.id'),
        nullable=False
    )
    assigned_by: Mapped[UUID]  = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("users.id"),
    nullable=False, 
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow(),
    )

    # relationships
    user: Mapped['User'] = relationship('User', back_populates='user_roles', foreign_keys=[user_id])
    assigner: Mapped['User'] = relationship('User', back_populates='assigned_roles', foreign_keys=[assigned_by])
    role: Mapped['Role'] = relationship('Role', back_populates='user_roles')

    def __repr__(self):
        return f"<UserRole user_id={self.user_id} role_id={self.role_id} assigned_by={self.assigned_by}>"

    

class Permission(Base):
    __tablename__ = 'permissions'
    id: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    name: Mapped[PermissionName] = mapped_column(
        SQLEnum(PermissionName, name="permission_name_enum", native_enum=False), 
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
    )

    # relationships
    user_role_permissions: Mapped[List['RolePermission']] = relationship('RolePermission', back_populates='permission', cascade="all, delete-orphan", foreign_keys="RolePermission.permission_id")

    def __repr__(self):
        return f"<Permission name={self.name}>"



class RolePermission(Base):
    __tablename__ = 'role_permissions'
    __table_args__ = (UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),)

    id: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    role_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('roles.id'),
        nullable=False
    )
    permission_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('permissions.id'),
        nullable=False
    )

    
    # relationships
    permission: Mapped['Permission'] = relationship('Permission', back_populates='user_role_permissions', foreign_keys=[permission_id])
    role: Mapped['Role'] = relationship('Role', back_populates='user_role_permissions', foreign_keys=[role_id])

    def __repr__(self):
        return f"<RolePermission role_id={self.role_id} permission_id={self.permission_id}>"


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

    # relationships
    user_roles: Mapped[List['UserRole']] = relationship('UserRole', back_populates='user', cascade="all, delete-orphan", foreign_keys="UserRole.user_id")
    assigned_roles: Mapped[List['UserRole']] = relationship('UserRole', back_populates='assigner', foreign_keys="UserRole.assigned_by")
    profile: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user')
    refresh_tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user')

    
    def __repr__(self):
        return f"{self.id}-{self.username}"


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