from fastapi import FastAPI

from .import models # critical import to start creating tables at startup

from app.core.database import engine
from .models.base import Base

# from route import router as exam_router
from app.routes.user import router as user_router
from app.routes.exam import router as exam_router
from app.middlewares.auth_middleware import auth_middleware

# creating app
app = FastAPI()

app.middleware("http")(auth_middleware)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Welcome to the Exam API"}


app.include_router(exam_router)
app.include_router(user_router)
app.include_router(exam_router)
