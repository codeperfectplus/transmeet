# cython: language_level=3
import os
import uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
from groq import Groq

# === Configuration ===
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OUTPUT_DIR = "podcast_audio"
MAX_WORKERS = 2  # Parallel audio generations
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Voice Mapping ===
VOICE_MAP = {
    "Jerry": {
        "elevenlabs": "Jerry B. - Hyper-Real & Conversational",
        "groq": "Fritz-PlayAI"  # You can change this based on Groq-supported voices
    },
    "Christina": {
        "elevenlabs": "Christina - Natural & Conversational",
        "groq": "Aaliyah-PlayAI"
    }
}

# === Clients ===
eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
groq_client = Groq()


def parse_podcast_script(script_text):
    lines = script_text.strip().splitlines()
    title = ""
    dialogues = []
    recording_script = False

    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("## Podcast Title") and i + 1 < len(lines):
            title = lines[i + 1].strip()
        elif line.startswith("## Podcast Script"):
            recording_script = True
            continue
        elif line.startswith("## Outro") or line.startswith("## Key Takeaways"):
            recording_script = False

        if recording_script and ':' in line:
            speaker, text = line.split(":", 1)
            speaker, text = speaker.strip(), text.strip()
            if speaker in VOICE_MAP:
                dialogues.append((speaker, text))

    return title, dialogues


def synthesize_with_elevenlabs(speaker, text, index, session_id):
    voice = VOICE_MAP[speaker]["elevenlabs"]
    filename = os.path.join(OUTPUT_DIR, f"{session_id}_line_{index:03}_{speaker}.mp3")
    print(f"🔊 [ElevenLabs] Generating [{index:03}] {speaker}: '{text[:60]}...'")

    try:
        audio_stream = eleven_client.generate(
            text=text,
            voice=voice,
            model="eleven_multilingual_v2",
            stream=True
        )
        with open(filename, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
        return filename
    except Exception as e:
        print(f"❌ Error generating with ElevenLabs for line {index}: {e}")
        return None


def synthesize_with_groq(speaker, text, index, session_id):
    voice = VOICE_MAP[speaker]["groq"]
    filename = os.path.join(OUTPUT_DIR, f"{session_id}_line_{index:03}_{speaker}.wav")
    print(f"🔊 [Groq] Generating [{index:03}] {speaker}: '{text[:60]}...'")

    try:
        response = groq_client.audio.speech.create(
            model="playai-tts",
            voice=voice,
            response_format="wav",
            input=text
        )

        with open(filename, "wb") as f:
            f.write(response.content)

        return filename

    except Exception as e:
        print(f"❌ Error generating with Groq for line {index}: {e}")
        return None



def synthesize_all_dialogues(dialogues, session_id, provider):
    audio_files = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for i, (speaker, text) in enumerate(dialogues):
            if provider == "elevenlabs":
                func = synthesize_with_elevenlabs
            elif provider == "groq":
                func = synthesize_with_groq
            else:
                raise ValueError(f"Unknown provider: {provider}")

            futures[executor.submit(func, speaker, text, i, session_id)] = i

        for future in as_completed(futures):
            result = future.result()
            if result:
                audio_files.append(result)

    audio_files.sort()
    return audio_files


def merge_audio_segments(files, output_file):
    print("🎧 Combining all audio files...")
    combined = AudioSegment.empty()

    for file in files:
        try:
            audio = AudioSegment.from_file(file)
            combined += audio + AudioSegment.silent(duration=500)
        except Exception as e:
            print(f"⚠️ Skipping file {file}: {e}")

    combined.export(output_file, format="mp3")
    return output_file


def generate_podcast_audio_file(podcast_script, provider="elevenlabs"):
    session_id = uuid.uuid4().hex[:8]
    _, dialogues = parse_podcast_script(podcast_script)
    audio_files = synthesize_all_dialogues(dialogues, session_id, provider)
    final_output = os.path.join(OUTPUT_DIR, f"{session_id}_final_podcast.mp3")
    return merge_audio_segments(audio_files, final_output)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--provider", choices=["elevenlabs", "groq"], default="elevenlabs", help="Choose the TTS provider.")
    parser.add_argument("--script", default="trasnscript.txt", help="Path to the podcast transcript file.")

    args = parser.parse_args()

    with open(args.script, 'r') as file:
        podcast_script = file.read()

    output = generate_podcast_audio_file(podcast_script, provider=args.provider)
    print(f"\n✅ Podcast generated: {output}")
