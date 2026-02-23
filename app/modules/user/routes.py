from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# from app.core.dependencies import get_db
from app.infrastructure.database import get_db
from app.modules.user.repository import UserRepository
from app.modules.user.services import UserService
from app.modules.user.schemas import UserCreate

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
        return service.create_user(user.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

