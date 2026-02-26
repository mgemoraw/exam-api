from fastapi import APIRouter
from app.modules.exam.routes import router as exam_router
from app.modules.user.routes import router as user_router
from app.modules.auth.routes import auth_router

v1_router = APIRouter(
    prefix="/v1",
    tags=["VERSION 1.0.0"],
)

v1_router.include_router(auth_router,)
v1_router.include_router(exam_router, prefix="/exams", tags=["Exams"])
v1_router.include_router(user_router, prefix="/users", tags=["Users"])