from abc import ABC, abstractmethod
from datetime import datetime

class LLMTokenObserver(ABC):
    @abstractmethod
    def notify(self, event_type: str, content: str, timestamp: datetime):
        pass


class BaseLLMClass(ABC):
    def __init__(self):
        self._observers = []

    def attach_observer(self, observer: LLMTokenObserver):
        self._observers.append(observer)

    def notify_observers(self, event_type: str, content: str):
        for observer in self._observers:
            observer.notify(event_type, content, datetime.now())

    @abstractmethod
    def generate_response(self, model_name, system_prompt, user_prompt):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def transcribe_audio_file(self, file_path: str, model_name: str) -> str:
        raise NotImplementedError("Audio transcription not supported by this LLM.")
