import secrets
from typing import Any, Dict, Optional
from fastapi import  Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from app.core.database import get_db    
from app.models.user import User
from app.core.config import settings

import uuid 

SECRET_KEY = "NKPD9W4hV/+YStZ+RejELM68Dw5okI5TrYrNWRcIf8q/OGfvxQXvtEirGA4yp9syAQkf3CWFqzH/nrV844dj8Q=="
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)

pwd_context = CryptContext(schemes=['argon2', "bcrypt", "pbkdf2_sha256"], deprecated='auto')
myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt"])


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token expired or invalid"
)
unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You are not Authorized"
)

# Initialize Redis for token storage
redis_client: Optional[Redis] = None
async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    if not redis_client:
        redis_client = Redis.from_url(settings.REDIS_URL)



def authenticate_user(username: str, password: str, db:Session):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False

    return user
 
def verify_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
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
    

def create_access_token(data: dict=Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)

    # add token metadata
    jti = secrets.token_urlsafe(16)
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(UTC),
        "jti": jti,  # Uniqe ID for this access toke
        "type": "access",
        "scope": "user_ccess",
    })

    # Create token payload
    # payload = {
    #     "sub": data.get("sub"),
    #     "exp": expire,
    #     "iat": datetime.now(UTC),
    #     "type": "access",
    #     "jti": jti,
    #     "scope": "user_access"
    # }
    
    # to_encode.update({"exp": expire})

    jwt_token = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
        )
    
    return {
        "token": jwt_token,
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES*60,
        "jti": jti,
        "token_type": "bearer",
    }


async def create_refresh_token(user_id: str, db) -> Dict[str, Any]:
    """
    Create refresh token and store it in database
    Implements refresh token rotation for security
    """
    # Generate unique token ID
    jti = secrets.token_urlsafe(32)
    
    # Calculate expiration
    expire = datetime.now(UTC) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    # Create token payload
    payload = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.now(UTC),
        "type": "refresh",
        "jti": jti,
        "scope": "refresh"
    }
    
    # Encode token
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    # Store refresh token in database (for invalidation)
    from app.models import RefreshToken

    # if refresh token for user already exists, update it
    existing_token = db.query(RefreshToken).filter_by(user_id=str(user_id)).first()
    if existing_token:
        existing_token.token_hash = hash_token(token)
        existing_token.expires_at = expire
        existing_token.is_revoked = False
    else:
        # add new refresh token if not exists
        db_refresh_token = RefreshToken(
        jti=jti,
        user_id=str(user_id),
        token_hash=hash_token(token),
        expires_at=expire,
        is_revoked=False
        )
        db.add(db_refresh_token)

    # Commit to database
    db.commit()
    
    # Also store in Redis for fast validation
    if redis_client:
        await redis_client.setex(
            f"refresh_token:{jti}",
            settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
            user_id
        )
    
    return {
        "token": token,
        "expires_in": settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        "jti": jti
    }

def hash_token(token: str) -> str:
    """Hash token for secure storage"""
    import hashlib
    return hashlib.sha256(token.encode()).hexdigest()

async def verify_token(token: str, expected_type: str = "access") -> dict:
    """
    Verify JWT token and check its type
    
    Args:
        token: JWT token to verify
        expected_type: "access" or "refresh"
    
    Returns:
        Decoded token payload if valid
    
    Raises:
        HTTPException if token is invalid or wrong type
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    type_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type. Expected {expected_type} token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Check token type
        if payload.get("type") != expected_type:
            raise type_exception
        
        # Additional validation for refresh tokens
        if expected_type == "refresh":
            jti = payload.get("jti")
            if not jti:
                raise credentials_exception
            
            # Check if refresh token is revoked
            if redis_client:
                # Check in Redis first
                stored_user = await redis_client.get(f"refresh_token:{jti}")
                if not stored_user:
                    raise credentials_exception
            else:
                # Fallback to database check
                from app.core.database import get_db
                from app.models import RefreshToken
                db = next(get_db())
                db_token = db.query(RefreshToken).filter(
                    RefreshToken.jti == jti,
                    RefreshToken.is_revoked == False
                ).first()
                if not db_token:
                    raise credentials_exception
        
        return payload
        
    except JWTError:
        raise credentials_exception


async def revoke_refresh_token(jti: str, db):
    """Revoke a refresh token (logout or security measure)"""
    if redis_client:
        await redis_client.delete(f"refresh_token:{jti}")
    
    # Mark as revoked in database
    from app.models import RefreshToken
    db_token = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    if db_token:
        db_token.is_revoked = True
        await db.commit()

def is_password_strong(password:str):
    SYMBOLS = ["!", "@", "#", "$", "%", "&", "*", "(", ")", "-", "_", "+", "=", "[", "]", "{", "}", "|", "\\", ";", ":", "'", '"', ",", "<", ".", ">", "/", "?"]
    
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in SYMBOLS for char in password):
        return False
    
    return True
    
    
def hash_password(password: str) -> str:
    # Implement a proper password hashing mechanism here
    import hashlib

    return hashlib.sha256(password.encode()).hexdigest()
    # return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password
    # return pwd_context.verify(plain_password, hashed_password)


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