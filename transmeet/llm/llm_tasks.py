from transmeet.utils.json_parser import extract_json_from_text
from transmeet.utils.prompt_loader import load_prompt, format_prompt
from transmeet.llm.llm_manager import LLMManager



def generate_meeting_minutes(llm_client, transcribed_text, model_name, meeting_datetime=None):
    system_prompt = load_prompt("meeting_minutes", "system")
    user_prompt = load_prompt("meeting_minutes", "user") #.replace("{transcribed_text}", transcribed_text).replace("{meeting_datetime}", meeting_datetime or "")
    user_prompt = format_prompt(user_prompt, transcribed_text, meeting_datetime)

    manager = LLMManager(provider=llm_client, model_name=model_name)
    return manager.generate_response(system_prompt=system_prompt, user_prompt=user_prompt)


def segment_conversation_by_speaker(llm_client, transcribed_text, model_name):
    system_prompt = load_prompt("speaker_segmentation", "system")
    user_prompt = load_prompt("speaker_segmentation", "user") #replace("{transcribed_text}", transcribed_text)
    user_prompt = format_prompt(user_prompt, transcribed_text)

    manager = LLMManager(provider=llm_client, model_name=model_name)
    return manager.generate_response(system_prompt=system_prompt, user_prompt=user_prompt)


def create_podcast_dialogue(llm_client, transcribed_text, model_name):
    system_prompt = load_prompt("podcast_script", "system")
    user_prompt = load_prompt("podcast_script", "user")
    user_prompt = format_prompt(user_prompt, transcribed_text)

    manager = LLMManager(provider=llm_client, model_name=model_name)
    return manager.generate_response(system_prompt=system_prompt, user_prompt=user_prompt)


def transform_transcript_to_mind_map(llm_client, transcribed_text, model_name):
    system_prompt = load_prompt("mind_map", "system")
    user_prompt = load_prompt("mind_map", "user").replace("{transcribed_text}", transcribed_text)
    user_prompt = format_prompt(user_prompt, transcribed_text)

    manager = LLMManager(provider=llm_client, model_name=model_name)
    response = manager.generate_response(system_prompt=system_prompt, user_prompt=user_prompt)

    if not response:
        raise ValueError("The LLM did not return a valid response.")

    response = extract_json_from_text(response)
    return response if response else {}
