from __future__ import annotations

import logging
import sys
from pathlib import Path

from app.core.config import settings


# ==========================================================
# Log Directory
# ==========================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "application.log"


# ==========================================================
# Formatter
# ==========================================================

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


formatter = logging.Formatter(
    fmt=LOG_FORMAT,
    datefmt=DATE_FORMAT,
)


# ==========================================================
# Logger Factory
# ==========================================================

def get_logger(
    name: str,
) -> logging.Logger:
    """
    Create or retrieve a configured logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(
        logging.DEBUG
        if settings.debug
        else logging.INFO
    )

    # ------------------------------------------
    # Console Handler
    # ------------------------------------------

    console_handler = logging.StreamHandler(
        sys.stdout
    )

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )

    # ------------------------------------------
    # File Handler
    # ------------------------------------------

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

    logger.propagate = False

    return logger