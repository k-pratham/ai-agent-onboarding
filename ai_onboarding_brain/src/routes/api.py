from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ai_onboarding_brain.src.schemas.job import DraftApprovalRequest, PendingDraftResponse
from ai_onboarding_brain.src.services.hr_service import process_draft_approval
from ai_onboarding_brain.src.core.database import get_db
from ai_onboarding_brain.src.core.config import settings, get_logger
from ai_onboarding_brain.src.core.exceptions import AppBaseException, CandidateNotFoundError, DatabaseTransactionError
from etl_pipeline.models.schema import JobTracker, CandidateInfo

logger = get_logger(__name__)
router = APIRouter()

@router.get("/dashboard/pending-drafts", response_model=List[PendingDraftResponse])
async def get_pending_drafts(db: Session = Depends(get_db)):
    """
    Exposes pending action logic to the HR UI.
    Fetches real draft emails waiting on human HR approval from the JobTracker.
    """
    try:
        # Fetch drafts where human action is required and they are pending an initial or follow-up email
        pending_jobs = db.query(JobTracker, CandidateInfo).join(
            CandidateInfo, JobTracker.CANDIDATE_ID == CandidateInfo.CANDIDATE_ID
        ).filter(
            JobTracker.STATUS_ID.in_([settings.STATUS_PENDING_ID, settings.STATUS_MAIL_DRAFTED_ID]),
            JobTracker.HUMAN_ACTION_REQUIRED == 1,
            JobTracker.JOB_TYPE_ID.in_([settings.JOB_TYPE_MAIL_SENT_ID, settings.JOB_TYPE_FOLLOW_UP_ID])
        ).all()
        
        results = []
        for job, candidate in pending_jobs:
            results.append(PendingDraftResponse(
                job_id=job.JOB_ID,
                candidate=candidate.CANDIDATE_NAME or candidate.CIN,
                cin=candidate.CIN,
                draft=job.DRAFT_MAIL or ""
            ))
            
        return results
    except Exception as e:
        logger.error(f"Failed to query pending drafts natively: {e}")
        raise HTTPException(status_code=500, detail="Database parsing failed")

@router.post("/action/approve-draft")
async def approve_draft(request: DraftApprovalRequest, db: Session = Depends(get_db)):
    """
    Interaction endpoint. 
    Receives HR edits/approval on the ML-generated follow-up string and initiates SMTP propagation.
    """
    try:
        response = await process_draft_approval(
            db,
            request.job_id,
            request.candidate_email,
            request.subject,
            request.approved_content
        )
        return response
    except CandidateNotFoundError as e:
        logger.warning(f"Draft verification missed Candidate hook: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseTransactionError as e:
        logger.error(f"Draft verification failed committing to Oracle: {e}")
        raise HTTPException(status_code=500, detail="Server transaction failed natively.")
    except AppBaseException as e:
        logger.warning(f"Business logic failure executing draft approval: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Approval sequence routing failed catastrophically: {e}")
        raise HTTPException(status_code=500, detail="Failed to dispatch HR verified draft: " + str(e))
