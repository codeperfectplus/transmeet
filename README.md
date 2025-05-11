# 🎙️ TransMeet — AI-Powered Meeting Summarizer

> **Turn your meeting recordings into clear, structured minutes using LLMs like Groq Whisper and Google Speech Recognition.**

---

## 🚀 Features

* ✅ **Audio Transcription** — Automatically convert `.wav` or `.mp3` files into text
* 🧠 **LLM-Powered Summarization** — Generate concise and structured meeting minutes
* 🔍 **Groq & Google Support** — Choose between Groq Whisper models or Google Speech API
* 🪓 **Automatic Chunking** — Splits large files intelligently for smoother transcription
* 🧾 **CLI & Python API** — Use it from the terminal or integrate in your Python workflows
* 📁 **Clean Output** — Saves transcripts and summaries neatly in your desired folder

---

## 📦 Installation

```bash
pip install transmeet
```

---

## 🔐 Setup

Set your **GROQ API Key** as an environment variable:

```bash
export GROQ_API_KEY=your_groq_api_key
```

To make this permanent, add it to your shell config (e.g., `~/.bashrc` or `~/.zshrc`):

```bash
echo 'export GROQ_API_KEY=your_groq_api_key' >> ~/.bashrc
```

---

## 🧑‍💻 How to Use

### ✅ Option 1: Import as a Python Module

```python
from transmeet import generate_meeting_transcript_and_minutes

audio_path = "/path/to/your/audio.wav"
output_path = "/path/to/output/folder"

generate_meeting_transcript_and_minutes(audio_path, output_path)
```

This will save two files in your output directory:

* `transcription_<timestamp>.txt`
* `meeting_minutes_<timestamp>.md`

---

### 🔧 Option 2: Use the CLI

#### Basic Command

```bash
transmeet -a /path/to/audio.wav -o output/
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

## 🛠️ Configuration

You can also customize transcription behavior using a `config.conf` file (optional). See examples in the repo.

---

## 🤖 LLM Models

* **Groq Whisper** (e.g. `whisper-large`)
* **Google Speech Recognition** (fallback if `--use-groq` not set)

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

Pull requests are welcome! If you find a bug or want a feature, open an issue or submit a PR.

---

## ⚖️ License

[MIT License](LICENSE)
