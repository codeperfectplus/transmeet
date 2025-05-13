
from transmeet.processor import generate_meeting_transcript_and_minutes, get_client, segment_conversation_by_speaker,generate_meeting_minutes


# if __name__ == "__main__":

#     audio_path  = "/home/admin/Downloads/record_audio_09-05-2025_18-49-03.wav"
#     transcript, meeting_minutes = generate_meeting_transcript_and_minutes(audio_path,
#                                             transcription_client="openai",
#                                             transcription_model="whisper-1",
#                                             llm_client="openai",
#                                             llm_model="gpt-3.5-turbo",
#     )

#     print("Transcription:")
#     print(transcript)
#     print("\nMeeting Minutes:")
#     print(meeting_minutes)


if __name__ == '__main__':
    # open transcript.txt file
    with open('trasnscript.txt', 'r') as file:
        transcript = file.read()
    # segment_conversation_by_speaker
    llm_client, error = get_client("groq", "llm")
    trasncript = segment_conversation_by_speaker(transcript, llm_client, "llama-3.3-70b-versatile")

    # save transcript to file
    with open('transcript_segmented.txt', 'w') as file:
        file.write(trasncript)

    # generate_meeting_minutes
    meeting_minutes = generate_meeting_minutes(transcript, llm_client, "llama-3.3-70b-versatile", "2025-05-09 18:49:03")

    # save meeting minutes to file
    with open('meeting_minutes.txt', 'w') as file:
        file.write(meeting_minutes)