import pandas as pd
from datetime import datetime
from etl_pipeline.transform.hash_generator import generate_row_hash

def transform_candidate_data(df_dict: dict) -> pd.DataFrame:
    """
    Consolidates sheets, applies transformations, adds ROW_HASH and CIN.
    """
    all_rows = []
    
    for sheet_name, df in df_dict.items():
        # Add source sheet name for traceability if needed
        df['SOURCE_SHEET'] = sheet_name
        all_rows.append(df)
        
    combined_df = pd.concat(all_rows, ignore_index=True)
    
    # Generate CIN: Concatenate offer release date + Ref No.
    # Ensure offer release date is datetime and formatted properly if present
    if 'OFFER_RELEASE_DATE' in combined_df.columns and 'REF_NO' in combined_df.columns:
        combined_df['OFFER_RELEASE_DATE'] = pd.to_datetime(combined_df['OFFER_RELEASE_DATE'], errors='coerce')
        combined_df['CIN'] = combined_df.apply(
            lambda x: f"{x['OFFER_RELEASE_DATE'].strftime('%Y%m%d') if pd.notnull(x['OFFER_RELEASE_DATE']) else 'UNKNOWN'}_{str(x['REF_NO'])}", axis=1
        )
    
    # Generate ROW_HASH
    combined_df['ROW_HASH'] = combined_df.apply(generate_row_hash, axis=1)
    
    return combined_df
