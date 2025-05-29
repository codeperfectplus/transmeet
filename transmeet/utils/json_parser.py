# cython: language_level=3
import json
import re
from typing import Dict, Any


def remove_think_tags(text: str) -> str:
    """
    Remove <think>...</think> tags from LLM responses.
    """
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)


def find_first_json_block(text: str) -> str:
    """
    Extract the first valid JSON object from a string using brace counting.
    """
    start = text.find('{')
    if start == -1:
        return ""
    
    brace_count = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                return text[start:i+1]
    
    return ""


def sanitize_json_text(text: str) -> str:
    """
    Clean up a JSON-like string:
    - Normalize special characters
    - Remove emojis
    - Fix newlines inside string values
    - Remove trailing commas
    """
    # Normalize special punctuation
    text = re.sub(r'[\r“”‘’]', '', text)

    # Remove emojis (basic unicode emoji range)
    text = re.sub(r'[\U0001F600-\U0001F64F]', '', text)

    # Remove newlines inside quoted strings (naive but helpful)
    text = re.sub(r'"\s*([^"]*?)\s*"', lambda m: '"' + m.group(1).replace('\n', ' ') + '"', text)

    # Remove trailing commas before closing braces/brackets
    text = re.sub(r',\s*([}\]])', r'\1', text)

    return text


def unwrap_json_string(text: str) -> str:
    """
    Remove surrounding quotes and unescape double-encoded strings if necessary.
    """
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
        text = text.encode().decode('unicode_escape')
    return text


def extract_json_from_text(text: str) -> Dict[str, Any]:
    """
    Extract and parse the first JSON object from a mixed LLM response.
    Returns a Python dictionary or an empty dict if parsing fails.
    """
    cleaned_text = remove_think_tags(text)
    json_str = find_first_json_block(cleaned_text)

    if not json_str:
        return {}

    # Remove code block markers (e.g., ```json)
    json_str = re.sub(r'^`+json|`+$', '', json_str).strip('`').strip()

    # Unescape if it's a JSON string literal
    json_str = unwrap_json_string(json_str)

    # Final cleanup before parsing
    json_str = sanitize_json_text(json_str)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}") 
        return {}
