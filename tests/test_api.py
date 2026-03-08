import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "HireSense AI API is running."}

def test_analyze_job_fit():
    response = client.post(
        "/api/v1/analyze/job-fit",
        data={
            "resume_text": "I am a Python developer with 5 years experience in React and Node.js. I have managed docker deployments and AWS.",
            "job_description": "We need a Senior Backend Engineer proficient in Python, Docker, Kubernetes, and AWS."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert "breakdown" in data
    assert "explanation" in data
    
    # Validate breakdown
    assert "skills_match" in data["breakdown"]
    assert "experience_match" in data["breakdown"]
    
    assert type(data["explanation"]) == str
