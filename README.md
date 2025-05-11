# 🎙️ TransMeet — AI-Powered Meeting Summarizer

> **Turn your meeting recordings into clear, structured minutes using LLMs like Groq Whisper and Google Speech Recognition.**

---

## 🚀 Features

* ✅ **Audio Transcription** — Automatically convert `.wav` or `.mp3` files into text
* 🧠 **LLM-Powered Summarization** — Generate concise and structured meeting minutes
* 🔍 **Groq & Google Support** — Choose between Groq Whisper models or Google Speech API
* 🪓 **Automatic Chunking** — Splits large files intelligently for smoother transcription
* ⚙️ **Fully Customizable** — Pick your preferred transcription and summarization models
* 🧾 **CLI & Python API** — Use it from the terminal or integrate in your Python workflows
* 📁 **Clean Output** — Saves transcripts and summaries neatly in your desired folder

---

## 📦 Installation

```bash
pip install transmeet
````

---

## 🔐 Setup

Set your **GROQ API Key**/**OPENAI API Key** in your environment variables.

```bash
export GROQ_API_KEY=your_groq_api_key
```

To make this permanent:

```bash
echo 'export GROQ_API_KEY=your_groq_api_key' >> ~/.bashrc
```

> If using OPENAI, set the `OPENAI_API_KEY` similarly.
> For Google Speech, no API key is needed; it uses the default model.

---

## 🧑‍💻 How to Use

### ✅ Option 1: Import as a Python Module

```python
from transmeet import generate_meeting_transcript_and_minutes

generate_meeting_transcript_and_minutes(
    meeting_audio_file="/path/to/audio.wav",
    output_dir="complete_path_to_output_dir/",
    transcription_client="groq",  # or "openai"
    transcription_model="whisper-large-v3-turbo", # change as per your need
    llm_client="groq",  # or "openai"
    llm_model="llama-3.3-70b-versatile", # change as per your need
)
```

This will save two files in your output directory:

* `transcription_<timestamp>.txt`
* `meeting_minutes_<timestamp>.md`

---

### 🔧 Option 2: Use the CLI

#### 🔹 Basic Usage (Default: GROQ)

```bash
transmeet -i /path/to/audio.wav -o output/
```

#### 🔸 Advanced Usage

```bash
transmeet \
  -i /path/to/audio.wav \
  -o output/ \
  --transcription-client groq \
  --transcription-model whisper-large-v3-turbo \
  --llm-client groq \
  --llm-model llama-3.3-70b-versatile \
```

---

## 🗂️ Output Structure

```
output/
├── transcriptions/
│   └── transcription_20250510_213038.txt
├── meeting_minutes/
│   └── meeting_minutes_20250510_213041.md
```

---

## 🧪 Supported Formats

* `.wav`
* `.mp3`

---

## ⚙️ CLI Options

| Argument                 | Description                                   |
| ------------------------ | --------------------------------------------- |
| `-i`, `--audio-path`     | Path to the input audio file                  |
| `-o`, `--output-dir`     | Output directory (default: `output/`)         |
| `--transcription-client` | `groq` or `google` (default: `groq`)          |
| `--transcription-model`  | e.g., `whisper-large-v3-turbo`                |
| `--llm-client`           | `groq` or `openai` (default: `groq`)          |
| `--llm-model`            | e.g., `llama-3.3-70b-versatile`               |

---

## 🤖 LLM Models

* **Groq Whisper**: `whisper-large`, `whisper-large-v3-turbo`, etc.
* **Google Speech**: Model defaults to their API standard
* **LLMs for minutes**: `llama-3`, `mixtral`, `gpt-4`, etc. (Groq/OpenAI)

---

## 📋 Roadmap

* [ ] Add support for multi-language meetings
* [ ] Speaker diarization support
* [ ] Upload directly to Notion or Google Docs
* [ ] Slack/Discord bots

---

## 🧑‍🎓 Author

**Deepak Raj**
👨‍💻 [GitHub](https://github.com/coderperfectplus) • 🌐 [LinkedIN](https://www.linkedin.com/in/deepak-raj-35887386/s)

---

## 🤝 Contributing

Pull requests are welcome! Found a bug or need a feature? Open an issue or submit a PR.

---

## ⚖️ License

[MIT License](LICENSE)

