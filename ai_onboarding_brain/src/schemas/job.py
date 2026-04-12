from pydantic import BaseModel
from typing import Optional

class DraftApprovalRequest(BaseModel):
    job_id: int
    candidate_email: str
    subject: str
    approved_content: str
    hr_comments: Optional[str] = None
