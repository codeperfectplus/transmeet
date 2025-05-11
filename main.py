
import argparse
from transmeet import generate_meeting_transcript_and_minutes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio and generate meeting minutes.")
    parser.add_argument("--audio-path", required=True, help="Path to the audio file.")
    args = parser.parse_args()
    generate_meeting_transcript_and_minutes(args.audio_path, output_dir="output")
