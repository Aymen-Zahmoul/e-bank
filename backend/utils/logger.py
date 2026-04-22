"""
utils/logger.py
Central logging accessor for the ebnk application.
Configuration is set in config/settings.py (LOGGING dict).
Usage:
    from utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Something happened")
"""
import logging


def get_logger(name: str) -> logging.Logger:
    """Return a logger under the 'ebnk' hierarchy."""
    # Normalise: if caller passes __name__ like 'services.auth_service',
    # prefix it so it falls under the configured 'ebnk' logger subtree.
    if not name.startswith("ebnk"):
        name = f"ebnk.{name}"
    return logging.getLogger(name)
