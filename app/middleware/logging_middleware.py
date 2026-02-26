import logging
import sys 
from enum import StrEnum
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid
from app.core.logger import logger

LOG_FORMAT_DEBUG="%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"






class LogLevels(StrEnum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"

def configure_logging(log_level: str = LogLevels.error):
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]

    if log_level not in log_levels:
        logging.basicConfig(level=LogLevels.error)
        return

    if log_level == LogLevels.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return 

    logging.basicConfig(level=log_level)



class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()
        # log_dict = {
        #     'url': request.url.path,
        #     'method': request.method,
        # }

        # logger.info(log_dict)

        try:
            response = await call_next(request)
        except Exception as exc:
            logger.exception(
                f"[{request_id}] Error: {request.method} {request.url.path}"
                )
            raise exc

        process_time = time.time() - start_time
        logger.info(
            f"Request ID: {request_id} | "
            f"{request.client.host} | "
            f"{request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"{process_time:.4f}s"
        )

        response.headers["X-Request-ID"] = request_id
        return response


# @app.middleware("http")
async def app_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    # log_dict = {
    #         'url': request.url.path,
    #         'method': request.method,
    #     }

    # logger.info(log_dict)

    try:
        response = await call_next(request)

    except Exception as exc:
        logger.exception(
            f"RID: {request_id} | "
            f"Error processing request {request.method} {request.url.path}"
        )
        raise exc

    process_time = time.time() - start_time

    logger.info(
        f"RID: {request_id} | "
        f"{request.client.host}:{request.client.port} | "
        f"{request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"{process_time:.4f}s"
    )

    response.headers["X-Request-ID"] = request_id

    return response