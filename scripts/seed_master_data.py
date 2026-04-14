import os
import sys
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to sys.path to easily import the models
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from etl_pipeline.models.schema import StatusMaster, JobTypeMaster, DocumentTypeMaster, Base

DB_URI = os.getenv("DB_URI", "oracle+cx_oracle://user:pass@localhost:1521/?service_name=orcl")

def seed_data():
    engine = create_engine(DB_URI)
    
    # Ensure tables exist (skip if using alembic or DB already created)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Seed Status Master
        statuses = [
            (1, 'Pending'),
            (2, 'Mail Drafted'),
            (3, 'Mail Sent'),
            (4, 'Mail Received'),
            (5, 'Verified'),
            (6, 'Rejected'),
            (7, 'Completed')
        ]
        
        for status_id, status_type in statuses:
            if not session.query(StatusMaster).filter_by(STATUS_ID=status_id).first():
                session.add(StatusMaster(STATUS_ID=status_id, STATUS_TYPE=status_type, IS_ACTIVE=1))
                
        # Seed Job Type Master
        job_types = [
            (1, 'mail sent', 'documents required', 'Initial mail for missing documents'),
            (2, 'follow up', 'documents required', 'Follow up mail for pending documents'),
            (3, 'attachments saved', '', 'Attachments successfully processed')
        ]
        
        for job_id, job_type, job_subtype, desc in job_types:
            if not session.query(JobTypeMaster).filter_by(JOB_TYPE_ID=job_id).first():
                session.add(JobTypeMaster(
                    JOB_TYPE_ID=job_id,
                    JOB_TYPE=job_type,
                    JOB_SUBTYPE=job_subtype,
                    JOB_DESCRIPTION=desc,
                    CREATED_ON=date.today(),
                    UPDATED_ON=date.today(),
                    IS_ACTIVE=1
                ))

        # Seed Document Type Master
        document_types = [
            (1, 'Aadhaar Card', 1, 1, 1),
            (2, 'PAN Card', 1, 1, 1),
            (3, '10th Marksheet', 1, 1, 1),
            (4, '12th Marksheet', 1, 1, 1),
            (5, 'Degree Certificate', 1, 1, 0),
            (6, 'Experience Letter', 0, 1, 1),
            (7, 'Relieving Letter', 0, 1, 1),
            (8, 'Salary Slips', 0, 1, 0)
        ]
        
        for doc_id, doc_name, fresher, exp, dev in document_types:
            if not session.query(DocumentTypeMaster).filter_by(DOCUMENT_TYPE_ID=doc_id).first():
                session.add(DocumentTypeMaster(
                    DOCUMENT_TYPE_ID=doc_id,
                    DOCUMENT_NAME=doc_name,
                    FRESHER=fresher,
                    EXPERIENCE=exp,
                    DEV_PARTNER=dev,
                    CREATED_ON=date.today(),
                    UPDATED_ON=date.today(),
                    IS_ACTIVE=1
                ))
                
        session.commit()
        print("Successfully seeded master data.")
    except Exception as e:
        session.rollback()
        print(f"Error seeding data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()
