# utils/deepgram_handler.py
# Unified Deepgram API Handler
# This module consolidates transcription and diarization.

import os
import time
from dotenv import load_dotenv
from deepgram import DeepgramClient
from utils.logger import get_logger

logger = get_logger("DeepgramHandler")

load_dotenv()

def process_audio_with_deepgram(file_path, diarize=False):
    """
    Processes an audio file using Deepgram's Nova-2 model.
    Can return either a simple transcript or a diarized segment list.
    
    Args:
        file_path (str): Path to the audio file.
        diarize (bool): If True, returns speaker-aligned segments.
        
    Returns:
        str or list: Depending on 'diarize' flag.
    """
    logger.info(f"Deepgram processing (diarize={diarize}) for: {file_path}")
    
    if not os.path.exists(file_path):
        error_msg = f"Error: File not found at {file_path}"
        logger.error(error_msg)
        return error_msg if not diarize else None

    try:
        # Step 1: Initialize the Deepgram Client 
        api_key = os.getenv("DEEPGRAM_API_KEY")
        if not api_key:
            error_msg = "Error: DEEPGRAM_API_KEY missing."
            logger.error(error_msg)
            return error_msg if not diarize else None
            
        deepgram = DeepgramClient(api_key=api_key)


        # Step 3: Read audio file
        logger.info("⏱️ Reading audio file...")
        read_start = time.time()
        with open(file_path, "rb") as file:
            audio_bytes = file.read()
        file_size_mb = len(audio_bytes) / (1024 * 1024)
        read_time = time.time() - read_start
        logger.info(f"✅ File read complete ({file_size_mb:.2f} MB) in {read_time:.2f} seconds")

        # Step 4: Call Deepgram API
        logger.info("⏱️ Calling Deepgram API...")
        api_start = time.time()
        response = deepgram.listen.v1.media.transcribe_file(
            request=audio_bytes,
            model="nova-2",
            smart_format=True,
            diarize=diarize,
            punctuate=True )
        api_time = time.time() - api_start
        logger.info(f"✅ Deepgram API call completed in {api_time:.2f} seconds")

        # Step 5: Process response
        logger.info("⏱️ Processing response...")
        process_start = time.time()
        if diarize:
            # Extract paragraphs with speaker labels
            paragraphs = response.results.channels[0].alternatives[0].paragraphs
            speaker_segments = []
            if paragraphs:
                for paragraph in paragraphs.paragraphs:
                    speaker_segments.append({
                        "speaker": f"Speaker {paragraph.speaker}",
                        "start": paragraph.start,
                        "end": paragraph.end,
                        "transcript": " ".join([s.text for s in paragraph.sentences]) if paragraph.sentences else ""
                    })
            process_time = time.time() - process_start
            logger.info(f"✅ Response processing completed in {process_time:.2f} seconds")
            return speaker_segments
        else:
            # Return simple text transcript
            result = response.results.channels[0].alternatives[0].transcript
            process_time = time.time() - process_start
            logger.info(f"✅ Response processing completed in {process_time:.2f} seconds")
            return result

    except Exception as e:
        error_msg = f"Deepgram Error: {str(e)}"
        logger.error(error_msg)
        return error_msg if not diarize else None

# --- High-level Wrapper Functions ---

def transcribe_audio(file_path):
    """
    Convenience function for simple transcription.
    """
    return process_audio_with_deepgram(file_path, diarize=False)

def diarize_audio(file_path):
    """
    Convenience function for speaker-labeled transcription.
    """
    return process_audio_with_deepgram(file_path, diarize=True)
