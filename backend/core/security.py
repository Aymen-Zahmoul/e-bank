# Security utils like password hashing and JWT
from datetime import datetime, timedelta
from typing import Any, Union, Optional
from core.config import settings

# This would use standard libraries like passlib and jose in a full real setup
# Mocking for the foundation, per standard structure

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # return pwd_context.verify(plain_password, hashed_password)
    return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    # return pwd_context.hash(password)
    return password

def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    # We would use python-jose to create JWT here
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    # mock token
    return f"mock_token_for_{subject}"
