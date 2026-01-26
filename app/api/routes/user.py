from typing import Optional
from fastapi import APIRouter, Depends, Form, Body
from fastapi.exceptions import HTTPException
from uuid import uuid4
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from sqlalchemy.exc import IntegrityError

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
	get_current_user,
	hash_password,
	verify_password,
)
from app.api.deps.user import get_user


user_router = APIRouter(
	prefix="/users",
	tags=["Users"]
	)

auth_router = APIRouter(
	prefix="/auth",
	tags=['Authentication']
	)


@auth_router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	"""
    Authenticate user and return access & refresh tokens
    """
	# check if user exists
	user = db.query(User).filter(User.username==data.username).first()
	if not user:
		raise HTTPException(
			status_code=400,
			detail="User is not Registered"
			)
	
	# verify password
	# if not verify_password(user.password, db_user.hashed_password):
	if not hash_password(data.password) == user.hashed_password:
		raise HTTPException(
			status_code=400,
			detail="Invalid username or password"
			)
	
	# check if user if active
	if not user.is_active:
		raise HTTPException(
			status_code=400,
			detail="User is not active"
			)
	# create and return token here
	access_token = create_access_token(data={"sub": str(user.id)})
	
	# refresh token
	refresh_token = await create_refresh_token(
		user_id=str(user.id),
		db=db,
		)
	
	return {
		"access_token": access_token["token"],
        "refresh_token": refresh_token["token"],
        "token_type": "bearer",
        "expires_in": access_token["expires_in"],
        "refresh_expires_in": refresh_token["expires_in"]
	}

@auth_router.post("/token", response_model=UserTokenResponse)
async def access_token(data:UserLogin, db:Session=Depends(get_db)):
	user = db.query(User).filter(User.username==data.username).first()
	if not user:
		raise HTTPException(
			status_code=400,
			detail="Invalid username or password"
			)
	
	if not verify_password(data.password, user.hashed_password):
		raise HTTPException(
			status_code=400,
			detail="Invalid username or password"
		)

	# check if user if active
	if not user.is_active:
		raise HTTPException(
			status_code=400,
			detail="User is not active. please activate your account throug email"
			)
	# create and return token here
	access_token = create_access_token(data={"sub": str(user.id)})
	
	# refresh token
	refresh_token = await create_refresh_token(
		user_id=str(user.id),
		db=db,
		)
	
	return {
		"access_token": access_token["token"],
        "refresh_token": refresh_token["token"],
        "token_type": "bearer",
        "expires_in": access_token["expires_in"],
        "refresh_expires_in": refresh_token["expires_in"]
	}
	return {
		"access_token": access_token,
	}

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

@auth_router.post("/activate")
async def activate_user_account(data: UserLogin, db:Session = Depends(get_db)):
	user = db.query(User).filter(User.username==data.username).first()
	
	if not user:
		raise HTTPException(
			status_code=400,
			detail="User is not Registered"
		)
	if user.is_active:
		raise HTTPException(
			status_code=400,
			detail="User is already active"
		)

	user.is_active=True
	db.commit()
	db.refresh(user)
	return user


@user_router.get("/")
async def get_all_users(db:Session = Depends(get_db)):
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



@user_router.get("/", response_model=list[UserResponse])
async def get_users(user: UserLogin = Depends(get_user), db:Session = Depends(get_db)):
	users = db.query(User).limit(100).all()
	return users


@user_router.get("/me", response_model=UserResponse)
async def get_me(user:User=Depends(get_user), db:Session=Depends(get_db)):
	data = db.query(User).filter(User.username==user.username).first()
	

	return {
		"message": "User profile",
		"data": data,
	}



@user_router.get("/user", response_model=UserResponse, )
async def get_user_data(user:User=Depends(get_user), db:Session=Depends(get_db)):
	if user is None:
		raise HTTPException(status_code=401, detail="Unauthorized")
	return user 
