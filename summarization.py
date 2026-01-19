import os
import time
from dotenv import load_dotenv
from groq import Groq
from utils.logger import get_logger
from prompts.meeting_prompts import MEETING_SUMMARY_PROMPT

logger = get_logger("Summarization")

load_dotenv()

def summarize_text(transcript):
    """
    Summarizes a meeting transcript using Groq's LLaMA API.
    
    Args:
        transcript (str): The transcribed text of the meeting.
        
    Returns:
        str: The generated summary in Markdown format.
    """
    logger.info("Starting summarization of transcript.")
    
    if not transcript or not transcript.strip():
        logger.warning("Empty transcript provided for summarization.")
        return "Error: No transcript content to summarize."

    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        client = Groq(api_key=groq_api_key)
        
        prompt = MEETING_SUMMARY_PROMPT.format(transcript=transcript)
        
        logger.info("⏱️ Calling Groq API for summarization...")
        api_start = time.time()
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2048
        )
        api_time = time.time() - api_start
        logger.info(f"✅ Groq API call completed in {api_time:.2f} seconds")
        
        summary = completion.choices[0].message.content
        logger.info("Summarization successful.")
        return summary
    except Exception as e:
        error_msg = f"Error during summarization: {str(e)}"
        logger.error(error_msg)
        return error_msg
