# MatEx RAP Validator Integration API Design Document

## Overview
This document defines the API design required for integrating the MatEx Portal with the RAP Validator system. The APIs handle real-time notifications for:
- Completed Checks
- Completed Cases
- Interim Case updates

The RAP Validator system must receive these notifications via HTTP POST and return a standardized 200 OK response.

## Base Configuration
- **Base URL:** _To be finalized_
- **Authentication:** Bearer Token
- **Headers:**
  - `Authorization: Bearer <token>`
  - `Content-Type: application/json`

---

## 1.1 Completed Check Notification

### Endpoint
`POST /matex/completed-check`

### Description
Notifies RAP Validator when a specific check is completed for validation processing.

### Request Body
```json
{
  "caseId": 0,
  "clientId": 0,
  "Projectid": 0,
  "Corporateid": 0,
  "Packageid": 0,
  "checkId": 0,
  "completionDetails": {
    "completedDate": "2025-05-29T10:30:00.000Z",
    "completedBy": "string",
    "checkStatus": "COMPLETED",
    "verificationResult": "string",
    "remarks": "string"
  }
}
```

### Response
```json
{
  "status": "SUCCESS",
  "message": "Check completion notification sent successfully",
  "validationId": "string"
}
```

---

## 1.2 Completed Case Notification

### Endpoint
`POST /matex/completed-case`

### Description
Notifies RAP Validator when an entire case is completed for final validation.

### Request Body
```json
{
  "caseId": 0,
  "clientId": 0,
  "Projectid": 0,
  "Corporateid": 0,
  "Packageid": 0,
  "caseDetails": {
    "caseRegistrationNumber": "string",
    "candidateName": "string",
    "completedDate": "2025-05-29T10:30:00.000Z",
    "completedBy": "string",
    "totalChecks": 0,
    "completedChecks": 0,
    "caseStatus": "COMPLETED"
  },
  "checksCompleted": [
    {
      "checkId": 0,
      "checkName": "string",
      "subChecks": [
        {
          "subCheckId": 0,
          "subCheckName": "string",
          "status": "COMPLETED"
        }
      ]
    }
  ]
}
```

### Response
```json
{
  "status": "SUCCESS",
  "message": "Case completion notification sent successfully",
  "validationId": "string",
  "timestamp": "2025-05-29T10:30:00.000Z"
}
```

---

## 1.3 Interim Case Notification

### Endpoint
`POST /rap/interim-case`

### Description
Notifies RAP Validator for interim validation while the case is in progress.

### Request Body
```json
{
  "caseId": 0,
  "clientId": 0,
  "projectid": 0,
  "corporateid": 0,
  "packageid": 0,
  "interimDetails": {
    "interimDate": "2025-05-29T10:30:00.000Z",
    "interimBy": "string",
    "interimType": "SCHEDULED|MANUAL|AUTO",
    "progressPercentage": 0,
    "remarks": "string"
  },
  "currentStatus": {
    "totalChecks": 0,
    "completedChecks": 0,
    "inProgressChecks": 0,
    "pendingChecks": 0
  },
  "checksCompleted": [
    {
      "checkId": 0,
      "checkName": "string",
      "subChecks": [
        {
          "subCheckId": 0,
          "subCheckName": "string",
          "status": "COMPLETED"
        }
      ]
    }
  ]
}
```

### Response
```json
{
  "status": "SUCCESS",
  "message": "Interim case notification sent successfully",
  "validationId": "string"
}
```

---

## Integration Notes
- All endpoints must validate authentication before processing.
- Ensure proper logging of request payloads for audit.
- Return 200 OK with JSON response format for all valid notifications.
- Validate enum values (e.g., `checkStatus`, `interimType`) against known types.
- Malformed or missing fields should result in `400 Bad Request` with descriptive error messages.

## Security Considerations
- Use HTTPS for all traffic.
- Rotate Bearer tokens periodically.
- Implement input validation and sanitization.

## Next Steps
- Finalize Base URL
- Share token generation mechanism
- Begin API integration testing post-implementation

---

## Implementation Details

### Technology Stack
- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Web Server:** Uvicorn (ASGI)
- **Auth:** Bearer Token validation using FastAPI Dependencies
- **Data Validation:** Pydantic Models
- **Logging:** Python standard logging for request tracking
- **Testing:** Pytest, HTTPX for integration tests

### Project Structure
```
matex_rap_validator/
├── app/
│   ├── main.py                  # FastAPI application entry point
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── notifications.py # Contains route handlers for all POST endpoints
│   ├── models/
│   │   └── schemas.py           # Pydantic models for request/response validation
│   ├── core/
│   │   └── config.py            # Configuration settings (auth tokens, env vars)
│   ├── services/
│   │   └── validator.py         # Business logic for handling notification payloads
│   ├── auth/
│   │   └── dependencies.py      # Auth handling using FastAPI Depends
│   └── utils/
│       └── logger.py            # Centralized logging setup
├── tests/
│   └── test_notifications.py    # Unit and integration tests
├── requirements.txt
└── README.md
```

### Development Steps
1. Define all request/response models using Pydantic in `schemas.py`.
2. Implement route logic in `notifications.py` for `/matex/completed-check`, `/matex/completed-case`, and `/rap/interim-case`.
3. Use dependency injection to validate Bearer token in all incoming requests via `dependencies.py`.
4. Add handler logic in `validator.py` to process and return appropriate responses.
5. Implement logging of all incoming requests and responses.
6. Write integration tests to verify each route and auth logic.

### Run Application
```bash
uvicorn app.main:app --reload
```

### Sample Endpoint Usage (cURL)
```bash
curl -X POST http://localhost:8000/matex/completed-check \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

