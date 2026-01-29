from typing import Optional
from fastapi import APIRouter, Depends, Form, Body, Request
from fastapi.exceptions import HTTPException
from uuid import UUID, uuid4
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from sqlalchemy.exc import IntegrityError

from app.models.auth import RefreshToken
from app.models.user import User 
from app.schemas.user import UserCreate, UserLogin
from app.responses.user import  UserResponse, UserTokenResponse
from app.core.database import get_db, SessionLocal
from app.core.config import settings
from app.core.security import (
    create_access_token,
	create_refresh_token,
    is_password_strong,
	verify_token,
	hash_password,
	verify_password,
)
from app.api.deps.user import get_user, get_current_user


user_router = APIRouter(
	prefix="/users",
	tags=["Users"]
	)



@user_router.get("/me", response_model=UserResponse)
async def get_user_detail(current_user: UserLogin = Depends(get_current_user), db:Session=Depends(get_db)):
	
	if current_user is None:
		JSONResponse(
            status_code=401,
            content={"message": "You're not logged in"}
        )
	return current_user

@user_router.post("/create")
async def create_user(user:UserCreate, db:Session = Depends(get_db)):
	# check if existing user in database
	existing = db.query(User).filter((User.username==user.username) | (User.email==user.email)).first()

	if existing :
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
	
	try:
		new_user = User(
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
	
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="Username or email already exists")

	except Exception as e:
		db.rollback()
		raise HTTPException(status_code=500, detail="Internal server error")

@user_router.get("/", response_model=list[UserResponse])
async def get_all_users(user:User=Depends(get_current_user), db:Session = Depends(get_db)):
	try:
		users = db.query(User).all()
		return users
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="Username or email already exists")

	except Exception as e:
		db.rollback()
		print(e)
		raise HTTPException(status_code=500, detail="Internal server error")


@user_router.get("/{username}")
async def get_user_by_username(username:str, db:Session = Depends(get_db)):
	user = db.query(User).filter(User.username==username).first()
	return user

@user_router.get("/{email}")
async def get_user_by_email(email:str, db:Session = Depends(get_db)):
	user = db.query(User).filter(User.email==email).first()
	return user

@user_router.delete("/{username}")
async def delete_user(username:str, db:Session = Depends(get_db)):
	user = db.query(User).filter(User.username==username).first()
	db.delete(user)
	db.commit()

	return user


