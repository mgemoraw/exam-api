from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import get_db    
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/auth/login")

SECRET_KEY = "NKPD9W4hV/+YStZ+RejELM68Dw5okI5TrYrNWRcIf8q/OGfvxQXvtEirGA4yp9syAQkf3CWFqzH/nrV844dj8Q=="
ALGORITHM = "HS256"


def verify_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def hash_password(password: str) -> str:
    # Implement a proper password hashing mechanism here
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password


def get_current_user(user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        # Convert user_id to UUID if necessary
        from uuid import UUID
        user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
     # Optional: Check if user is active
    if hasattr(user, 'is_active') and not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Optional: Check if user is deleted
    if hasattr(user, 'is_deleted') and user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="User account has been deleted"
        )
    
    return user