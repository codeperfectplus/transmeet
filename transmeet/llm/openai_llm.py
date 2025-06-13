from openai import OpenAI
from transmeet.llm.base_llm import BaseLLMClass

class OpenAIClient(BaseLLMClass):
    def get_llm_client(self):
        return OpenAI()

    def generate_response(self, model_name, system_prompt, user_prompt):
        self.notify_observers("input", user_prompt)
        llm = self.get_llm_client()

        response = llm.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )
        content = response.choices[0].message.content
        if content is not None:
            self.notify_observers("output", content)
            return content.strip()
