import logging
from typing import Optional

class Logger:
    def __init__(self, mode: bool):
        if not mode:
            logging.basicConfig(
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%m/%d %H:%M",
                level=logging.INFO
            )
            logging.info(f"Logger initialized in development mode.")
        else:
            logging.basicConfig(
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%m/%d %H:%M",
                level=logging.ERROR
            )
            logging.info(f"Logger initialized in production mode.")
        self.logger = logging.getLogger("main-logger")

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

logger_instance: Optional[Logger] = None

def init_logger(mode: bool):
    global logger_instance
    if logger_instance is None:
        logger_instance = Logger(mode)
    return logger_instance

def get_logger() -> Logger:
    if logger_instance is None:
        raise RuntimeError("Logger has not been initialized.")
    return logger_instance
