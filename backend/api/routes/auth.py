from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from services.google_auth import verify_google_token
from services.apple_auth import verify_apple_token

router = APIRouter()

class GoogleLoginRequest(BaseModel):
    id_token: str

class AppleLoginRequest(BaseModel):
    id_token: str

@router.post("/google")
def google_login(payload: GoogleLoginRequest):
    user_info = verify_google_token(payload.id_token)
    if not user_info:
        raise HTTPException(status_code=400, detail="Invalid Google Token")
    
    return {"message": "Google verification successful", "user": user_info}

@router.post("/apple")
def apple_login(payload: AppleLoginRequest):
    user_info = verify_apple_token(payload.id_token)
    if not user_info:
        raise HTTPException(status_code=400, detail="Invalid Apple Token")
    
    return {"message": "Apple verification successful", "user": user_info}
