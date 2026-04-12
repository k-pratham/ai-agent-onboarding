import os
import logging
from mcp_server.constants.common_functions import get_attachment_path
from datetime import datetime

logger = logging.getLogger(__name__)

def store_attachment(cin: str, file_name: str, file_bytes: bytes) -> str:
    """
    Saves the attachment into the candidate's CIN folder locally.
    Returns the absolute path of stored file.
    """
    target_dir = get_attachment_path(cin)
    
    # Optional: sanitize file_name or append timestamp to prevent overwriting identical names
    clean_name = os.path.basename(file_name)
    file_path = os.path.join(target_dir, clean_name)
    
    try:
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        logger.info(f"Stored attachment {clean_name} for candidate {cin}")
        return os.path.abspath(file_path)
    except Exception as e:
        logger.error(f"Error saving attachment {clean_name}: {e}")
        raise
