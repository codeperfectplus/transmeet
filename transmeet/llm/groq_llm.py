from groq import Groq

from transmeet.llm.base_llm import BaseLLMClass

class GroqAIClient(BaseLLMClass):

    def get_llm_client(self):
        """
        Get the OpenAI client instance.

        :return: An instance of the OpenAI client.
        """
        llm_client = Groq()
        return llm_client
    
    def generate_response(self, model_name, system_prompt, user_prompt):
        """
        Generate a response using the OpenAI API.

        :param model_name: The name of the model to use.
        :param system_prompt: The system prompt to set the context.
        :param user_prompt: The user's input for which a response is generated.
        :return: The generated response from the model.
        """
        llm_client = self.get_llm_client()
        response = llm_client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        if response:
            content = response.choices[0].message.content
            return content.strip() if content else None