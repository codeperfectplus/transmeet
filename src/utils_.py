import re
import logging
import os
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
print(f"ROOT_DIR: {ROOT_DIR}")

def extract_datetime_from_filename(filename: str):
    """
    Extracts datetime from filename like 'record_audio_5-9-2025_8-03-59 PM'
    and returns a datetime object.
    """
    # Use regex to find the date and time portion
    match = re.search(r"(\d{1,2}-\d{1,2}-\d{4})_(\d{1,2}-\d{2}-\d{2})\s?(AM|PM)", filename)
    if not match:
        return datetime.now()  # Default to now if no match found
    
    date_part, time_part, am_pm = match.groups()
    datetime_str = f"{date_part} {time_part} {am_pm}"    
    return datetime.strptime(datetime_str, "%m-%d-%Y %I-%M-%S %p")

def get_audio_size_mb(audio_segment):
    return len(audio_segment.raw_data) / (1024 * 1024)

def export_temp_wav(chunk, prefix, index):
    filename = f"{prefix}_chunk_{index}.wav"
    chunk.export(filename, format="wav")
    return filename

def delete_file(path):
    file = Path(path)
    if file.exists():
        file.unlink()

def validate_config(config):
    audio_path = Path(config["transcription"]["audio_path"])
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    if not config["api"].get("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY is missing in config.")
    return audio_path

def split_audio_by_target_size(audio, target_mb):
    """Split audio into chunks of approx. target MB without exceeding max size."""
    # Convert target size and max size to bytes
    target_bytes = target_mb * 1024 * 1024
    
    # Get the total duration of the audio in milliseconds
    total_duration_ms = len(audio)
    
    # Calculate the duration (in ms) of a chunk that corresponds to the target size in MB
    chunk_duration_ms = (target_bytes / len(audio.raw_data)) * total_duration_ms
    
    print(f"Chunk duration (ms): {chunk_duration_ms}")

    # Prepare the list of chunks
    chunks = []
    start = 0
    while start < total_duration_ms:
        # Determine the end of the chunk based on the calculated duration
        end = min(start + int(chunk_duration_ms), total_duration_ms)
        chunk = audio[start:end]
        
        # Ensure that the chunk does not exceed max size
        while len(chunk.raw_data) > target_bytes:
            end -= 1  # Adjust end point if chunk size exceeds max size
            chunk = audio[start:end]

        chunks.append(chunk)
        start = end

    return chunks

def get_logger(name: str = __name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent adding multiple handlers to the same logger
    if not logger.handlers:
        log_dir = f"logs/{name}"
        os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(f"{log_dir}/log.txt", mode='a')
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
