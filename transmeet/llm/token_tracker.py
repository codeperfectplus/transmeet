import tiktoken
from transmeet.llm.base_llm import LLMTokenObserver
from datetime import datetime

class TokenTracker(LLMTokenObserver):
    def __init__(self, model_name: str = "gpt-4"):
        """
        Initialize with the model to ensure accurate token encoding.
        """
        self.token_log = []
        self.model_name = model_name
        try:
            self.encoder = tiktoken.encoding_for_model(model_name)
        except KeyError:
            print(f"[WARN] Model '{model_name}' not supported. Falling back to 'cl100k_base'.")
            self.encoder = tiktoken.get_encoding("cl100k_base")
            
    def count_tokens(self, text: str) -> int:
        return len(self.encoder.encode(text))

    def notify(self, event_type: str, content: str, timestamp: datetime):
        tokens = self.count_tokens(content)
        log_entry = {
            "event": event_type,
            "tokens": tokens,
            "timestamp": timestamp,
            "preview": content[:60].replace('\n', ' ') + ("..." if len(content) > 60 else "")
        }
        self.token_log.append(log_entry)
        print(f"[{timestamp}] {event_type.upper():<6} | Tokens: {tokens:>4} | {log_entry['preview']}")
