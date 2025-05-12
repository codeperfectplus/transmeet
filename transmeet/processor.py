import argparse
import os
from pathlib import Path
from datetime import datetime
import configparser
from pydub import AudioSegment
from groq import Groq
from openai import OpenAI

from transmeet.utils.general_utils import (
    extract_datetime_from_filename,
    get_logger,
    ROOT_DIR,
)

from transmeet.utils.audio_utils import (
    get_audio_size_mb,
    split_audio_by_target_size,
)

from transmeet.clients.llm_client import generate_meeting_minutes
from transmeet.clients.transcription_client import transcribe_with_groq, transcribe_with_google

logger = get_logger(__name__)


def load_config(config_path: Path) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def handle_transcription(transcription_client, transcription_model, 
                         audio: AudioSegment, 
                         file_size_mb: float,
                        audio_chunk_size_mb: int,
                        audio_chunk_overlap: float) -> str:
    
    if transcription_client.__class__.__name__ in ["Groq", "OpenAI"]:
        if file_size_mb > audio_chunk_size_mb:
            logger.info(f"File is {file_size_mb:.2f} MB — splitting into chunks...")
            chunks = split_audio_by_target_size(audio, audio_chunk_size_mb, audio_chunk_overlap)
        else:
            chunks = [audio]
            logger.info("Audio is small enough — using Groq directly...")

        return transcribe_with_groq(chunks, transcription_model, transcription_client)

    logger.info("Using Google Speech Recognition...")
    return transcribe_with_google(audio)


def save_transcription(transcript: str, transcription_path: Path, audio_filename: str) -> Path:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = transcription_path / f"{audio_filename}_transcript_{timestamp}.txt"
    path.write_text(transcript, encoding="utf-8")
    logger.info(f"Saved transcription to {path}")
    return path

def get_client(client_type: str, service_name: str):
    """
    Returns an initialized client or an error message if missing.
    """
    env_var = f"{client_type.upper()}_API_KEY"
    api_key = os.getenv(env_var)

    if not api_key:
        return None, f"Error: {client_type.capitalize()} API key is not set, export {env_var} in your environment."

    if client_type == "groq":
        return Groq(api_key=api_key), None
    elif client_type == "openai":
        return OpenAI(api_key=api_key), None
    else:
        return None, f"Error: Unsupported {service_name} client: {client_type}"


def generate_meeting_transcript_and_minutes(
    meeting_audio_file: str,
    transcription_service="groq",
    transcription_model="whisper-large-v3-turbo",
    llm_client="groq",
    llm_model="llama-3.3-70b-versatile",
    audio_chunk_size_mb=18,
    audio_chunk_overlap=0.5
):
    """
    Generate meeting transcript and minutes from an audio file.
    """
    try:
        # Initialize transcription client
        transcription_service, error = get_client(transcription_service, "transcription")
        if error:
            logger.error(error)
            return error, "No meeting minutes generated."

        # Initialize LLM client
        llm_service, error = get_client(llm_client, "llm")
        if error:
            logger.error(error)
            return error, "No meeting minutes generated."

        logger.info(f"LLM Client: {llm_service.__class__.__name__}")
        logger.info(f"Transcription Client: {transcription_service.__class__.__name__}")
        logger.debug(f"Audio file path: {meeting_audio_file}")

        # Load and analyze audio
        audio_path = Path(meeting_audio_file)
        meeting_datetime = extract_datetime_from_filename(audio_path.name)
        audio = AudioSegment.from_file(audio_path)
        file_size_mb = get_audio_size_mb(audio)

        # Transcribe
        transcript = handle_transcription(
            transcription_client=transcription_service,
            transcription_model=transcription_model,
            audio=audio,
            file_size_mb=file_size_mb,
            audio_chunk_size_mb=audio_chunk_size_mb,
            audio_chunk_overlap=audio_chunk_overlap
        )

        # Generate minutes
        meeting_minutes = generate_meeting_minutes(transcript, llm_service, llm_model, meeting_datetime)

        return transcript, meeting_minutes

    except Exception as e:
        logger.error(f"Processing failed: {e}", exc_info=True)
        return f"Error: {e}", "No meeting minutes generated."
