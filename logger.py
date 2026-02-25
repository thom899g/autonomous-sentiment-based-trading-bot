"""
Robust logging configuration for the trading bot system.
Provides structured logging with proper formatting and error handling.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import json

class StructuredLogger:
    """Enhanced logger with structured JSON output and error handling"""
    
    def __init__(self, name: str, log_level: str = "INFO", log_file: Optional[str] = None):
        """
        Initialize structured logger
        
        Args:
            name: Logger name
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file path for file logging
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Create formatters
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'