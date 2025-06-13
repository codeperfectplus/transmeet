from transmeet.llm.llm_factory import LLMFactory
from transmeet.llm.token_tracker import TokenTracker

class LLMManager:
    def __init__(self, provider: str):
        self.token_tracker = TokenTracker()
        self.llm_client = LLMFactory.get_client(provider)
        self.llm_client.attach_observer(self.token_tracker)

    def generate_response(self, model_name, system_prompt, user_prompt):
        return self.llm_client.generate_response(model_name, system_prompt, user_prompt)

    def get_token_log(self):
        return self.token_tracker.token_log
