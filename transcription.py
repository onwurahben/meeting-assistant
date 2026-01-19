import os
from dotenv import load_dotenv
from groq import Groq
from utils.logger import get_logger

# Initialize logger
logger = get_logger("Transcription")

# Load environment variables (GROQ_API_KEY)
load_dotenv()

def transcribe_audio(file_path):
    """
    Transcribes an audio file using Groq's Whisper API.
    
    Args:
        file_path (str): Path to the audio file (mp3, wav, m4a, etc.)
        
    Returns:
        str: Transcribed text or an error message.
    """
    logger.info(f"Starting transcription for: {file_path}")
    
    if not os.path.exists(file_path):
        error_msg = f"Error: File not found at {file_path}"
        logger.error(error_msg)
        return error_msg

    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        client = Groq(api_key=groq_api_key)
        
        with open(file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(file_path), file.read()),
                model="distil-whisper-large-v3-en",
                response_format="verbose_json"
            )
        
        logger.info(f"Transcription successful for: {file_path}")
        return transcription
    except Exception as e:
        error_msg = f"Error during transcription: {str(e)}"
        logger.error(error_msg)
        return error_msg
