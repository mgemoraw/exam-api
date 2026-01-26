from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from uuid import UUID

from app.core.database import get_db
from app.core.security import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.models.user import User


def get_user(tokens: dict = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = tokens.get("access_token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")

        if user_id is None:
            # db.rollback()
            raise credentials_exception
        
        user = db.get(User, UUID(user_id))
        # user = db.query(User).filter(User.id == UUID(user_id)).first()
        if user is None:
            db.rollback()
            raise credentials_exception

        return user

    except JWTError:
        # db.rollback()
        raise credentials_exception

    except  Exception as e:
        db.rollback()
        raise credentials_exception
    
