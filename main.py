
from transmeet.processor import transcribe_audio_file, generate_podcast_script_from_transcript, synthesize_podcast_audio

if __name__ == "__main__":

    audio_path  = "/home/admin/Downloads/record_audio_09-05-2025_18-49-03.wav"
    transcript = transcribe_audio_file(
        audio_path=audio_path,
    )

    print("Transcription:")
    print(transcript)
    
    # save transcript to file
    with open("transcript.md", "w") as f:
        f.write(transcript)

    # create transcript to podcast text
    podcast_text = generate_podcast_script_from_transcript(
        transcript=transcript,
        podcast_client="groq",
        podcast_model="llama-3.3-70b-versatile"
    )

    print("Podcast Text:")
    print(podcast_text)

    # save podcast text to file
    with open("podcast.md", "w") as f:
        f.write(podcast_text)

    with open("podcast.md", "r") as f:
        podcast_text = f.read()

    # create podcast audio
    podcast_audio = synthesize_podcast_audio(
        podcast_text=podcast_text,
    )

    print("Podcast Audio:")
    print(podcast_audio)
