import os
from pathlib import Path
from datetime import datetime
import configparser
from pydub import AudioSegment
from typing import Tuple, Optional
from groq import Groq
from openai import OpenAI

from transmeet.utils.general_utils import (
    get_logger,
)

from transmeet.utils.audio_utils import (
    get_audio_size_mb,
    split_audio_by_target_size,
)

from transmeet.clients.llm_client import generate_meeting_minutes, create_podcast_dialogue
from transmeet.clients.transcription_client import transcribe_with_llm_calls, transcribe_with_google
from transmeet.clients.audio_client import generate_podcast_audio_file

logger = get_logger(__name__)

def load_config(config_path: Path) -> configparser.ConfigParser:
    """
    Load and return the configuration file.
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def process_audio_transcription(
    transcription_client,
    transcription_model: str, 
    audio: AudioSegment, 
    file_size_mb: float,
    audio_chunk_size_mb: int,
    audio_chunk_overlap: float) -> str:
    """
    Handle the transcription process, splitting audio if necessary.
    """
    if transcription_client.__class__.__name__ in ["Groq", "OpenAI"]:
        if file_size_mb > audio_chunk_size_mb:
            logger.info(f"Audio file is {file_size_mb:.2f} MB — splitting into chunks.")
            chunks = split_audio_by_target_size(audio, audio_chunk_size_mb, audio_chunk_overlap)
        else:
            chunks = [audio]
            logger.info(f"Audio file is small enough for transcription with {transcription_client.__class__.__name__}.")
        
        return transcribe_with_llm_calls(chunks, transcription_model, transcription_client)

    logger.info("Using Google Speech Recognition for transcription.")
    return transcribe_with_google(audio)


def save_transcription(
    transcript: str, 
    transcription_path: Path, 
    audio_filename: str) -> Path:
    """
    Save the transcription text to a file.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = transcription_path / f"{audio_filename}_transcript_{timestamp}.txt"
    path.write_text(transcript, encoding="utf-8")
    logger.info(f"Transcription saved to {path}")
    return path


def get_client(client_type: str) -> Tuple[Optional[object], Optional[str]]:
    """
    Get the appropriate client based on the client type (Groq, OpenAI, etc.).
    """
    env_var = f"{client_type.upper()}_API_KEY"
    api_key = os.getenv(env_var)

    if not api_key:
        return None, f"Error: {client_type.capitalize()} API key is not set. Please set the {env_var} environment variable."

    if client_type == "groq":
        return Groq(api_key=api_key), None
    elif client_type == "openai":
        return OpenAI(api_key=api_key), None
    return None, f"Error: Unsupported client type: {client_type}"

def transcribe_audio_file(
    audio_path: str,
    transcription_client="groq",
    transcription_model="whisper-large-v3-turbo",
    audio_chunk_size_mb=18,
    audio_chunk_overlap=0.5) -> str:
    """
    Convert an audio file to a transcript using the specified client and model.
    """
    try:
        # Initialize the transcription client
        transcription_client, error = get_client(transcription_client)
        if error:
            logger.error(error)
            return error

        logger.info(f"Using transcription client: {transcription_client.__class__.__name__}")
        logger.debug(f"Processing audio file: {audio_path}")

        # Load and analyze the audio file
        audio_path = Path(audio_path) # type: ignore
        audio = AudioSegment.from_file(audio_path)
        file_size_mb = get_audio_size_mb(audio)

        # Perform transcription
        transcript = process_audio_transcription(
            transcription_client=transcription_client,
            transcription_model=transcription_model,
            audio=audio,
            file_size_mb=file_size_mb,
            audio_chunk_size_mb=audio_chunk_size_mb,
            audio_chunk_overlap=audio_chunk_overlap
        )
        return transcript
    
    except Exception as e:
        logger.error(f"Error processing audio file {audio_path}: {e}", exc_info=True)
        return f"Error: {e}"


def generate_meeting_minutes_from_transcript(
    transcript: str,
    llm_client="groq",
    llm_model="llama-3.3-70b-versatile") -> str:
    """
    Generate meeting minutes from the transcript using the specified client and model.
    """
    try:
        # Initialize the LLM client
        llm_client, error = get_client(llm_client)
        if error:
            logger.error(error)
            return error

        logger.info(f"Using LLM client: {llm_client.__class__.__name__}")
        logger.debug(f"Generating meeting minutes from transcript.")

        # Generate meeting minutes
        meeting_minutes = generate_meeting_minutes(transcript, llm_client, llm_model)

        return meeting_minutes
    except Exception as e:
        logger.error(f"Error generating meeting minutes: {e}", exc_info=True)
        return f"Error: {e}"


def generate_podcast_script_from_transcript(
    transcript: str,
    podcast_client="groq",
    podcast_model="llama-3.3-70b-versatile") -> str:
    """
    Generate a podcast from the transcript using the specified client and model.
    """
    try:
        # Initialize the podcast client
        podcast_client, error = get_client(podcast_client)
        if error:
            logger.error(error)
            return error

        logger.info(f"Using podcast client: {podcast_client.__class__.__name__}")
        logger.debug(f"Generating podcast from transcript.")

        # Generate the podcast
        podcast_text = create_podcast_dialogue(transcript, podcast_client, podcast_model)

        return podcast_text
    except Exception as e:
        logger.error(f"Error generating podcast: {e}", exc_info=True)
        return f"Error: {e}"

def synthesize_podcast_audio(
    podcast_text: str
):
    """
    Generate a podcast audio file from the podcast text using the specified client and model.
    """
    try:
        auiod_path = generate_podcast_audio_file(podcast_text)
        return auiod_path
    except Exception as e:
        logger.error(f"Error generating podcast audio: {e}", exc_info=True)
        return f"Error: {e}"
        