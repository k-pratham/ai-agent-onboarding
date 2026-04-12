from fastapi import APIRouter, HTTPException
from ai_onboarding_brain.src.schemas.job import DraftApprovalRequest
from ai_onboarding_brain.src.services.hr_service import process_draft_approval
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/dashboard/pending-drafts")
async def get_pending_drafts():
    """
    Exposes pending action logic to the HR UI.
    Typically utilized when loading the "Approval Dashboard" viewing documents waiting validation.
    """
    # Sample mock placeholder until ORM integration query binding completes
    return [
        {"job_id": 100, "candidate": "John Doe", "cin": "20231201_JD123", "draft": "Please send missing PAN."}
    ]

@router.post("/action/approve-draft")
async def approve_draft(request: DraftApprovalRequest):
    """
    Interaction endpoint. 
    Receives HR edits/approval on the ML-generated follow-up string and initiates SMTP propagation.
    """
    try:
        response = await process_draft_approval(
            request.job_id,
            request.candidate_email,
            request.subject,
            request.approved_content
        )
        return response
    except Exception as e:
        logger.error(f"Approval sequence routing failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to dispatch HR verified draft.")
