from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum

# --- Enums ---

class CheckStatus(str, Enum):
    COMPLETED = "COMPLETED"

class CaseStatus(str, Enum):
    COMPLETED = "COMPLETED"

class InterimType(str, Enum):
    SCHEDULED = "SCHEDULED"
    MANUAL = "MANUAL"
    AUTO = "AUTO"

# --- Base Models ---

class BaseResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    status: str = "SUCCESS"
    message: str
    validation_id: str = Field(..., alias="validationId")

# --- Completed Check ---

class CompletionDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    completed_date: datetime = Field(..., alias="completedDate")
    completed_by: str = Field(..., alias="completedBy")
    check_status: CheckStatus = Field(..., alias="checkStatus")
    verification_result: str = Field(..., alias="verificationResult")
    remarks: str

class CompletedCheckRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    case_id: int = Field(..., alias="caseId")
    client_id: int = Field(..., alias="clientId")
    project_id: int = Field(..., alias="projectId")
    corporate_id: int = Field(..., alias="corporateId")
    package_id: int = Field(..., alias="packageId")
    check_id: int = Field(..., alias="checkId")
    completion_details: CompletionDetails = Field(..., alias="completionDetails")

class CompletedCheckResponse(BaseResponse):
    message: str = "Check completion notification sent successfully"

# --- Completed Case ---

class CaseDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    case_registration_number: str = Field(..., alias="caseRegistrationNumber")
    candidate_name: str = Field(..., alias="candidateName")
    completed_date: datetime = Field(..., alias="completedDate")
    completed_by: str = Field(..., alias="completedBy")
    total_checks: int = Field(..., alias="totalChecks")
    completed_checks: int = Field(..., alias="completedChecks")
    case_status: CaseStatus = Field(..., alias="caseStatus")

class SubCheck(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    sub_check_id: int = Field(..., alias="subCheckId")
    sub_check_name: str = Field(..., alias="subCheckName")
    status: CheckStatus

class CheckCompleted(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    check_id: int = Field(..., alias="checkId")
    check_name: str = Field(..., alias="checkName")
    sub_checks: List[SubCheck] = Field(..., alias="subChecks")

class CompletedCaseRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    case_id: int = Field(..., alias="caseId")
    client_id: int = Field(..., alias="clientId")
    project_id: int = Field(..., alias="projectId")
    corporate_id: int = Field(..., alias="corporateId")
    package_id: int = Field(..., alias="packageId")
    case_details: CaseDetails = Field(..., alias="caseDetails")
    checks_completed: List[CheckCompleted] = Field(..., alias="checksCompleted")

class CompletedCaseResponse(BaseResponse):
    message: str = "Case completion notification sent successfully"
    timestamp: datetime

# --- Interim Case ---

class InterimDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    interim_date: datetime = Field(..., alias="interimDate")
    interim_by: str = Field(..., alias="interimBy")
    interim_type: InterimType = Field(..., alias="interimType")
    progress_percentage: int = Field(..., alias="progressPercentage")
    remarks: str

class CurrentStatus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    total_checks: int = Field(..., alias="totalChecks")
    completed_checks: int = Field(..., alias="completedChecks")
    in_progress_checks: int = Field(..., alias="inProgressChecks")
    pending_checks: int = Field(..., alias="pendingChecks")

class InterimCaseRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    case_id: int = Field(..., alias="caseId")
    client_id: int = Field(..., alias="clientId")
    project_id: int = Field(..., alias="projectId")
    corporate_id: int = Field(..., alias="corporateId")
    package_id: int = Field(..., alias="packageId")
    interim_details: InterimDetails = Field(..., alias="interimDetails")
    current_status: CurrentStatus = Field(..., alias="currentStatus")
    checks_completed: List[CheckCompleted] = Field(..., alias="checksCompleted")

class InterimCaseResponse(BaseResponse):
    message: str = "Interim case notification sent successfully"

