from loguru import logger
import sys
import os

def get_logger(name):
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    
    # Add file handler
    logger.add(
        f"{log_dir}/{name}.log",
        rotation="10 MB",
        retention="1 week",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    
    return logger