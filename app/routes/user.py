from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from uuid import uuid4
from sqlalchemy.orm import Session 

from models import User 
from schemas.user import UserCreate, UserLogin
from core.database import get_db, SessionLocal
from core.security import create_access_token, hash_password

router = APIRouter(
	prefix="/users",
	)


@router.get("/")
async def greetings():
	return {"message": "Hello users"}

@router.post("/auth/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
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
			)
	
	if new_user:
		db.add(new_user)
		db.commit()
		db.refresh(new_user)


	return new_user

@router.post("/get/{user_id}")
async def get_user(user_id:str, db:Session = Depends(get_db)):
	user = db.query(User).filter(User.id==user_id).first()
	return user
