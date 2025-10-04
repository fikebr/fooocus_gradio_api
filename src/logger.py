import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from .config import config


def setup_logging(
    log_file_path: str = config.logfile,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    rotation_type: str = "size",
    max_bytes: int = 10_485_760,
    backup_count: int = 3,
    encoding: str = "utf-8",
) -> logging.Logger:
    """Configure console + rotating file logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_dir = os.path.dirname(os.path.abspath(log_file_path))
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding=encoding,
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info(
        "Logging initialized: console=%s, file=%s at '%s'",
        logging.getLevelName(console_level),
        logging.getLevelName(file_level),
        log_file_path,
    )
    return logger


