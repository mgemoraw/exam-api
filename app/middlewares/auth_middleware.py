from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Set
import re

from app.core.security import verify_token


# PUbic endpoints that do not require authentication
PUBLIC_ENDPOINTS: Set[str] = {
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/users/auth/login",
    "/users/register",
    "/public/.*",
}


def is_public_path(path: str) -> bool:
    """Check if the requested path is public."""
    for pattern in PUBLIC_ENDPOINTS:
        if re.match(pattern, path):
            return True
    return False


async def auth_middleware(request: Request, call_next):

    # Skip authentication for public routes
    if is_public_path(request.url.path):
        return await call_next(request)
    
    # Get token from header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer"):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Not authenticated"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    

    token = auth_header.replace("Bearer ", "")

    try:
        # Verify token
        user_id = verify_token(token)
        # Attache user info to request state
        request.state.user_id = user_id
        request.state.is_authenticated = True

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Not authorized"},
            headers={"WWW-Authenticate": "Bearer"},
        )
   
    response = await call_next(request)
    return response