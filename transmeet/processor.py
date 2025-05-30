# cython: language_level=3
import os
from pathlib import Path
from datetime import datetime
import configparser
from typing import Tuple, Optional

from pydub import AudioSegment
from groq import Groq
from openai import OpenAI

from transmeet.utils.general_utils import get_logger
from transmeet.utils.audio_utils import get_audio_size_mb, split_audio_by_target_size
from transmeet.clients.llm_client import (
    generate_meeting_minutes,
    create_podcast_dialogue,
    transform_transcript_to_mind_map,
    segment_conversation_by_speaker
)
from transmeet.clients.transcription_client import (
    transcribe_with_llm_calls,
    transcribe_with_google,
)
from transmeet.clients.audio_client import generate_podcast_audio_file


logger = get_logger(__name__)

def load_config(config_path: Path) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def process_audio_transcription(
    transcription_client,
    transcription_model: str,
    audio: AudioSegment,
    file_size_mb: float,
    audio_chunk_size_mb: int,
    audio_chunk_overlap: float
) -> str:
    if transcription_client.__class__.__name__ in {"Groq", "OpenAI"}:
        if file_size_mb > audio_chunk_size_mb:
            logger.info(f"Audio file is {file_size_mb:.2f} MB — splitting into chunks.")
            chunks = split_audio_by_target_size(audio, audio_chunk_size_mb, audio_chunk_overlap)
        else:
            logger.info(f"Audio file is within size limit — transcribing directly.")
            chunks = [audio]

        return transcribe_with_llm_calls(chunks, transcription_model, transcription_client)

    logger.info("Using Google Speech Recognition for transcription.")
    return transcribe_with_google(audio)

def save_transcription(
    transcript: str,
    transcription_path: Path,
    audio_filename: str
) -> Path:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = transcription_path / f"{audio_filename}_transcript_{timestamp}.txt"
    path.write_text(transcript, encoding="utf-8")
    logger.info(f"Transcription saved to {path}")
    return path

def get_client(client_type: str) -> Tuple[Optional[object], Optional[str]]:
    env_var = f"{client_type.upper()}_API_KEY"
    api_key = os.getenv(env_var)

    if not api_key:
        return None, f"Error: {client_type.capitalize()} API key is not set. Please set the {env_var} environment variable."

    client_classes = {
        "groq": Groq,
        "openai": OpenAI,
    }
    
    client_class = client_classes.get(client_type.lower())
    if client_class:
        return client_class(api_key=api_key), None
    return None, f"Error: Unsupported client type: {client_type}"

def transcribe_audio_file(
    audio_path: str,
    llm_client: str = "groq",
    llm_model: str = "whisper-large-v3-turbo",
    audio_chunk_size_mb: int = 18,
    audio_chunk_overlap: float = 0.5
) -> str:
    try:
        client, error = get_client(llm_client)
        if error:
            logger.error(error)
            return error

        logger.info(f"Using transcription client: {client.__class__.__name__}")

        audio_file_path = Path(audio_path)
        audio = AudioSegment.from_file(audio_file_path)
        file_size_mb = get_audio_size_mb(audio)

        transcript = process_audio_transcription(
            transcription_client=client,
            transcription_model=llm_model,
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
    llm_client: str = "groq",
    llm_model: str = "llama-3.3-70b-versatile"
) -> str:
    try:
        client, error = get_client(llm_client)
        if error:
            logger.error(error)
            return error

        logger.info(f"Using LLM client: {client.__class__.__name__} for meeting minutes generation.")
        return generate_meeting_minutes(transcript, client, llm_model)

    except Exception as e:
        logger.error(f"Error generating meeting minutes: {e}", exc_info=True)
        return f"Error: {e}"

def generate_mind_map_from_transcript(
    transcript: str,
    llm_client: str = "groq",
    llm_model: str = "llama-3.3-70b-versatile"
):
    client, error = get_client(llm_client)
    if error:
        logger.error(error)
        return error

    logger.info(f"Using LLM client: {client.__class__.__name__} for mind map generation.")
    return transform_transcript_to_mind_map(transcript, client, llm_model)

def generate_podcast_script_from_transcript(
    transcript: str,
    llm_client: str = "groq",
    llm_model: str = "llama-3.3-70b-versatile"
) -> str:
    try:
        client, error = get_client(llm_client)
        if error:
            logger.error(error)
            return error

        logger.info(f"Using LLM client: {client.__class__.__name__} for podcast script generation.")
        return create_podcast_dialogue(transcript, client, llm_model)

    except Exception as e:
        logger.error(f"Error generating podcast script: {e}", exc_info=True)
        return f"Error: {e}"

def synthesize_podcast_audio(podcast_text: str, provider: str = "groq") -> str:
    try:
        return generate_podcast_audio_file(podcast_text, provider)
    except Exception as e:
        logger.error(f"Error generating podcast audio: {e}", exc_info=True)
        return f"Error: {e}"


# segment_conversation_by_speaker
def segment_speech_by_speaker(
    transcript: str,
    llm_client: str = "groq",
    llm_model: str = "llama-3.3-70b-versatile"
) -> str:
    try:
        client, error = get_client(llm_client)
        if error:
            logger.error(error)
            return error
        logger.info(f"Using LLM client: {client.__class__.__name__} for speaker segmentation.")
        return segment_conversation_by_speaker(transcript, client, llm_model)
    except Exception as e:
        logger.error(f"Error segmenting speech by speaker: {e}", exc_info=True)
        return f"Error: {e}"
