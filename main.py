# cython: language_level=3

from transmeet.processor import transcribe_audio_file, generate_podcast_script_from_transcript, synthesize_podcast_audio, generate_mind_map_from_transcript, segment_speech_by_speaker
import os
import json


if __name__ == "__main__":

    audio_path  = "/home/alpha/Downloads/Mandatory isms awareness training session india.wav"
    transcript = transcribe_audio_file(
        audio_path=audio_path,
    )

    print("Transcription:")
    print(transcript)


    
    # save transcript to file
    # with open("transcript.md", "w") as f:
    #     f.write(transcript)

    # # transcript.md
    # with open("transcript.md", "r") as f:
    #     transcript = f.read()
    
    # # segment conversation by speaker
    # segmented_transcript = segment_speech_by_speaker(
    #     transcript=transcript,
    #     llm_client="groq",
    #     llm_model="llama-3.3-70b-versatile"
    # )

    # print("Segmented Transcript:")
    # # print(segmented_transcript)

    # # save segmented transcript to file
    # with open("segmented_transcript.md", "w") as f:
    #     f.write(segmented_transcript)

    # mind_map_json = generate_mind_map_from_transcript(
    #     transcript=transcript,
    #     llm_client="groq",
    #     llm_model="llama-3.3-70b-versatile"
        
    # )

    # print("Mind Map JSON:")
    # print(mind_map_json)

    # with open("mind_map.json", "w") as f:
    #     json.dump(mind_map_json, f, indent=4)
    

    # # create transcript to podcast text
    # podcast_text = generate_podcast_script_from_transcript(
    #     transcript=transcript,
    #     llm_client="groq",
    #     llm_model="llama-3.3-70b-versatile"
    # )

    # print("Podcast Text:")
    # print(podcast_text)

    # # save podcast text to file
    # with open("podcast.md", "w") as f:
    #     f.write(podcast_text)

    # with open("podcast.md", "r") as f:
    #     podcast_text = f.read()

    # # create podcast audio
    # podcast_audio = synthesize_podcast_audio(
    #     podcast_text=podcast_text,
    #     provider="groq"
    # )

    # print("Podcast Audio:")
    # print(podcast_audio)
