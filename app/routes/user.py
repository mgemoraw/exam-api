from typing import Optional
from fastapi import APIRouter, Depends, Form, Body
from fastapi.exceptions import HTTPException
from uuid import uuid4
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 

from app.models.user import User 
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.database import get_db, SessionLocal
from app.core.security import create_access_token, get_current_user, hash_password

router = APIRouter(
	prefix="/users",
	)


@router.get("/")
async def greetings():
	return {"message": "Hello users"}

@router.post("/auth/login")
async def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
# async def login(username:Optional[str] = Body(None), password: Optional[str]= Body(None), user_json: Optional[UserLogin] = None, db: Session = Depends(get_db)):

	# if username and password:
	# 	user = UserLogin(username=username, password=password)
	
	# elif user_json:
	# 	user = user_json
	
	# else:
	# 	raise HTTPException(
	# 		status_code=400,
	# 		detail="Invalid username or password"
	# 		)
	
	db_user = db.query(User).filter(User.username==user.username).first()
	if db_user is None:
		raise HTTPException(
			status_code=400,
			detail="Invalid username or password"
			)
	
	
	user_password = user.password
	if not hash_password(user_password) == db_user.hashed_password:
		raise HTTPException(
			status_code=400,
			detail="Invalid username or password"
			)
	
	# create and return token here
	access_token = create_access_token(data={"sub": str(db_user.id)})
	return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create")
async def create_user(user:UserCreate, db:Session = Depends(get_db)):
	new_user = User(
		id=uuid4(), 
		username=user.username, 
		email=user.email,
		is_superuser=user.is_superuser,
		hashed_password=hash_password(user.password)
		)

	db_user = db.query(User).filter(User.username==user.username).first()

	if db_user is not None:
		raise HTTPException(
			status_code=400,
			detail="Username already exists"
			)
	
	if new_user:
		db.add(new_user)
		db.commit()
		db.refresh(new_user)


	return new_user

@router.get("/get/{user_id}")
async def get_user(user_id:str, db:Session = Depends(get_db)):
	user = db.query(User).filter(User.id==user_id).first()
	return user

@router.get("/get/users/", response_model=list[UserResponse])
async def get_users(user: User = Depends(get_current_user), db:Session = Depends(get_db)):
	users = db.query(User).limit(100).all()
	return users


@router.get("/get/me/", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user), db:Session = Depends(get_db)):
	return {
		"id": user.id,
		"username": user.username,
		"email": user.email,
		"is_active": user.is_active,
		"is_superuser": user.is_superuser
	}

