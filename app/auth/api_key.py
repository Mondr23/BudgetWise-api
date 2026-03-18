# API key security for analytics endpoints

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "my-secret-key"

api_key_header = APIKeyHeader(name="x-api-key")


def verify_api_key(api_key: str = Depends(api_key_header)):
    """
    Validates API key
    """

    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    return api_key