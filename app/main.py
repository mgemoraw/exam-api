from fastapi import FastAPI
from contextlib import asynccontextmanager

# import models # critical import to start creating tables at startup

from core.database import engine
from models.base import Base

# from route import router as exam_router
from routes.user import router as user_router
from routes.exam import router as exam_router

@asynccontextmanager
def lifespan():
    # create basemodel
    Base.metadata.create_all(bind=engine)

    yield 

# creating app
app = FastAPI(lifespan=lifespan)


# @app.on_event("startup")
# def startup():
#     Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Welcome to the Exam API"}


app.include_router(exam_router)
app.include_router(user_router)
app.include_router(exam_router)
