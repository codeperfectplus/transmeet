import re
import logging
import os
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def extract_datetime_from_filename(filename: str):
    """
    Extracts datetime from filename like 'record_audio_5-9-2025_8-03-59 PM'
    and returns a datetime object.
    """
    match = re.search(r"(\d{1,2}-\d{1,2}-\d{4})_(\d{1,2}-\d{2}-\d{2})\s?(AM|PM)", filename)
    if not match:
        return datetime.now()
    
    date_part, time_part, am_pm = match.groups()
    datetime_str = f"{date_part} {time_part} {am_pm}"    
    return datetime.strptime(datetime_str, "%m-%d-%Y %I-%M-%S %p")

def get_logger(name: str = __name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        log_dir = f"logs/{name}"
        os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(f"{log_dir}/log.txt", mode='a')
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.propagate = False
    logger.debug(f"Logger initialized for {name}")
    return logger
