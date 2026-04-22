from fastapi import APIRouter, Depends
from models.schemas import UserResponse
from api.dependencies import get_current_active_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_current_user(
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get current user.
    """
    return {"email": current_user["email"], "name": "Current User", "id": 1}
