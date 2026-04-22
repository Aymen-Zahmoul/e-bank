from google.oauth2 import id_token
from google.auth.transport import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")

def verify_google_token(token: str):
    """
    Verifies a Google OAuth ID token.
    """
    try:
        # Verify the token against Google
        if GOOGLE_CLIENT_ID == "YOUR_GOOGLE_CLIENT_ID":
            # Mock mode logic if not configured
            return {"email": "mockuser@google.com", "name": "Mock User"}
            
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        return idinfo
    except ValueError as e:
        # Invalid token
        print(f"Google Token Verification Failed: {e}")
        return None
