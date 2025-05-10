# MeetingSummarizer

LLM based meeting summarization


## How to use

Create a `config.conf` file in the root directory with the following content:

```ini
[transcription]
use_groq = true
groq_model = whisper-large-v3-turbo
groq_chunk_target_mb = 18
groq_chunk_overlap = 0.5

[api]
groq_api_key = <YOUR_GROQ_API_KEY>
groq_model_llm = llama-3.3-70b-versatile
```
