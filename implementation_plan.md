# Implementation Plan - AI Meeting Assistant

## Goal Description
Implement the core modules (transcription, logging) for the AI meeting assistant.

## User Review Required
> [!IMPORTANT]
> You will need a **Groq API Key** saved in a `.env` file as `GROQ_API_KEY=your_key_here`.

## Proposed Changes
### Core Modules
#### [MODIFY] [transcription.py](file:///c:/Users/Benny/ai_meeting_assistant/transcription.py) [DONE]
- Updated to use `distil-whisper-large-v3-en`.
- Integrate logging for monitoring transcription events and errors.

#### [NEW] [utils/logger.py](file:///c:/Users/Benny/ai_meeting_assistant/utils/logger.py) [DONE]
- Centralized logging configuration using Python's `logging` module.
- Configure both console and file logging.

#### [MODIFY] [summarization.py](file:///c:/Users/Benny/ai_meeting_assistant/summarization.py) [DONE]
- Import `groq`, `dotenv`, and `prompts`.
- Implement `summarize_text(transcript)` using LLaMA 3 via Groq.
- Integrate logging for summarization success/failure.

#### [MODIFY] [prompts/meeting_prompts.py](file:///c:/Users/Benny/ai_meeting_assistant/prompts/meeting_prompts.py) [DONE]
- Add the actual prompt text for summarization and action item extraction.

#### [NEW] [utils/pdf_export.py](file:///c:/Users/Benny/ai_meeting_assistant/utils/pdf_export.py) [DONE]
- Implement PDF generation using `fpdf2`.
- Format summary and transcript into a professional document.

#### [NEW] [utils/deepgram_handler.py](file:///c:/Users/Benny/ai_meeting_assistant/utils/deepgram_handler.py) [DONE]
- Unified API handler for Deepgram Nova-2.
- Contains `transcribe_audio_deepgram` and `diarize_audio_deepgram` functions.
- Handles both transcription and diarization without heavy local dependencies.

## Future Considerations
> [!NOTE]
> The following features are planned for future iterations based on user feedback:
> - **Editable Meeting Titles**: Allow users to manually set the title of the generated summary and PDF.
> - **Meeting Metadata**: Fields for attendees, date, and location.
> - **Editable Transcript**: A text editor for the transcript before summarization.

## Verification Plan
### Automated Tests
- Create a small test script to transcribe a sample audio file and print the output.
