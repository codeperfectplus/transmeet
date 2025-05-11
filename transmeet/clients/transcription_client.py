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

def transcribe_with_groq(audio_segments, model_name, api_key):
    client = Groq(api_key=api_key)
    full_text = ""

    for idx, chunk in enumerate(audio_segments):
        temp_filename = export_temp_wav(chunk, "groq", idx)
        logger.info(f"Sending chunk {idx + 1}/{len(audio_segments)} to Groq...")

        with open(temp_filename, "rb") as f:
            transcription = client.audio.transcriptions.create(
                file=(temp_filename, f.read()),
                model=model_name,
                response_format="verbose_json",
            )

        delete_file(temp_filename)
        full_text += transcription.text.strip() + " "

    return full_text.strip()

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

# === STANDALONE TEXT FILE HANDLER ===
# def transcribe_with_text_file(text_file_path):
#     try:
#         transcript = Path(text_file_path).read_text(encoding='utf-8')
#         client = Groq(api_key=config["api"]["GROQ_API_KEY"])
#         model = config["api"]["GROQ_MODEL_LLM"]
#         minutes = generate_meeting_minutes(transcript, client, model, "meeting_datetime")
#         MEETING_MINUTES_FILE.write_text(minutes, encoding='utf-8')
#         logger.info(f"Meeting minutes saved to {MEETING_MINUTES_FILE}")
#     except Exception as e:
#         logger.exception("Failed to generate meeting minutes from text file.")

