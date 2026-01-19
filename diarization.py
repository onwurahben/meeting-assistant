# diarization.py
# Optional speaker diarization module
# This file will contain:
# 1. Imports for diarization tools (e.g., pyannote.audio).
# 2. A function to pipeline the audio for speaker identification.
# 3. Logic to map speaker segments to the transcription.
# 4. Handling of authentication tokens if using models like pyannote that require it.
# 5. Return format that includes speaker labels along with text segments.

import os
from utils.logger import get_logger

# Initialize logger for tracking diarization progress
logger = get_logger("Diarization")

def diarize_audio(audio_path, hf_token=None):
    """
    Identifies 'who spoke when' in an audio file.
    Note: Requires pyannote.audio and a Hugging Face token for pre-trained models.
    """
    logger.info(f"Starting diarization for: {audio_path}")
    
    # Check if the audio file exists before processing
    if not os.path.exists(audio_path):
        logger.error(f"Audio file not found: {audio_path}")
        return None

    try:
        # Step 1: Import pyannote.audio inside the function to keep it optional
        # This prevents the whole app from crashing if the library isn't installed.
        from pyannote.audio import Pipeline
        
        # Step 2: Initialize the pre-trained diarization pipeline
        # You need to accept the user agreement on Hugging Face for the speaker-diarization model.
        if hf_token is None:
            hf_token = os.getenv("HUGGINGFACE_TOKEN")
            
        if not hf_token:
            logger.warning("Hugging Face token missing. Diarization might fail.")
            return None

        # Load the pipeline from Hugging Face
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token
        )

        # Step 3: Run the pipeline on the audio file
        # This returns an 'Annotation' object containing speaker segments.
        diarization = pipeline(audio_path)

        # Step 4: Format the output into a readable list of segments
        speaker_segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speaker_segments.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            })
            
        logger.info(f"Diarization complete. Found {len(speaker_segments)} segments.")
        return speaker_segments

    except ImportError:
        logger.error("pyannote.audio not installed. Please install it to use diarization.")
        return "Error: pyannote.audio library not found."
    except Exception as e:
        logger.error(f"Unexpected error during diarization: {str(e)}")
        return f"Error: {str(e)}"
