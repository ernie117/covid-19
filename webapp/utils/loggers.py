import logging
import sys

LOGGERS = {}


def build_logger(name: str):
    if LOGGERS.get(name):
        return LOGGERS.get(name)

    logger = logging.getLogger(name)
    logger.setLevel(level=logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s - %(name)s] - %(levelname)s - %(message)s"
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level=logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    LOGGERS[name] = logger

    return logger
