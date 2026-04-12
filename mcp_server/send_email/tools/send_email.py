from mcp.server import Server
from mcp_server.send_email.engine.mail_engine import dispatch_email
import logging

logger = logging.getLogger(__name__)

async def tool_send_email(candidate_email: str, subject: str, draft_content: str) -> str:
    """
    MCP Tool: Sends an email to a candidate given the HR-approved draft content.
    Returns status confirming the operation.
    """
    try:
        dispatch_email(candidate_email, subject, draft_content)
        
        # Here we would also implement DB logic updating JOB_TRACKER: 
        # "Job type Followup_mail. NextActionDate +2 days."
        
        return f"Successfully sent the email draft to {candidate_email} with subject '{subject}'"
    except Exception as e:
        return f"Error sending email: {str(e)}"
