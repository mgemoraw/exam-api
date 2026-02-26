import logging
import sys

# get logger
logger = logging.getLogger()

# formatter
LOG_FORMAT ="%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"
formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("app.log")

# set formatter
stream_handler.setFormatter(formatter)

# add handlers to the logger
logger.handlers = [stream_handler, file_handler]

# set log-level
logger.setLevel(logging.INFO)