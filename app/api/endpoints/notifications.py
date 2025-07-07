from fastapi import APIRouter, Depends
from datetime import datetime
import uuid

from app.models.schemas import (
    CompletedCheckRequest, CompletedCheckResponse,
    CompletedCaseRequest, CompletedCaseResponse,
    InterimCaseRequest, InterimCaseResponse
)
from app.auth.dependencies import validate_token
from app.services import validator
from app.utils.logger import logger

router = APIRouter()

@router.post("/matex/completed-check", response_model=CompletedCheckResponse)
async def completed_check(request: CompletedCheckRequest, is_authenticated: bool = Depends(validate_token)):
    """
    Receives notification for a completed check.
    """
    logger.info(f"Received /matex/completed-check request: {request.model_dump(by_alias=True)}")
    validator.process_completed_check(request)
    response = CompletedCheckResponse(validation_id=str(uuid.uuid4()))
    logger.info(f"Sending /matex/completed-check response: {response.model_dump(by_alias=True)}")
    return response

@router.post("/matex/completed-case", response_model=CompletedCaseResponse)
async def completed_case(request: CompletedCaseRequest, is_authenticated: bool = Depends(validate_token)):
    """
    Receives notification for a completed case.
    """
    logger.info(f"Received /matex/completed-case request: {request.model_dump(by_alias=True)}")
    validator.process_completed_case(request)
    response = CompletedCaseResponse(
        validation_id=str(uuid.uuid4()),
        timestamp=datetime.utcnow()
    )
    logger.info(f"Sending /matex/completed-case response: {response.model_dump(by_alias=True)}")
    return response

@router.post("/rap/interim-case", response_model=InterimCaseResponse)
async def interim_case(request: InterimCaseRequest, is_authenticated: bool = Depends(validate_token)):
    """
    Receives notification for an interim case update.
    """
    logger.info(f"Received /rap/interim-case request: {request.model_dump(by_alias=True)}")
    validator.process_interim_case(request)
    response = InterimCaseResponse(validation_id=str(uuid.uuid4()))
    logger.info(f"Sending /rap/interim-case response: {response.model_dump(by_alias=True)}")
    return response



