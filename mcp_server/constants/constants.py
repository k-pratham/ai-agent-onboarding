import os

# Base directory for all email attachments to be saved
# We fall back to a local folder in current working directory if env unavailable
EMAIL_ATTACHMENT_DIR = os.getenv("EMAIL_ATTACHMENT_DIR", "./email_attachments")
