# app/models/token.py
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, UniqueConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

import uuid

from app.infrastructure.base import Base
from enum import Enum
from datetime import datetime
from typing import List, Optional

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

class RefreshToken(Base):
    """Model for storing refresh tokens"""
    __tablename__ = "refresh_tokens"
    
    id = Column(String(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    jti = Column(String(64), unique=True, index=True, nullable=False)  # JWT ID
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, )
    token_hash = Column(String(128), nullable=False)  # Hashed token for security
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationship
    user: Mapped['User'] = relationship("User", back_populates="refresh_tokens")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
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
        nullable=False,
    )
    role_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('roles.id'),
        nullable=False
    )
    assigned_by: Mapped[str]  = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=False, 
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),  server_default=func.now(),
    )

    # relationships
    user: Mapped['User'] = relationship('User', back_populates='user_roles', foreign_keys=[user_id])
    assigner: Mapped['User'] = relationship('User', back_populates='assigned_roles', foreign_keys=[assigned_by])
    role: Mapped['Role'] = relationship('Role', back_populates='user_roles')

    def __repr__(self):
        return f"<UserRole user_id={self.user_id} role_id={self.role_id} assigned_by={self.assigned_by}>"

    

class Permission(Base):
    __tablename__ = 'permissions'
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
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

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    role_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('roles.id'),
        nullable=False
    )
    permission_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('permissions.id'),
        nullable=False
    )

    
    # relationships
    permission: Mapped['Permission'] = relationship('Permission', back_populates='user_role_permissions', foreign_keys=[permission_id])
    role: Mapped['Role'] = relationship('Role', back_populates='user_role_permissions', foreign_keys=[role_id])

    def __repr__(self):
        return f"<RolePermission role_id={self.role_id} permission_id={self.permission_id}>"
