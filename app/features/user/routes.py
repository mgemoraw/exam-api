from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# from app.core.dependencies import get_db
from app.api.deps.user import get_user, get_current_user
# from app.core.security import get_current_user
from app.infrastructure.database import get_db
from .repository import UserRepository
from .services import UserService
from .schemas import UserCreate, UserUpdate, UpdatePasswordRequest

router = APIRouter(
    prefix="/user",
    tags=["User"],
    )


def get_user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)


@router.post("/")
def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put("/")
def update_user(user_data:UserUpdate, service: UserService=Depends(get_user_service), user=Depends(get_user)):
    user_id = user.id
    try:
        return service.update_user(user_id=user_id, update_data=user_data.dict())
    except ValueError as e:
        raise HTTPException(status_code=4000, detail=str(e))


@router.put("/update-password")
def update_user_password(data: UpdatePasswordRequest, service: UserService=Depends(get_user_service), user=Depends(get_user)):
    try:
        return service.update_password(user.id, data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

 
@router.put("/{user_id}/reset-password")
def reset_password(user_id: str, data: UpdatePasswordRequest, service: UserService=Depends(get_user_service)):
    try:
        return service.update_password(user_id, data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    


