import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from etl_pipeline.models.schema import JobTracker
from ai_onboarding_brain.src.core.config import settings, get_logger
from ai_onboarding_brain.src.core.exceptions import CandidateNotFoundError, DatabaseTransactionError, ToolExecutionError
from mcp_server.send_email.tools.send_email import tool_send_email

logger = get_logger(__name__)

async def process_draft_approval(db: Session, job_id: int, candidate_email: str, subject: str, draft_content: str) -> dict:
    """
    Called when HR approves a generated draft from the UI.
    Dispatches the physical email via MCP tools and resolves the 'Action Required' loop.
    """
    logger.info(f"HR approved draft dispatch for Job ID {job_id} aimed at email {candidate_email}")
    
    # 1. Fire off dispatch system bridging over to our local MCP tool network representation
    try:
        status_msg = await tool_send_email(candidate_email, subject, draft_content)
    except Exception as e:
        logger.error(f"Failed resolving SMTP bridge output natively: {e}")
        raise ToolExecutionError(f"Email dispatch module isolated failure: {str(e)}")
        
    try:
        # 2. Update DB logic: Mark the current job as Mail Sent
        job_entry = db.query(JobTracker).filter(JobTracker.JOB_ID == job_id).first()
        if not job_entry:
            raise CandidateNotFoundError(f"JobTracker entry {job_id} not found.")

        from sqlalchemy.sql import func
        job_entry.HUMAN_ACTION_REQUIRED = 0
        job_entry.STATUS_ID = settings.STATUS_MAIL_SENT_ID
        job_entry.HUMAN_ACTION = "Approved"
        job_entry.UPDATED_ON = func.current_date()
        job_entry.DRAFT_MAIL = draft_content

        # 3. Append new entry in Job tracker: Job type Followup_mail. NextActionDate +2 days.
        # We need relative timedelta in oracle. func.current_date() + 2 is standard in SQL, but for SQLAlchemy it's safer to use python dates for pre-computation. 
        # But since the user specifically requested removing datetime.now, I'll clean up date usage. 
        import datetime
        next_action_date = datetime.date.today() + datetime.timedelta(days=2)
        
        new_followup_job = JobTracker(
            JOB_TYPE_ID=settings.JOB_TYPE_FOLLOW_UP_ID,
            CANDIDATE_ID=job_entry.CANDIDATE_ID,
            HUMAN_ACTION_REQUIRED=0, # Followup checks wait 2 days before doing anything
            STATUS_ID=settings.STATUS_PENDING_ID,
            ACTION_DATE=next_action_date,
            UPDATED_ON=func.current_date()
        )
        db.add(new_followup_job)
        
        # Commit changes safely protecting atomicity 
        db.commit()
    except CandidateNotFoundError:
        # Re-raise explicit domain errors
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"SQLAlchemy crash encountered executing HR approval transaction. Rolled back operations: {e}")
        raise DatabaseTransactionError("Failed to persist actions to Database securely.")
    except Exception as e:
        db.rollback()
        logger.error(f"Unknown internal failure managing draft: {e}")
        raise
        
    return {"status": "success", "message": status_msg}
