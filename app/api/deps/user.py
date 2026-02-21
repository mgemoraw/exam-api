from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from uuid import UUID

from app.infrastructure.database import get_db
from app.core.security import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.models.user import User


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials. Token Invalid or Expired.",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    # print("Passed token: ", token)

    if token is None:
        raise HTTPException(status_code=401, detail="Invalid/Missing token")

    try:
        # token = tokens.get("access_token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        
        user = db.get(User, str(user_id))
        # user = db.query(User).filter(User.id == UUID(user_id)).first()
        if user is None:
            raise credentials_exception

        return user

    except JWTError:
        raise credentials_exception

  
    
def get_current_user(token: str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    # print("TOKEN: ", token)
    if not token:
        raise credentials_exception
    
    try:
        # token = tokens.get("access_token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        
        user = db.get(User, str(user_id))
        # user = db.query(User).filter(User.id == UUID(user_id)).first()
        if user is None:
            raise credentials_exception

        return user

    except JWTError:
        raise credentials_exception