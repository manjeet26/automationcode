import logging
import os
from datetime import datetime
from pathlib import Path


class LoggerConfig:
    """Configure logging for the test suite"""
    
    @staticmethod
    def setup_logging(test_name: str = "test", log_dir: str = "test-results/logs") -> logging.Logger:
        """
        Set up logging configuration for tests
        
        Args:
            test_name: Name of the test for log file naming
            log_dir: Directory where log files will be stored
            
        Returns:
            Configured logger instance
        """
        # Create log directory if it doesn't exist
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        # Create logger
        logger = logging.getLogger(test_name)
        logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers to avoid duplicates
        logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        # File handler (detailed logs)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"{test_name}_{timestamp}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
        
        # Console handler (simple logs)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)
        
        return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)
