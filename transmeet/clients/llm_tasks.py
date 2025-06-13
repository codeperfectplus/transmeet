from transmeet.utils.json_parser import extract_json_from_text
from transmeet.utils.prompt_loader import load_prompt
from transmeet.llm.manager import LLMManager


def generate_meeting_minutes(llm_client, transcribed_text, model_name, meeting_datetime=None):
    system_prompt = load_prompt("meeting_minutes", "system")
    user_prompt = load_prompt("meeting_minutes", "user").replace("{transcribed_text}", transcribed_text).replace("{meeting_datetime}", meeting_datetime or "")

    manager = LLMManager(provider=llm_client)
    return manager.generate_response(model_name=model_name, system_prompt=system_prompt, user_prompt=user_prompt)


def segment_conversation_by_speaker(llm_client, transcribed_text, model_name):
    system_prompt = load_prompt("speaker_segmentation", "system")
    user_prompt = load_prompt("speaker_segmentation", "user").replace("{transcribed_text}", transcribed_text)

    manager = LLMManager(provider=llm_client)
    return manager.generate_response(model_name=model_name, system_prompt=system_prompt, user_prompt=user_prompt)


def create_podcast_dialogue(llm_client, transcribed_text, model_name):
    system_prompt = load_prompt("podcast_script", "system")
    user_prompt = load_prompt("podcast_script", "user").replace("{transcribed_text}", transcribed_text)

    manager = LLMManager(provider=llm_client)
    return manager.generate_response(model_name=model_name, system_prompt=system_prompt, user_prompt=user_prompt)


def transform_transcript_to_mind_map(llm_client, transcribed_text, model_name):
    system_prompt = load_prompt("mind_map", "system")
    user_prompt = load_prompt("mind_map", "user").replace("{transcribed_text}", transcribed_text)

    manager = LLMManager(provider=llm_client)
    response = manager.generate_response(model_name=model_name, system_prompt=system_prompt, user_prompt=user_prompt)

    if not response:
        raise ValueError("The LLM did not return a valid response.")

    response = extract_json_from_text(response)
    return response if response else {}
