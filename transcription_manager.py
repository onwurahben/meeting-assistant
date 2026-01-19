import os
import time
from transcription import transcribe_audio
from diarization import diarize_audio
import deepgram_handler
from utils.logger import get_logger

logger = get_logger("TranscriptionManager")

def align_segments(whisper_segments, pyannote_segments):
    """
    Aligns Whisper text segments with Pyannote speaker labels based on timestamps.
    """
    logger.info("Aligning Whisper transcription with Pyannote diarization...")
    aligned_transcript = []
    
    for ws in whisper_segments:
        w_start = ws.get('start', 0)
        w_end = ws.get('end', 0)
        w_text = ws.get('text', "").strip()
        
        # Find the speaker who was talking most during this segment
        best_speaker = "Unknown Speaker"
        max_overlap = 0
        
        for ps in pyannote_segments:
            overlap = min(w_end, ps['end']) - max(w_start, ps['start'])
            if overlap > max_overlap:
                max_overlap = overlap
                best_speaker = ps['speaker']
        
        aligned_transcript.append(f"{best_speaker}: {w_text}")
    
    return "\n".join(aligned_transcript)

def process_meeting_audio(file_path):
    """
    Unified entry point for transcription and diarization.
    Tries Local (Whisper + Pyannote) first, then falls back to Deepgram.
    """
    logger.info(f"⏱️ Starting audio processing for: {file_path}")
    total_start = time.time()
    
    # 0. Fast-check for Pyannote availability to avoid wasted Whisper calls
    # If the user doesn't have local diarization, they likely want the full Deepgram experience.
    pyannote_available = False
    try:
        from pyannote.audio import Pipeline
        pyannote_available = True
        logger.info("✅ Pyannote available - will try local flow first")
    except ImportError:
        logger.info("⚠️ pyannote.audio not found. Skipping local flow and falling back to Deepgram.")

    if pyannote_available:
        # 1. Try Local Flow
        try:
            logger.info("⏱️ Attempting local transcription flow (Whisper + Pyannote)...")
            local_start = time.time()
            
            # Get verbose transcription (with segments)
            whisper_response = transcribe_audio(file_path)
            
            if isinstance(whisper_response, dict) and 'segments' in whisper_response:
                # Try diarization
                pyannote_segments = diarize_audio(file_path)
                
                if pyannote_segments and isinstance(pyannote_segments, list):
                    # Successful local flow - align them
                    result = align_segments(whisper_response['segments'], pyannote_segments)
                    local_time = time.time() - local_start
                    total_time = time.time() - total_start
                    logger.info(f"✅ Local transcription completed in {local_time:.2f}s (total: {total_time:.2f}s)")
                    return result
                else:
                    logger.warning("⚠️ Diarization failed. Falling back to Deepgram for full speaker support.")
                    # If diarization failed, we go to Deepgram instead of just plain Whisper
                    # to fulfill the "diarized transcript" requirement.
            else:
                logger.warning("⚠️ Whisper failed or returned non-segmented output.")
        except Exception as e:
            logger.error(f"❌ Local flow failed: {str(e)}. Falling back to Deepgram.")
        
    # 2. Fallback to Deepgram (either because Pyannote is missing or local flow failed)
    try:
        logger.info("🌐 Using Deepgram API for transcription and diarization.")
        deepgram_start = time.time()
        deepgram_segments = deepgram_handler.diarize_audio(file_path)
        
        if deepgram_segments and isinstance(deepgram_segments, list):
            formatted_lines = [f"{s['speaker']}: {s['transcript']}" for s in deepgram_segments]
            result = "\n".join(formatted_lines)
            deepgram_time = time.time() - deepgram_start
            total_time = time.time() - total_start
            logger.info(f"✅ Deepgram transcription completed in {deepgram_time:.2f}s (total: {total_time:.2f}s)")
            return result
        else:
            # Last ditch effort: Simple Deepgram transcription
            logger.info("⚠️ Diarized segments empty, trying simple transcription...")
            result = deepgram_handler.transcribe_audio(file_path)
            deepgram_time = time.time() - deepgram_start
            total_time = time.time() - total_start
            logger.info(f"✅ Deepgram simple transcription completed in {deepgram_time:.2f}s (total: {total_time:.2f}s)")
            return result
            
    except Exception as e:
        total_time = time.time() - total_start
        logger.error(f"❌ Deepgram fallback also failed after {total_time:.2f}s: {str(e)}")
        return f"Error: All transcription methods failed. {str(e)}"
