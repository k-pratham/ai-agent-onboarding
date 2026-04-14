import pytest
import datetime
from unittest.mock import MagicMock
from ai_onboarding_brain.src.services.hr_service import process_draft_approval
from ai_onboarding_brain.src.core.config import settings
from etl_pipeline.models.schema import JobTracker

@pytest.mark.asyncio
async def test_process_draft_approval_success(monkeypatch):
    mock_db = MagicMock()
    
    # Mock finding the initial job entry
    mock_job = MagicMock()
    mock_job.CANDIDATE_ID = 55
    mock_db.query.return_value.filter.return_value.first.return_value = mock_job
    
    # Mock the tool_send_email dependency to avoid actually sending emails
    async def mock_tool_send_email(email, subject, content):
        return "Success"
    monkeypatch.setattr("ai_onboarding_brain.src.services.hr_service.tool_send_email", mock_tool_send_email)
    
    response = await process_draft_approval(
        db=mock_db,
        job_id=1,
        candidate_email="test@test.com",
        subject="Hello",
        draft_content="Draft Content"
    )
    
    # Assert return status
    assert response["status"] == "success"
    assert response["message"] == "Success"
    
    # Assert job entry state mutations
    assert mock_job.HUMAN_ACTION_REQUIRED == 0
    assert mock_job.STATUS_ID == settings.STATUS_MAIL_SENT_ID
    assert mock_job.HUMAN_ACTION == "Approved"
    assert mock_job.DRAFT_MAIL == "Draft Content"
    
    # Assert specific follow-up addition and commits
    assert mock_db.add.called
    added_job = mock_db.add.call_args[0][0]
    
    assert added_job.CANDIDATE_ID == 55
    assert added_job.JOB_TYPE_ID == settings.JOB_TYPE_FOLLOW_UP_ID
    assert added_job.STATUS_ID == settings.STATUS_PENDING_ID
    assert added_job.HUMAN_ACTION_REQUIRED == 0
    # Date logic should be today + 2 days
    assert added_job.ACTION_DATE == datetime.date.today() + datetime.timedelta(days=2)
    
    assert mock_db.commit.called

@pytest.mark.asyncio
async def test_process_draft_approval_job_not_found(monkeypatch):
    mock_db = MagicMock()
    # Mock not finding a job entry
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    async def mock_tool_send_email(*args, **kwargs):
        return "Success"
    monkeypatch.setattr("ai_onboarding_brain.src.services.hr_service.tool_send_email", mock_tool_send_email)
    
    with pytest.raises(ValueError, match="JobTracker entry 999 not found."):
        await process_draft_approval(
            db=mock_db,
            job_id=999,
            candidate_email="test@test.com",
            subject="Hello",
            draft_content="Draft Content"
        )
