"""
CrewBot Utilities
"""

import logging
import sys
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    enable_console: bool = True
) -> logging.Logger:
    """
    Setup structured logging for CrewBot
    
    Args:
        level: Logging level
        format_string: Custom format string
        enable_console: Whether to enable console output
        
    Returns:
        Configured root logger
    """
    if format_string is None:
        format_string = (
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )
    
    # Configure root logger
    root_logger = logging.getLogger("crewbot")
    root_logger.setLevel(level)
    
    # Remove existing handlers
    root_logger.handlers = []
    
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        formatter = logging.Formatter(format_string)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    return root_logger


class LoggerMixin:
    """Mixin to add logger to classes"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        return logging.getLogger(self.__class__.__module__ + "." + self.__class__.__name__)
