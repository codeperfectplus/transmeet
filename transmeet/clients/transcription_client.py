import math
from venv import logger
from groq import Groq
import speech_recognition as sr


from transmeet.utils.file_utils import (
    export_temp_wav,
    delete_file,
)

from transmeet.utils.general_utils import get_logger

logger = get_logger(__name__)

from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)


def transcribe_with_llm_calls(audio_segments, model_name, client, max_workers=4):
    """
    Transcribes a list of audio segments using an LLM client in parallel.
    """
    results = [""] * len(audio_segments)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_transcribe_chunk_safe, chunk, idx, model_name, client): idx
            for idx, chunk in enumerate(audio_segments)
        }

        for future in as_completed(futures):
            idx, text = future.result()
            results[idx] = text

    return " ".join(results).strip()


def _transcribe_chunk_safe(chunk, idx, model_name, client):
    """
    Wraps the transcription call with error handling and logging.
    """
    try:
        return _transcribe_chunk(chunk, idx, model_name, client)
    except Exception as e:
        logger.exception(f"Failed to transcribe chunk {idx}: {e}")
        return idx, ""


def _transcribe_chunk(chunk, idx, model_name, client):
    """
    Handles exporting, sending the transcription request, and cleanup.
    """
    temp_filename = export_temp_wav(chunk, "groq", idx)
    logger.info(
        f"Transcribing chunk {idx + 1} using {client.__class__.__name__} and model '{model_name}'..."
    )

    try:
        with open(temp_filename, "rb") as f:
            response = client.audio.transcriptions.create(
                file=(temp_filename, f.read()),
                model=model_name,
            )
        return idx, response.text.strip()
    finally:
        delete_file(temp_filename)


def transcribe_with_google(audio, chunk_length_ms=60_000):
    recognizer = sr.Recognizer()
    full_text = ""
    num_chunks = math.ceil(len(audio) / chunk_length_ms)

    for i in range(num_chunks):
        start, end = i * chunk_length_ms, min((i + 1) * chunk_length_ms, len(audio))
        chunk = audio[start:end]
        temp_filename = export_temp_wav(chunk, "google", i)
        logger.info(f"Transcribing {temp_filename} with Google...")

        with sr.AudioFile(temp_filename) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data) # type: ignore
                full_text += text + " "
            except sr.UnknownValueError:
                logger.warning(f"Could not understand audio in {temp_filename}")
            except sr.RequestError as e:
                logger.error(f"Google request error: {e}")

        delete_file(temp_filename)

    return full_text.strip()
