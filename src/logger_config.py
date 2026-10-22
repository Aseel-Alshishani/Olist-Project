"""
Logger Configuration Module
Sets up production-grade logging to both console (stdout) and a log file.
"""

import logging
import sys
from pathlib import Path

def setup_logger(name: str = "olist_mlops", log_file: str = "logs/inference.log") -> logging.Logger:
    """
    Configures and returns a logger instance with dual handlers (Console & File).
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Prevent adding duplicate handlers if logger is called multiple times
    if logger.handlers:
        return logger

    # Ensure log directory exists
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Define professional log format
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. Console Handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 2. File Handler (Persistent logs)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Attach handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger