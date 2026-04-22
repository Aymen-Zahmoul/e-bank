from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import verify_password
from models.schemas import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/auth/login"
)

def get_current_user(token: str = Depends(reusable_oauth2)):
    # Mock validation of JWT token
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return {"user_id": "123", "email": "mock@example.com"}

def get_current_active_user(
    current_user: dict = Depends(get_current_user),
):
    # Mock checking if user is active
    return current_user
