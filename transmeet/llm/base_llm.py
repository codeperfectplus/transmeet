from abc import ABC, abstractmethod

class BaseLLMClass(ABC):
    @abstractmethod
    def generate_response(self, model_name, system_prompt, user_prompt):
        """
        Generate a response using the LLM API.

        :param model_name: The name of the model to use.
        :param system_prompt: The system prompt to set the context.
        :param user_prompt: The user's input for which a response is generated.
        :return: The generated response from the model.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
