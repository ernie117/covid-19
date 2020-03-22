import logging
import sys


def build_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s - %(name)s] - %(levelname)s - %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level=logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
