from typing import Optional
from fastapi import APIRouter, Depends, Form, Body
from fastapi.exceptions import HTTPException
from uuid import uuid4
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 

from app.models.user import User 
from app.schemas.user import UserCreate, UserLogin
from app.responses.user import  UserResponse
from app.core.database import get_db, SessionLocal
from app.core.config import settings
from app.core.security import (
    create_access_token,
	create_refresh_token,
    is_password_strong,
	verify_token,
	get_current_user,
	hash_password,
	verify_password,
)
from app.api.deps.user import get_user


user_router = APIRouter(
	prefix="/users",
	tags=["authentication"]
	)

auth_router = APIRouter(
	prefix="/auth",
	)


@user_router.get("/")
async def greetings():
	return {"message": "Hello users"}

@auth_router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	"""
    Authenticate user and return access & refresh tokens
    """
	# check if user exists
	db_user = db.query(User).filter(User.username==user.username).first()
	if db_user is None:
		raise HTTPException(
			status_code=400,
			detail="Invalid username or password"
			)
	
	# verify password
	if not hash_password(user.password) == db_user.hashed_password:
		raise HTTPException(
			status_code=400,
			detail="Invalid username or password"
			)
	
	# check if user if active
	if not db_user.is_active:
		raise HTTPException(
			status_code=400,
			detail="User is not active"
			)
	# create and return token here
	access_token = create_access_token(data={"sub": str(db_user.id)})
	
	# refresh token
	refresh_token = create_refresh_token(
		user_id=str(db_user.id),
		db=db,
		)
	
	return {
		"access_token": access_token["token"],
        "refresh_token": refresh_token["token"],
        "token_type": "bearer",
        "expires_in": access_token["expires_in"],
        "refresh_expires_in": refresh_token["expires_in"]
	}


@user_router.post("/create")
async def create_user(user:UserCreate, db:Session = Depends(get_db)):
	# check if existing user in database
	db_user = db.query(User).filter(User.username==user.username, User.email==user.email).first()

	if db_user is not None:
		raise HTTPException(
			status_code=400,
			detail="Username or email already exists"
			)

	# Check the password strength of new user password
	if not is_password_strong(user.password):
		raise HTTPException(
			status_code=400,
			detail="Password is not strong enough"
			)
	
	new_user = User(
		id=uuid4(), 
		username=user.username, 
		email=user.email,
		is_superuser=user.is_superuser,
		hashed_password=hash_password(user.password)
		)

	if new_user:
		db.add(new_user)
		db.commit()
		db.refresh(new_user)


	return new_user

@user_router.get("/{user_id}")
async def get_user(user_id:str, db:Session = Depends(get_db)):
	user = db.query(User).filter(User.id==user_id).first()
	return user

@user_router.get("/", response_model=list[UserResponse])
async def get_users(user: UserLogin = Depends(get_user), db:Session = Depends(get_db)):
	users = db.query(User).limit(100).all()
	return users


@user_router.get("/me", response_model=UserResponse)
async def get_me(user: UserLogin = Depends(get_current_user), db:Session = Depends(get_db)):
	return {
		"id": user.id,
		"username": user.username,
		"email": user.email,
		"is_active": user.is_active,
		"is_superuser": user.is_superuser
	}

