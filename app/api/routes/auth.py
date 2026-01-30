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
from app.core.database import get_db
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


auth_router = APIRouter(
	prefix="/auth",
	tags=['Authentication']
	)


@auth_router.post("/login")
async def login(username: str, password:str, db: Session = Depends(get_db)):
	"""
    Authenticate user and return access & refresh tokens
    """
	# check if user exists
	user = db.query(User).filter(User.username==username).first()
	if not user:
		raise HTTPException(
			status_code=400,
			detail="User is not Registered"
			)
	
	# verify password
	# if not verify_password(user.password, db_user.hashed_password):
	if not hash_password(password) == user.hashed_password:
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
	
	content =  {
		"access_token": access_token["token"],
        "refresh_token": refresh_token["token"],
        "token_type": "bearer",
        "expires_in": access_token["expires_in"],
        "refresh_expires_in": refresh_token["expires_in"]
	}

	# create a json response object
	response = JSONResponse(
		content=content,
		
	)
	response.set_cookie(
		key="access_token", 
		value=access_token["token"], 
		httponly=True,
		secure=True,
		samesite="Lax",
	)

	
	return response 


@auth_router.post("/token", response_model=UserTokenResponse)
async def access_token(data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
	user = db.query(User).filter(User.username==data.username).first()
	if not user:
		raise HTTPException(
			status_code=400,
			detail="Invalid username or password"
			)
	
	# if not verify_password(data.password, user.hashed_password):
	if not hash_password(data.password) == user.hashed_password:
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
	
	
	content =  {
		"access_token": access_token["token"],
        "refresh_token": refresh_token["token"],
        "token_type": "bearer",
        "expires_in": access_token["expires_in"],
        "refresh_expires_in": refresh_token["expires_in"]
	}

	# create a json response object
	response = JSONResponse(
		content=content,
		
	)
	response.set_cookie(
		key="access_token", 
		value=access_token["token"], 
		httponly=True,
		secure=True,
		samesite="Lax",
	)

	return response


@auth_router.post("/activate")
async def activate_user_account(username:str, db:Session = Depends(get_db)):
	user = db.query(User).filter(User.username==username).first()
	
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


@auth_router.delete("/{user_id}/refresh-tokens/delete")
async def delete_refresh_tokens(user_id: UUID, db:Session=Depends(get_db)):
	tokens = db.query(RefreshToken).filter_by(user_id=user_id).all()
	for token in tokens:
		db.delete(token)
	db.commit()
	return {"message": f"Deleted {len(tokens)} refresh tokens for user {user_id}"}

@auth_router.delete("/refresh-tokens")
async def delete_refresh_tokens(db:Session=Depends(get_db)):
	tokens = db.query(RefreshToken).all()
	return tokens





