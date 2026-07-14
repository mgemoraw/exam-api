from fastapi import Depends, HTTPException, status
from core.roles import UserRole, ROLE_PERMISSIONS
from core.security import get_current_user


class RoleChecker:

    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user=Depends(get_current_user)):

        if current_user.role not in self.allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action."
            )

        return current_user
    


class PermissionChecker:

    def __init__(self, permission: str):
        self.permission = permission

    def __call__(self, user=Depends(get_current_user)):

        permissions = ROLE_PERMISSIONS.get(user.role, set())

        if self.permission not in permissions:

            raise HTTPException(
                status_code=403,
                detail="Permission denied."
            )

        return user


AllowAdmin = RoleChecker([
    UserRole.ADMIN
])

AllowStaff = RoleChecker([
    UserRole.ADMIN,
    UserRole.STAFF
])

AllowStudent = RoleChecker([
    UserRole.ADMIN,
    UserRole.STAFF,
    UserRole.STUDENT
])