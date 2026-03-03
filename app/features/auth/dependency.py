from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.infrastructure.database import get_async_db, get_db
from ..user.models import User

# SECRETE_KEY = settings.SECRET_KEY
# ALGORITHM = settings.ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRETE_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    # EAGER LOADING: Use selectinload to fetch roles in the same operation
    result = await db.execute(
        select(User).where(User.email==email).options(selectinload(User.roles))
    )

    user = result.scalars().first()

    if user is None:
        raise credentials_exception
    
    return user