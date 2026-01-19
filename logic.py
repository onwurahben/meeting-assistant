# logic.py
# Business logic for the AI Meeting Assistant
# Handles transcription, summarization, PDF export, and email sending

from transcription_manager import process_meeting_audio as speech_to_text
from summarization import summarize_text
from utils.pdf_export import export_to_pdf
from utils.email_sender import send_meeting_report
from utils.logger import get_logger
import os
import re
import time

logger = get_logger("Logic")

# State variables to track last generated content
last_pdf_path = None
last_summary = None

def process_meeting(audio_file):
    """
    Handles the full pipeline: Transcription -> Summarization -> PDF Export.
    """
    global last_pdf_path, last_summary
    
    if audio_file is None:
        return "Please upload an audio file.", "", None, ""
    
    logger.info(f"Processing new meeting audio: {audio_file}")
    pipeline_start = time.time()
    
    # 1. Transcribe
    logger.info("⏱️ Starting transcription...")
    transcription_start = time.time()
    transcript = speech_to_text(audio_file)
    transcription_time = time.time() - transcription_start
    logger.info(f"✅ Transcription completed in {transcription_time:.2f} seconds")
    
    if transcript.startswith("Error"):
        return transcript, "Summarization skipped due to transcription error.", None, ""
    
    # 2. Summarize
    logger.info("⏱️ Starting summarization...")
    summarization_start = time.time()
    summary = summarize_text(transcript)
    summarization_time = time.time() - summarization_start
    logger.info(f"✅ Summarization completed in {summarization_time:.2f} seconds")
    
    if summary.startswith("Error"):
        return transcript, summary, None, ""
    
    # 3. Export to PDF
    logger.info("⏱️ Starting PDF export...")
    pdf_start = time.time()
    pdf_path = export_to_pdf(summary, transcript)
    pdf_time = time.time() - pdf_start
    logger.info(f"✅ PDF export completed in {pdf_time:.2f} seconds")
    
    # Store for email sending
    last_pdf_path = pdf_path
    last_summary = summary
    
    total_time = time.time() - pipeline_start
    logger.info(f"🎉 Meeting processing complete in {total_time:.2f} seconds")
    logger.info(f"📊 Breakdown: Transcription={transcription_time:.2f}s, Summarization={summarization_time:.2f}s, PDF={pdf_time:.2f}s")
    
    return transcript, summary, pdf_path, ""

def send_email(recipient_email):
    """
    Sends the last generated meeting report via email.
    """
    # Validate email is not empty
    if not recipient_email or not recipient_email.strip():
        return "⚠️ Please enter a valid email address."
    
    # Validate email format using regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, recipient_email.strip()):
        return "⚠️ Invalid email format. Please enter a valid email address (e.g., user@example.com)."
    
    if not last_pdf_path or not last_summary:
        return "⚠️ No report available. Please process a meeting first."
    
    if not os.path.exists(last_pdf_path):
        return "⚠️ PDF file not found. Please regenerate the report."
    
    logger.info(f"Sending email to: {recipient_email}")
    result = send_meeting_report(recipient_email, last_pdf_path, last_summary)
    
    if result is True:
        return f"✅ Email sent successfully to {recipient_email}!"
    else:
        return f"❌ Failed to send email: {result}"
