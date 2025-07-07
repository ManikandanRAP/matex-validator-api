import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

VALID_TOKEN = settings.API_TOKEN
INVALID_TOKEN = "invalid-token"

# --- Test Data ---

completed_check_payload = {
    "caseId": 1,
    "clientId": 100,
    "Projectid": 200,
    "Corporateid": 300,
    "Packageid": 400,
    "checkId": 500,
    "completionDetails": {
        "completedDate": "2025-05-29T10:30:00.000Z",
        "completedBy": "test_user",
        "checkStatus": "COMPLETED",
        "verificationResult": "Verified",
        "remarks": "All clear"
    }
}

completed_case_payload = {
    "caseId": 1,
    "clientId": 100,
    "Projectid": 200,
    "Corporateid": 300,
    "Packageid": 400,
    "caseDetails": {
        "caseRegistrationNumber": "CASE-123",
        "candidateName": "John Doe",
        "completedDate": "2025-05-29T10:30:00.000Z",
        "completedBy": "test_user",
        "totalChecks": 1,
        "completedChecks": 1,
        "caseStatus": "COMPLETED"
    },
    "checksCompleted": [
        {
            "checkId": 500,
            "checkName": "ID Check",
            "subChecks": [
                {
                    "subCheckId": 501,
                    "subCheckName": "Passport Verification",
                    "status": "COMPLETED"
                }
            ]
        }
    ]
}

interim_case_payload = {
    "caseId": 1,
    "clientId": 100,
    "projectid": 200,
    "corporateid": 300,
    "packageid": 400,
    "interimDetails": {
        "interimDate": "2025-05-29T10:30:00.000Z",
        "interimBy": "auto_system",
        "interimType": "SCHEDULED",
        "progressPercentage": 50,
        "remarks": "Halfway there"
    },
    "currentStatus": {
        "totalChecks": 2,
        "completedChecks": 1,
        "inProgressChecks": 1,
        "pendingChecks": 0
    },
    "checksCompleted": [
        {
            "checkId": 500,
            "checkName": "ID Check",
            "subChecks": [
                {
                    "subCheckId": 501,
                    "subCheckName": "Passport Verification",
                    "status": "COMPLETED"
                }
            ]
        }
    ]
}

# --- Fixtures for Headers ---

@pytest.fixture
def auth_headers():
    return {"Authorization": f"Bearer {VALID_TOKEN}"}

@pytest.fixture
def invalid_auth_headers():
    return {"Authorization": f"Bearer {INVALID_TOKEN}"}

# --- Test Cases ---

# Completed Check Endpoint
def test_completed_check_success(auth_headers):
    response = client.post("/matex/completed-check", headers=auth_headers, json=completed_check_payload)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "SUCCESS"
    assert "validationId" in json_response

def test_completed_check_no_auth():
    response = client.post("/matex/completed-check", json=completed_check_payload)
    assert response.status_code == 401

def test_completed_check_invalid_auth(invalid_auth_headers):
    response = client.post("/matex/completed-check", headers=invalid_auth_headers, json=completed_check_payload)
    assert response.status_code == 401

# Completed Case Endpoint
def test_completed_case_success(auth_headers):
    response = client.post("/matex/completed-case", headers=auth_headers, json=completed_case_payload)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "SUCCESS"
    assert "validationId" in json_response
    assert "timestamp" in json_response

def test_completed_case_no_auth():
    response = client.post("/matex/completed-case", json=completed_case_payload)
    assert response.status_code == 401

def test_completed_case_invalid_auth(invalid_auth_headers):
    response = client.post("/matex/completed-case", headers=invalid_auth_headers, json=completed_case_payload)
    assert response.status_code == 401

# Interim Case Endpoint
def test_interim_case_success(auth_headers):
    response = client.post("/rap/interim-case", headers=auth_headers, json=interim_case_payload)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "SUCCESS"
    assert "validationId" in json_response

def test_interim_case_no_auth():
    response = client.post("/rap/interim-case", json=interim_case_payload)
    assert response.status_code == 401

def test_interim_case_invalid_auth(invalid_auth_headers):
    response = client.post("/rap/interim-case", headers=invalid_auth_headers, json=interim_case_payload)
    assert response.status_code == 401
