---
title: "AI Meeting Intelligence Assistant"
emoji: "🎙️"
colorFrom: "slate"
colorTo: "indigo"
sdk: gradio
sdk_version: "6.3.0"
app_file: app.py
pinned
---



# AI Meeting Intelligence Assistant

An end-to-end AI system that transforms raw meeting audio into structured, speaker-aware transcripts, summaries, and shareable PDF reports.

This application demonstrates a **production-style speech intelligence pipeline**, combining modern speech-to-text, speaker diarization, LLM-based post-processing, and polished outputs suitable for internal business use.

---

## ✨ Features

* Upload recorded meeting audio (MP3 / WAV)
* High-accuracy speech-to-text transcription (Deepgram Nova-2 or Whisper)
* Accurate **speaker diarization** with timestamp alignment
* Clean, readable meeting transcripts
* Automated meeting summaries
* PDF report generation
* Email delivery of results
* Web-based UI built with **Gradio 6**

---

## 🧠 System Architecture (High Level)

```
Audio Upload
     ↓
Speech-to-Text (Deepgram)
     ↓
Speaker Diarization
     ↓
Segment Alignment & Cleanup
     ↓
LLM-Based Summarization
     ↓
Transcript + PDF + Email Output
```

This design mirrors how **real internal AI tools** are built inside companies — modular and extensible.

---

## 🛠️ Tech Stack

* **UI**: Gradio 6.3.0
* **Backend**: Python
* **Speech-to-Text**: Deepgram SDK Nova-2 or Whisper
* **Speaker Diarization**: Deepgram SDK Nova-2 or Pyannote(local)
* **LLM**: Llama 3 via Groq API (LLM inference)
* **Audio Processing**: pydub, ffmpy
* **Reporting**: fpdf2 (PDF generation)
* **Email Delivery**: SMTP / SendGrid (optional)
* **Deployment**: Hugging Face Spaces (CPU)

---

## 🔐 Environment Variables

To run this app, set the following environment variables:

```bash
DEEPGRAM_API_KEY=your_deepgram_key
GROQ_API_KEY=your_groq_key

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=meetings@yourdomain.com
SENDER_PASSWORD=your_app_password
```

You can configure these securely in **Hugging Face → Space Settings → Variables**.

---

## 🚀 Running Locally

```bash
pip install -r requirements.txt
python app.py
```

The app will launch at:

```
http://127.0.0.1:7860
```

---

## 🎯 Use Cases

* Internal meeting documentation
* Async team updates
* Founder / leadership meetings
* Client calls and discovery sessions
* Research interviews

---

## 🧩 Notes on Deployment

* Currently configured to run on **CPU-only environments** (via Deepgram API)
* Suitable for Hugging Face CPU Basic tier
* Heavy models like Whisper (local) and Pyannote need more resources to run locally.

---

## 📌 Portfolio Context

This project is intentionally built as a **systems-focused AI application**, not a chatbot.

It demonstrates:

* Applied AI integration
* Speech intelligence pipelines
* Real-world automation design
* Clean separation of concerns

---

## 📄 License

MIT License

---

**Built as an AI engineering project.**
