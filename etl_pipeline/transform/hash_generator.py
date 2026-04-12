import hashlib
import json
import pandas as pd

def generate_row_hash(row: pd.Series) -> str:
    """
    Generates a unique SHA-256 hash for a given DataFrame row.
    Nulls are filled to standardize output.
    """
    # Convert row to dict, replace NaNs with empty string
    row_dict = row.fillna('').to_dict()
    # Sort keys to ensure consistent hashing
    serialized = json.dumps(row_dict, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()
