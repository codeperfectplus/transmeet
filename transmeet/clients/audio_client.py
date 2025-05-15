import os
from re import S
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

# === Configuration ===
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OUTPUT_DIR = "podcast_audio"
MAX_WORKERS = 4  # Parallel audio generations

# Generate a unique prefix for this run


# === Voice Mapping ===
VOICE_MAP = {
    "Alex": "Jerry B. - Hyper-Real & Conversational",
    "Jamie": "Zara - Sweet & Gentle Companion"
}

# === Setup ===
os.makedirs(OUTPUT_DIR, exist_ok=True)
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def parse_podcast_script(script_text):
    """
    Parses the podcast script text to extract title and speaker lines.

    Args:
        script_text (str): The full markdown-formatted script content.

    Returns:
        tuple: (title, list of (speaker, line) tuples)
    """
    lines = script_text.strip().splitlines()
    title = ""
    dialogues = []
    recording_script = False

    for i, line in enumerate(lines):
        line = line.strip()

        # Parse title
        if line.startswith("## Podcast Title"):
            if i + 1 < len(lines):
                title = lines[i + 1].strip()
        
        # Begin processing lines only after the "## Podcast Script" header
        elif line.startswith("## Podcast Script"):
            recording_script = True
            continue
        elif line.startswith("## Outro") or line.startswith("## Key Takeaways"):
            recording_script = False

        # Parse dialogues after "## Podcast Script"
        if recording_script and ':' in line:
            speaker, text = line.split(":", 1)
            speaker = speaker.strip()
            text = text.strip()
            if speaker in VOICE_MAP:
                dialogues.append((speaker, text))

    return title, dialogues


def synthesize_speaker_audio(speaker, text, index, SESSION_ID):
    voice = VOICE_MAP.get(speaker)
    if not voice:
        raise ValueError(f"No voice defined for speaker: {speaker}")
    
    filename = os.path.join(OUTPUT_DIR, f"{SESSION_ID}_line_{index:03}_{speaker}.mp3")
    print(f"🔊 Generating [{index:03}] {speaker}: '{text[:60]}...'")

    try:
        audio_stream = client.generate(
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
        print(f"❌ Error generating audio for line {index}: {e}")
        return None


def synthesize_all_dialogues(dialogues, SESSION_ID):
    audio_files = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(synthesize_speaker_audio, speaker, text, i, SESSION_ID): i
            for i, (speaker, text) in enumerate(dialogues)
        }

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


def generate_podcast_audio_file(podcast_script):
    SESSION_ID = uuid.uuid4().hex[:8]
    _, dialogues = parse_podcast_script(podcast_script)
    audio_files = synthesize_all_dialogues(dialogues, SESSION_ID)
    final_output = os.path.join(OUTPUT_DIR, f"{SESSION_ID}_final_podcast.mp3")
    output_file = merge_audio_segments(audio_files, final_output)
    return output_file


if __name__ == "__main__":
    with open('trasnscript.txt', 'r') as file:
        podcast_script = file.read()
    generate_podcast_audio_file(podcast_script)
