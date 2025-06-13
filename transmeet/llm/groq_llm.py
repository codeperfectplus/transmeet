from groq import Groq
from transmeet.llm.base_llm import BaseLLMClass

class GroqAIClient(BaseLLMClass):
    def get_llm_client(self):
        return Groq()

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

    def transcribe_audio_file(self, file_path: str, model_name: str) -> str:
        client = self.get_llm_client()
        with open(file_path, "rb") as f:
            response = client.audio.transcriptions.create(
                file=(file_path, f.read()),
                model=model_name,
            )
        self.notify_observers("Output", response.text.strip())
        return response.text.strip()