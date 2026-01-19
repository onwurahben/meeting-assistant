# utils/email_sender.py
# Optional email sending functions
# This file will contain:
# 1. Imports for SMTP or an email API client (e.g., smtplib, sendgrid).
# 2. Configuration for email credentials and server settings.
# 3. A `send_email` function that accepts recipient, subject, body, and attachments (PDF).
# 4. Error handling for failed email delivery.

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from utils.logger import get_logger

# Initialize logger for email operations
logger = get_logger("EmailSender")

def send_meeting_report(recipient_email, pdf_path, summary_text):
    """
    Sends the generated meeting summary and PDF report via email.
    Assumes standard SMTP configuration from environment variables.
    """
    logger.info(f"Preparing to send email to: {recipient_email}")
    
    # Step 1: Retrieve credentials from environment variables
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD") # Use an App Password for Gmail

    if not sender_email or not sender_password:
        logger.error("Email credentials missing in .env file.")
        return "Error: Sender credentials not configured."

    try:
        # Step 2: Create the multi-part email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Meeting Summary & Report"

        # Step 3: Attach the body of the email (the summary text)
        body = f"Hello,\n\nPlease find the meeting summary below and the full report attached.\n\n{summary_text}"
        msg.attach(MIMEText(body, 'plain'))

        # Step 4: Attach the PDF file
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(pdf_path)}'
                )
                msg.attach(part)
        else:
            logger.warning(f"PDF attachment not found at {pdf_path}. Sending email without it.")

        # Step 5: Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
        logger.info("Email sent successfully!")
        return True

    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return f"Error: {str(e)}"
