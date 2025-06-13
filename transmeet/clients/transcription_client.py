# cython: language_level=3
import math
import time
from collections import deque
from threading import Lock

import speech_recognition as sr
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor, as_completed

from transmeet.llm.llm_manager import LLMManager
from transmeet.utils.file_utils import (
    export_temp_wav,
    delete_file,
)
from transmeet.utils.audio_utils import split_audio_by_target_size
from transmeet.utils.general_utils import get_logger


logger = get_logger(__name__)

MAX_CALLS_PER_MINUTE = 20
TIME_WINDOW = 60  # in seconds
call_times = deque()
rate_lock = Lock()

def wait_for_rate_limit():
    with rate_lock:
        now = time.time()
        # Remove expired timestamps
        while call_times and now - call_times[0] > TIME_WINDOW:
            call_times.popleft()

        if len(call_times) >= MAX_CALLS_PER_MINUTE:
            wait_time = TIME_WINDOW - (now - call_times[0])
            print(f"[RateLimit] Hit 19 calls. Sleeping {wait_time:.2f} seconds...")
            time.sleep(wait_time)
            call_times.popleft()

        call_times.append(time.time())

def rate_limited(func):
    def wrapper(*args, **kwargs):
        wait_for_rate_limit()
        return func(*args, **kwargs)
    return wrapper

@rate_limited
def _transcribe_chunk_safe(chunk, idx, llm_manager: LLMManager):
    try:
        return _transcribe_chunk(chunk, idx, llm_manager)
    except Exception as e:
        logger.exception(f"Failed to transcribe chunk {idx}: {e}")
        return idx, ""

def transcribe_with_llm_calls(audio_segments, llm_manager: LLMManager, max_workers=20):
    """
    Transcribes a list of audio segments using an LLM client in parallel, rate-limited to 19 calls/minute.
    """
    results = [""] * len(audio_segments)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_transcribe_chunk_safe, chunk, idx, llm_manager): idx
            for idx, chunk in enumerate(audio_segments)
        }

        for future in as_completed(futures):
            idx, text = future.result()
            results[idx] = text

    return " ".join(results).strip()

def _transcribe_chunk(chunk, idx, llm_manager: LLMManager):
    temp_filename = export_temp_wav(chunk, "llm", idx)
    logger.info(f"Transcribing chunk {idx + 1} using {llm_manager.provider}...")

    try:
        text = llm_manager.transcribe_audio(temp_filename)
        return idx, text
    finally:
        delete_file(temp_filename)


def process_audio_transcription(
    transcription_client,
    transcription_model: str,
    audio: AudioSegment,
    file_size_mb: float,
    audio_chunk_size_mb: int,
    audio_chunk_overlap: float
) -> str:
    llm_manager = LLMManager(
        provider=transcription_client,
        model_name=transcription_model
    )
    if file_size_mb > audio_chunk_size_mb:
        logger.info(f"Audio file is {file_size_mb:.2f} MB — splitting into chunks.")
        chunks = split_audio_by_target_size(audio, audio_chunk_size_mb, audio_chunk_overlap)
    else:
        logger.info(f"Audio file is within size limit — transcribing directly.")
        chunks = [audio]

    return transcribe_with_llm_calls(chunks, llm_manager)

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
