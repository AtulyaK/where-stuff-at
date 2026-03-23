"""Centralized logging module for the Where's My Stuff application.

This module provides a configured logger with both console and rotating file
handlers, adhering to the Google Python Style Guide conventions.
"""

import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Optional


def get_logger(name: str, log_file: str = "app.log") -> logging.Logger:
    """Retrieves a configured logger instance.

    Sets up a logger that outputs to both the console and a rotating log file.
    The file handler keeps up to 5 backups, up to 5MB each.

    Args:
        name: The name of the logger (typically __name__ from the calling module).
        log_file: The path to the log file. Defaults to "app.log" in the root dir.

    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(name)

    # If the logger already has handlers, avoid adding duplicates.
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler (INFO level and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating File Handler (DEBUG level and above)
    try:
        file_handler = RotatingFileHandler(
            filename=log_file, maxBytes=5 * 1024 * 1024, backupCount=5  # 5 MB
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError as e:
        # Fallback if file logging fails (e.g. permissions)
        console_handler.setLevel(logging.DEBUG)
        logger.warning(f"Failed to set up file logging: {e}")

    return logger
