from fastapi import HTTPException, Depends, status
from typing import List, Optional
from app.core.security import get_user 
from ..user.models import User

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles


    def __call__(self, user: User = Depends(get_user)):
        # Extract role names from the user object
        user_role_names = [role.name for role in user.roles]

        # check if any of hte user's roles match tht allowed roles
        for role in self.allowed_roles:
            if role in user_role_names:
                return True
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the required permission",
        )


