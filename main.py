
from transmeet import generate_meeting_transcript_and_minutes


if __name__ == "__main__":

    audio_path  = "/home/admin/Downloads/record_audio_09-05-2025_18-49-03.wav"
    transcript, meeting_minutes = generate_meeting_transcript_and_minutes(audio_path,
                                            transcription_client="openai",
                                            transcription_model="whisper-1",
                                            llm_client="openai",
                                            llm_model="gpt-3.5-turbo",
    )

    print("Transcription:")
    print(transcript)
    print("\nMeeting Minutes:")
    print(meeting_minutes)



# [transcription]
# speech_service = groq
# groq_model = whisper-large-v3-turbo
# groq_chunk_target_mb = 18
# groq_chunk_overlap = 0.5

# [api]
# groq_model_llm = llama-3.3-70b-versatile
