from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth, users

app = FastAPI(title="e-bnk API", version="1.0.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict to frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apple App Site Association
@app.get("/.well-known/apple-app-site-association")
def get_apple_app_site_association():
    aasa = {
        "applinks": {
            "apps": [],
            "details": [
                {
                    "appID": "TEAMID.com.yourcompany.ebnk",
                    "paths": ["*"]
                }
            ]
        }
    }
    return Response(content=str(aasa).replace("'", '"'), media_type="application/json")


app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Welcome to the e-bnk API"}
