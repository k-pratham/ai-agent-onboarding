import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database Settings
    DB_URI: str = os.getenv("DB_URI", "oracle+cx_oracle://user:pass@localhost:1521/?service_name=orcl")
    
    # Mail Settings
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.sendgrid.net")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASS: str = os.getenv("SMTP_PASS", "")

    # Application Constants Mapping
    # Hardcoded fallback values matching standard master table seeding.
    
    # Status Types Master
    STATUS_PENDING_ID: int = 1
    STATUS_MAIL_DRAFTED_ID: int = 2
    STATUS_MAIL_SENT_ID: int = 3
    STATUS_MAIL_RECEIVED_ID: int = 4
    STATUS_VERIFIED_ID: int = 5
    STATUS_REJECTED_ID: int = 6
    STATUS_COMPLETED_ID: int = 7
    
    # Job Types Master
    JOB_TYPE_MAIL_SENT_ID: int = 1
    JOB_TYPE_FOLLOW_UP_ID: int = 2
    JOB_TYPE_ATTACHMENTS_SAVED_ID: int = 3

    class Config:
        env_file = ".env"

settings = Settings()

import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """ Generates a universally formatted logger for any backend module. """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(handler)
    return logger
