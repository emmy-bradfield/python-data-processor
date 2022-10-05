from multiprocessing import get_logger
import logging
from .ConsoleHandler import ConsoleHandler

def logger(level=logging.INFo):
    logger = get_logger()
    logger.setLevel(level)
    handler = ConsoleHandler()
    handler.setFormatter(logging.Formatter(
        "%(levelname)s: %(asctime)s - %(process)s - %(message)s"))
    logger.addHandler(handler)

    return logger

app_logger = logger()