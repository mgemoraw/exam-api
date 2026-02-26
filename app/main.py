from fastapi import FastAPI
from contextlib import asynccontextmanager

# import redis
import redis.asyncio as redis
import os


# import models # critical import to start creating tables at startup
from app.infrastructure.database import engine
# from app.models import Base
from app.infrastructure.base import Base 
from app.core.logging import setup_logging

# from app.api.routes.user import  user_router
# from app.api.routes.auth import auth_router
# from app.api.routes.exam import exam_router
# from app.api.routes.question import question_router
# from app.api.routes.school import school_router
# from app.api.routes.news import news_router
# from app.modules.user.routes import router

from app.api.v1.router import v1_router




from app.middleware.auth_middleware import auth_middleware
from app.middleware.logging_middleware import LoggingMiddleware
import logging


PRODUCTION = False # make it True for production

# logger setup
setup_logging()
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__file__)
# configure_logging(LogLevels.info)

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_db = int(os.getenv("REDIS_DB", 0))
redis_password = os.getenv("REDIS_PASSWORD", None)

# redis.Redis client setup
# redis_client = redis.Redis(
#     host=redis_host,
#     port=redis_port,
#     db=redis_db,
#     password=redis_password,
#     decode_responses=True
# )

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    password="",
    decode_responses=True,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    logger.info("Starting up FASTAPI SERVER ...")
    # Base.metadata.create_all(bind=engine)
    
    yield  # App runs here
    
    # Shutdown: Clean up
    logger.info("Shutting down FASTAPI SERVER...")
    engine.dispose()


# creating app
app = FastAPI(
    docs_url=None if PRODUCTION else "/docs",
    redoc_url=None if PRODUCTION else "/redoc",
    openapi_url=None if PRODUCTION else "/openapi.json",
    lifespan=lifespan,
    title="Exam API",
    version="1.2.0",
    )

app.middleware("http")(auth_middleware)

# ADD LOGGING MIDDLEWARE
# app.middleware("http")(LoggingMiddleware)
app.middleware(LoggingMiddleware)

# @app.on_event("startup")
# def startup():
#     Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    payload = {"message": "Welcome to the Exam API"}
    logger.info("Root endpoint accessed")
    return payload

@app.get("/health")
async def health_check():
    payload = {"status": "healthy"}
    logger.info("Health check endpoint accessed")
    return payload

@app.get("/redis-test")
async def redis_test():
    try:
        await redis_client.set("test_key", "Hello, Redis!")
        value = await redis_client.get("test_key")
        return {"redis_test": value}
    except Exception as e:
        logger.error(f"Redis test failed: {e}")
        return {"error": "Failed to connect to Redis"}
    

# app.include_router(auth_router)
# app.include_router(user_router)
# app.include_router(exam_router)
# app.include_router(question_router)
# app.include_router(school_router)
# app.include_router(news_router)
# app.include_router(router)
app.include_router(v1_router, prefix="/api")



if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST_DOMAIN", "0.0.0.0"), port=int(os.getenv("HOST_PORT", 8001)))
