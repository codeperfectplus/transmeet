from transmeet.llm.llm_factory import LLMFactory
from transmeet.llm.token_tracker import TokenTracker

class LLMManager:
    def __init__(self, provider: str, model_name: str):
        self.provider = provider.lower()
        self.model_name = model_name
        self.token_tracker = TokenTracker(model_name)
        self.llm_client = LLMFactory.get_client(provider)
        self.llm_client.attach_observer(self.token_tracker)

    def generate_response(self, system_prompt, user_prompt):
        return self.llm_client.generate_response(self.model_name, system_prompt, user_prompt)

    def transcribe_audio(self, file_path: str) -> str:
        return self.llm_client.transcribe_audio_file(file_path, self.model_name)