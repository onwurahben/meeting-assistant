# utils/sendgrid_handler.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from utils.logger import get_logger
import base64

logger = get_logger("SendGridHandler")

def send_meeting_report(recipient_email, pdf_path, summary_text):
    logger.info(f"Preparing to send email via SendGrid to: {recipient_email}")

    sender_email = os.getenv("SENDER_EMAIL")
    api_key = os.getenv("SENDGRID_API_KEY")

    if not sender_email or not api_key:
        logger.error("SendGrid credentials missing in .env file.")
        return "Error: Credentials not configured."

    # Step 1: Build the email
    message = Mail(
        from_email=sender_email,
        to_emails=recipient_email,
        subject="Meeting Summary & Report",
        plain_text_content=f"Hello,\n\nPlease find the meeting summary below and the full report attached.\n\n{summary_text}"
    )

    # Step 2: Attach PDF if exists
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            attachment = Attachment(
                FileContent(encoded),
                FileName(os.path.basename(pdf_path)),
                FileType('application/pdf'),
                Disposition('attachment')
            )
            message.attachment = attachment
    else:
        logger.warning(f"PDF attachment not found at {pdf_path}. Sending email without it.")

    # Step 3: Send the email
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        logger.info(f"Email sent successfully! Status code: {response.status_code}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email via SendGrid: {str(e)}")
        return f"Error: {str(e)}"
