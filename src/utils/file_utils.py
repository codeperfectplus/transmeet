import os
from pathlib import Path

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


def export_temp_wav(chunk, prefix, index):
    filename = f"{prefix}_chunk_{index}.wav"
    chunk.export(filename, format="wav")
    return filename
