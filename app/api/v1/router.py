from fastapi import APIRouter
from app.features.exam.routes import router as exam_router
from app.features.user.routes import router as user_router
from app.features.auth.routes import auth_router
from app.features.question.routes import question_router
from app.features.school.routes import  school_router
from app.features.address.routes import  address_router

v1_router = APIRouter(
    prefix="/v1",
    # tags=["VERSION 1.0.0"],
)

v1_router.include_router(auth_router,)
v1_router.include_router(exam_router, )
v1_router.include_router(user_router, prefix="/users", tags=["Users"])
v1_router.include_router(question_router,)
v1_router.include_router(school_router,)
v1_router.include_router(address_router, prefix="/address", tags=["Address"])