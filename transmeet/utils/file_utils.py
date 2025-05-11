import os
from pathlib import Path

def delete_file(path):
    file = Path(path)
    if file.exists():
        file.unlink()

def export_temp_wav(chunk, prefix, index):
    filename = f"{prefix}_chunk_{index}.wav"
    chunk.export(filename, format="wav")
    return filename
