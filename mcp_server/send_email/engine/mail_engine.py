import smtplib
from email.message import EmailMessage
import logging
import os

logger = logging.getLogger(__name__)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.sendgrid.net")  # Example default
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "apikey")
SMTP_PASS = os.getenv("SMTP_PASS", "")

def dispatch_email(to_address: str, subject: str, draft_content: str):
    """
    Dispatches a pre-approved draft email via SMTP.
    """
    try:
        msg = EmailMessage()
        msg.set_content(draft_content)
        msg['Subject'] = subject
        msg['From'] = "hr-noreply@example.com"
        msg['To'] = to_address
        
        # NOTE: Using sendgrid or similar standard setup
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            if SMTP_PASS: # Login if credentials provided
                server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        logger.info(f"Email successfully dispatched to {to_address}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_address}: {e}")
        raise
