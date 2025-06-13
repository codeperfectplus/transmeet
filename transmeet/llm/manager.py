from transmeet.llm.openai_llm import OpenAIClient
from transmeet.llm.groq_llm import GroqAIClient

class LLMManager:
    def __init__(self, provider: str):
        """
        Initialize the LLMManager with the specified provider.

        :param provider: The name of the LLM provider (e.g., 'openai', 'groq').
        """
        self.provider = provider.lower()
        self.llm_client = self._get_llm_client()

    def _get_llm_client(self):
        """
        Get the appropriate LLM client based on the provider.

        :return: An instance of the LLM client.
        """
        # NOTE: Factory method to create the appropriate LLM client
        if self.provider == 'openai':
            return OpenAIClient()
        elif self.provider == 'groq':
            return GroqAIClient()
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def generate(self, model_name, system_prompt, user_prompt):
        """
        Generate a response using the specified model and prompts.

        :param model_name: The name of the model to use.
        :param system_prompt: The system prompt to set the context.
        :param user_prompt: The user's input for which a response is generated.
        :return: The generated response from the model.
        """
        return self.llm_client.generate(model_name, system_prompt, user_prompt)