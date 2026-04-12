import pandas as pd
from datetime import datetime
from etl_pipeline.models.schema import CandidateInfo, JobTracker
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

def load_data(session: Session, transformed_df: pd.DataFrame):
    """
    Loads transformed candidate data into CANDIDATE_INFO and creates initial jobs.
    """
    now = datetime.now()
    new_candidates_count = 0
    updated_candidates_count = 0
    
    for _, row in transformed_df.iterrows():
        row_hash = row.get('ROW_HASH')
        
        # Check if record exists based on ROW_HASH
        existing_candidate = session.query(CandidateInfo).filter_by(ROW_HASH=row_hash).first()
        
        if existing_candidate:
            # Hash matches, no change needed. 
            continue
            
        # Check if candidate exists by CIN but updated hash
        cin = row.get('CIN')
        candidate = session.query(CandidateInfo).filter_by(CIN=cin).first()
        
        if candidate:
            # Update candidate
            candidate.UPDATED_ON = now
            candidate.ROW_HASH = row_hash
            # NOTE: We can dynamically map the rest of the columns logic here if needed
            updated_candidates_count += 1
        else:
            # New Candidate
            new_candidate = CandidateInfo(
                CIN=cin,
                REF_NO=row.get('REF_NO'),
                OFFER_RELEASE_DATE=row.get('OFFER_RELEASE_DATE'),
                ROW_HASH=row_hash,
                CREATED_ON=now,
                UPDATED_ON=now
                # Note: Full data mapped logic placeholder...
            )
            session.add(new_candidate)
            session.flush() # Flush to get the CANDIDATE_ID
            
            # Create Job
            # Job type for 'documents required' implies a specific ID, typically 1 or referenced from JOB_TYPE_MASTER
            new_job = JobTracker(
                JOB_TYPE_ID=1, 
                START_TIME=now,
                CANDIDATE_ID=new_candidate.CANDIDATE_ID,
                STATUS_ID=1, # System status Pending
                UPDATED_ON=now
            )
            session.add(new_job)
            new_candidates_count += 1
            
    session.commit()
    logger.info(f"Load complete. New: {new_candidates_count}, Updated: {updated_candidates_count}")
