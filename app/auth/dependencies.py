from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from app.core.config import settings

reusable_oauth2 = HTTPBearer(
    scheme_name="Bearer",
    auto_error=False
)

def validate_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(reusable_oauth2)):
    """
    Validates the bearer token from the Authorization header.
    
    Handles missing credentials by raising a 401 Unauthorized error.
    """
    if credentials is None or credentials.scheme != "Bearer" or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if credentials.credentials != settings.API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True

