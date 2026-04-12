import os
import logging
from .constants import EMAIL_ATTACHMENT_DIR

logger = logging.getLogger(__name__)

def get_attachment_path(cin: str) -> str:
    """
    Returns the target folder path to store attachments for a specific candidate.
    Creates the directory if it does not exist.
    """
    path = os.path.join(EMAIL_ATTACHMENT_DIR, cin)
    try:
        os.makedirs(path, exist_ok=True)
        return path
    except Exception as e:
        logger.error(f"Could not create path {path}: {e}")
        raise
