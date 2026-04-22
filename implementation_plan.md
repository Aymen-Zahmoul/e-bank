# Backend Architecture & Implementation Plan

This document outlines the professional implementation plan for the Python backend of the `e-bnk` application.

## 1. Goal Description

Develop a robust, professional backend API using Python. The objective is to establish a secure, organized structure with essential integrations such as Google Authentication verification, iOS universal links / Apple Sign-In support, and correct Git version control tracking.

> [!NOTE]
> By "pure Python," a modern asynchronous framework like **FastAPI** is heavily recommended over the standard library's `http.server`. FastAPI is native, standard-library-compliant (using `pydantic` and type hinting), and recognized as the industry standard for lightweight, high-performance professional Python APIs.

---

## 2. Proposed Directory Structure

To maintain a scalable and modular codebase, the backend will be set up in a dedicated `backend/` directory within the existing `e-bnk` project.

```text
backend/
├── .env                        # Local environment variables
├── .gitignore                  # Python-specific ignore rules
├── requirements.txt            # Project dependencies
├── main.py                     # Application entry point (FastAPI initialization)
├── api/                        # Route definitions (Controllers)
│   ├── __init__.py
│   ├── dependencies.py         # Reusable dependencies (e.g., get_db, auth)
│   ├── routes/
│       ├── auth.py             # Login, OAuth routes
│       └── users.py            # User management routes
├── core/                       # Core configurations
│   ├── __init__.py
│   ├── config.py               # Environment parsing
│   └── security.py             # Password hashing, JWT creation/decoding
├── services/                   # Business logic layers
│   ├── __init__.py
│   ├── google_auth.py          # Google token verification logic
│   └── apple_auth.py           # Apple verifications & logic
├── models/                     # ORM Models and Pydantic schemas
│   ├── __init__.py
│   ├── domain.py               # Database schemas
│   └── schemas.py              # Pydantic schemas for request/response
└── utils/                      # Helper functions
```

---

## 3. Integrations Setup

### 3.1. Google Verification
For Google Verification, we will expose an endpoint that accepts a Google OAuth ID Token from the frontend. The backend will use `google-auth` to securely verify this token against Google's servers.

```python
# Conceptual implementation
from google.oauth2 import id_token
from google.auth.transport import requests

def verify_google_token(token: str):
    try:
        # Verify token and extract user details
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        return idinfo
    except ValueError:
        # Invalid token
        return None
```

### 3.2. iOS Verification ("iOS Verif thing")
There are two distinct iOS integrations. Please clarify in the **Open Questions** which one is required, or if both are:
1. **Apple Sign-In Verification**: Similar to Google, verifying identity tokens granted by Apple.
2. **Apple App Site Association (AASA)**: Serving a specialized `.well-known/apple-app-site-association` static JSON configuration for iOS Universal Links, allowing iOS apps to intercept web URLs.

### 3.3. Git Ignore Configuration

The `backend/.gitignore` will comprehensively cover standard Python artifacts to keep the repository clean.

```text
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Project specifics
.vscode/
.idea/
*.db
*.sqlite3
```

---

## 4. User Review Required

> [!IMPORTANT]
> **Framework selection:** 
> Will we proceed with **FastAPI**? It is the most professional standard for "pure Python" API development today. Relying purely on Python's built-in `http` or `wsgi` libraries without a framework is strongly discouraged for production security, routing, and maintainability.

> [!CAUTION]
> **Database strategy:**
> What database should be used? Options include SQLite (for rapid prototyping/small scale) or PostgreSQL (for production readiness).

---

## 5. Open Questions

1. **Framework Confirmation:** Are you comfortable with FastAPI, or did "pure Python" explicitly mean *zero external packages* (standard library only)?
2. **iOS Specifics:** Does the "iOS verif thing" refer to **"Sign in with Apple" authentication**, or the **Universal Links file** (`apple-app-site-association`), or both?
3. **Database:** Should we integrate a standard database via an ORM like SQLAlchemy, or do we start with mock data and add the database later?

---

## 6. Verification Plan

### Automated Tests
- Create Python unit tests (`pytest`) covering the Google JWT token verification logic.
- Verify status codes on standard endpoints (e.g. `GET /health` returns `200 OK`).

### Manual Verification
- Start the server using `uvicorn main:app --reload`.
- Hit the `/docs` auto-generated Swagger UI to verify all routes load.
- Validate that the iOS universal link configuration (`.well-known/apple-app-site-association`) is served as `application/json` without an extension.
