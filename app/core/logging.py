import logging
import sys
import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))[:-8]

formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s %(message)s", datefmt="%d.%m.%Y %H:%M:%S")

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(formatter)
time_handler_info = logging.handlers.TimedRotatingFileHandler(
    APP_ROOT + "/logs/logs_info.log", when="m", interval=10, backupCount=1)

time_handler_info.doRollover()
time_handler_info.setFormatter(formatter)
logger_info = logging.getLogger("my_info")
logger_info.setLevel(logging.DEBUG)  # set to INFO
logger_info.addHandler(consoleHandler)
logger_info.addHandler(time_handler_info)

logger = logging.getLogger(__file__)
logger_error_handler = logging.handlers.RotatingFileHandler(
    APP_ROOT + "/logs/logs_error.log", maxBytes=100000, backupCount=1
)
logger_error_handler.setFormatter(formatter)
logger.setLevel(logging.ERROR)
logger.addHandler(consoleHandler)
logger.addHandler(logger_error_handler)
