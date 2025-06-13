from transmeet.llm.base_llm import LLMTokenObserver
from datetime import datetime

class TokenTracker(LLMTokenObserver):
    def __init__(self):
        self.token_log = []

    def notify(self, event_type: str, content: str, timestamp: datetime):
        tokens = len(content.split())
        self.token_log.append({
            "event": event_type,
            "tokens": tokens,
            "timestamp": timestamp,
        })
        print(f"[{timestamp}] {event_type.upper()} - Tokens: {tokens}")
