import logging
from config import LOG_LEVEL

def setup_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:  # Prevent adding multiple handlers in re-imports
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(levelname)s:     %(asctime)s, %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL)
    return logger