from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
import httpx
import os
from dotenv import load_dotenv
from typing import Optional
import secrets

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth configuration
PROVIDER = os.getenv('OAUTH_PROVIDER', 'azure')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
AUTHORITY = os.getenv('AUTHORITY')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost/getAToken')
SCOPE = os.getenv('SCOPE', 'openid profile email').split()

# Session management
sessions = {}

# Provider-specific configuration
if PROVIDER == 'azure':
    AUTH_URL = f"{AUTHORITY}/oauth2/v2.0/authorize"
    TOKEN_URL = f"{AUTHORITY}/oauth2/v2.0/token"
    USERINFO_URL = f"{AUTHORITY}/v2.0/me"
elif PROVIDER == 'auth0':
    AUTH_URL = f"https://{AUTHORITY}/authorize"
    TOKEN_URL = f"https://{AUTHORITY}/oauth/token"
    USERINFO_URL = f"https://{AUTHORITY}/userinfo"
else:
    raise ValueError(f"Unsupported OAuth provider: {PROVIDER}")

@app.get("/")
async def root(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        return RedirectResponse(url="/login")
    return RedirectResponse(url="http://localhost/chatbot")

@app.get("/login")
async def login():
    state = secrets.token_urlsafe(32)
    auth_url = (
        f"{AUTH_URL}?"
        f"client_id={CLIENT_ID}&"
        f"response_type=code&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope={' '.join(SCOPE)}&"
        f"state={state}"
    )
    return RedirectResponse(url=auth_url)

@app.get("/getAToken")
async def get_token(code: str, state: str):
    try:
        async with httpx.AsyncClient() as client:
            # Exchange code for token
            token_response = await client.post(
                TOKEN_URL,
                data={
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": REDIRECT_URI,
                },
            )
            token_data = token_response.json()
            
            # Get user info
            userinfo_response = await client.get(
                USERINFO_URL,
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )
            userinfo = userinfo_response.json()
            
            # Create session
            session_id = secrets.token_urlsafe(32)
            sessions[session_id] = userinfo
            
            response = RedirectResponse(url="/")
            response.set_cookie(key="session_id", value=session_id, httponly=True)
            return response
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("session_id")
    return response

@app.get("/user")
async def get_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return sessions[session_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000) 