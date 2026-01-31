from fastapi import FastAPI
from contextlib import asynccontextmanager

# import models # critical import to start creating tables at startup

from app.core.database import engine
from app.models import Base

# from route import router as exam_router

from app.api.routes.user import  user_router
from app.api.routes.auth import auth_router
from app.api.routes.exam import exam_router
from app.api.routes.school import school_router

from app.middlewares.auth_middleware import auth_middleware
import logging

logger = logging.getLogger(__file__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    print("Starting up...")
    # Base.metadata.create_all(bind=engine)
    
    yield  # App runs here
    
    # Shutdown: Clean up
    print("Shutting down...")
    engine.dispose()


# creating app
app = FastAPI(lifespan=lifespan)

app.middleware("http")(auth_middleware)

# @app.on_event("startup")
# def startup():
#     Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Welcome to the Exam API"}


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(exam_router)
app.include_router(school_router)