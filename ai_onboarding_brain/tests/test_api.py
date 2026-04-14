import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import date

# Import app to mount TestClient
from ai_onboarding_brain.src.main import app
from ai_onboarding_brain.src.core.database import get_db
from ai_onboarding_brain.src.core.config import settings

client = TestClient(app)

# Helper Mocks for SQLAlchemy Objects
class MockJob:
    def __init__(self, job_id, draft):
        self.JOB_ID = job_id
        self.DRAFT_MAIL = draft

class MockCandidate:
    def __init__(self, name, cin):
        self.CANDIDATE_NAME = name
        self.CIN = cin

def test_get_pending_drafts_empty(monkeypatch):
    mock_db = MagicMock()
    # Setup chain: db.query().join().filter().all()
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = []
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.get("/api/v1/dashboard/pending-drafts")
    assert response.status_code == 200
    assert response.json() == []
    
    app.dependency_overrides.clear()

def test_get_pending_drafts_with_data(monkeypatch):
    mock_db = MagicMock()
    # Mock return value for the chained query sequence
    mock_job = MockJob(job_id=1, draft="Hello from HR")
    mock_candidate = MockCandidate(name="John Doe", cin="CIN123")
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [
        (mock_job, mock_candidate)
    ]
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.get("/api/v1/dashboard/pending-drafts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["job_id"] == 1
    assert data[0]["candidate"] == "John Doe"
    assert data[0]["cin"] == "CIN123"
    assert data[0]["draft"] == "Hello from HR"
    
    app.dependency_overrides.clear()

def test_approve_draft_success(monkeypatch):
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # We need to mock process_draft_approval inside the api
    async def mock_process_draft_approval(*args, **kwargs):
        return {"status": "success", "message": "Email sent"}
        
    monkeypatch.setattr("ai_onboarding_brain.src.routes.api.process_draft_approval", mock_process_draft_approval)
    
    payload = {
        "job_id": 100,
        "candidate_email": "test@candidate.com",
        "subject": "Missing Forms",
        "approved_content": "Please send it"
    }
    
    response = client.post("/api/v1/action/approve-draft", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    app.dependency_overrides.clear()
