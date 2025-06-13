import os

def load_prompt(task_name, prompt_type):
    """
    Load prompt from a given task and type (system/user).
    Example: load_prompt("meeting_minutes", "system")
    """
    base_path = os.path.join(os.path.dirname(__file__), "..", "prompts")
    file_path = os.path.join(base_path, task_name, f"{prompt_type}.md")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Prompt file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def format_prompt(prompt, *args):
    for i, arg in enumerate(args):
        placeholder = f"{{arg{i}}}"
        prompt = prompt.replace(placeholder, str(arg))
    return prompt
