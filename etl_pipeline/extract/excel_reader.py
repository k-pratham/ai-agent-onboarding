import pandas as pd
import logging

logger = logging.getLogger(__name__)

def extract_excel_data(file_path: str) -> dict:
    """
    Extracts data from all sheets in the given Excel file.
    Args:
        file_path: Path to the shared Excel offer tracker.
    Returns:
        Dictionary of DataFrames, keyed by sheet name.
    """
    try:
        logger.info(f"Extracting data from {file_path}")
        # sheet_name=None reads all sheets into a dict of DataFrames
        df_dict = pd.read_excel(file_path, sheet_name=None)
        logger.info(f"Successfully extracted {len(df_dict)} sheets.")
        return df_dict
    except Exception as e:
        logger.error(f"Error extracting data from {file_path}: {str(e)}")
        raise
