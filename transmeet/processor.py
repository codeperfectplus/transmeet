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


def save_meeting_minutes(llm_client, llm_model, transcript: str, meeting_datetime: datetime, meeting_minutes_path: Path, audio_filename: str) -> Path:
    minutes = generate_meeting_minutes(transcript, llm_client, llm_model, meeting_datetime)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = meeting_minutes_path / f"{audio_filename}_minutes_{timestamp}.md"
    path.write_text(minutes, encoding="utf-8")
    logger.info(f"Saved meeting minutes to {path}")
    return path


def generate_meeting_transcript_and_minutes(meeting_audio_file: str, output_dir,
                                            transcription_client="groq",
                                            transcription_model="whisper-large-v3-turbo",
                                            llm_client="groq",
                                            llm_model="llama-3.3-70b-versatile",
                                            audio_chunk_size_mb=18,
                                            audio_chunk_overlap=0.5):
    """
    Generate meeting transcript and minutes from an audio file.

    Args:
        meeting_audio_file (str): Path to the audio file.
        output_dir (str): Directory to save the output files.
        speech_client (str): Speech recognition client to use.
        llm_client (str): LLM client to use for generating meeting minutes.
        transcription_model (str): Model to use for transcription.
        llm_model (str): Model to use for generating meeting minutes.
    """ 
    try:
        if llm_client == "groq":
            llm_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        if llm_client == "openai":
            llm_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if transcription_client == "groq":
            transcription_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        if transcription_client == "openai":
            transcription_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # print llm_client name
        logger.info(f"LLM Client: {llm_client.__class__.__name__}")
        logger.info(f"Transcription Client: {transcription_client.__class__.__name__}")

        logger.info("Starting transcription and meeting minutes generation...")
        logger.debug(f"Audio path: {meeting_audio_file}")
        meeting_audio_filename = Path(meeting_audio_file).stem

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
        transcription_path = output_dir / "transcriptions"
        meeting_minutes_path = output_dir / "meeting_minutes"

        transcription_path.mkdir(parents=True, exist_ok=True)
        meeting_minutes_path.mkdir(parents=True, exist_ok=True)
        
        audio_path = Path(meeting_audio_file)
        
        audio = AudioSegment.from_file(audio_path)
        file_size_mb = get_audio_size_mb(audio)

        transcript = handle_transcription(transcription_client=transcription_client,
                                            transcription_model=transcription_model,
                                            audio=audio,
                                            file_size_mb=file_size_mb,
                                            audio_chunk_size_mb=audio_chunk_size_mb,
                                            audio_chunk_overlap=audio_chunk_overlap)
        save_transcription(transcript, transcription_path, meeting_audio_filename)

        meeting_datetime = extract_datetime_from_filename(audio_path.name)
        save_meeting_minutes(llm_client, llm_model, transcript, meeting_datetime, meeting_minutes_path, meeting_audio_filename)

    except Exception as e:
        logger.exception("❌ Unexpected error during processing.")
