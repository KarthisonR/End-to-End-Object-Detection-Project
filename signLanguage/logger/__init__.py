import logging
import os
from datetime import datetime
from from_root import from_root

# Define your specific directory for logs
SPECIFIC_LOG_DIR = 'D:\Temp\End-to-End-Object-Detection-Project'

# Get the log file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Use from_root() and override with your specific directory
LOG_DIR = os.path.join(SPECIFIC_LOG_DIR, 'log')
os.makedirs(LOG_DIR, exist_ok=True)

# Full path for the log file
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler()  # Also output logs to console
    ]
)
