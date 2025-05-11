import argparse
import sys
from transmeet import generate_meeting_transcript_and_minutes


def main():
    parser = argparse.ArgumentParser(
        description="🎤 TransMeet: Transcribe audio and generate meeting minutes using Groq or Google."
    )
    parser.add_argument(
        "-i", "--audio-path", required=True,
        help="Path to the audio file (.wav, .mp3, etc.)"
    )
    parser.add_argument(
        "-o", "--output-dir", default="output",
        help="Directory where output (transcript + minutes) will be saved"
    )
  

    args = parser.parse_args()

    try:
        generate_meeting_transcript_and_minutes(
            meeting_audio_file=args.audio_path,
            output_dir=args.output_dir,
        )
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
