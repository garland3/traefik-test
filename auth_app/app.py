from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from jose import jwt
import httpx
import os
from dotenv import load_dotenv
from typing import Optional
import secrets

load_dotenv()

# Validate required environment variables
required_env_vars = [
    'CLIENT_ID',
    'CLIENT_SECRET',
    'AUTHORITY',
    'OAUTH_PROVIDER'
]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_vars)}. "
        "Please ensure all required variables are set in your .env file."
    )

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    USERINFO_URL = "https://graph.microsoft.com/oidc/userinfo"
elif PROVIDER == 'auth0':
    AUTH_URL = f"https://{AUTHORITY}/authorize"
    TOKEN_URL = f"https://{AUTHORITY}/oauth/token"
    USERINFO_URL = f"https://{AUTHORITY}/userinfo"
else:
    raise ValueError(f"Unsupported OAuth provider: {PROVIDER}")

# print out all the environment variables, use *** for secret
print(f"CLIENT_ID: {CLIENT_ID}")
# print(f"CLIENT_SECRET: ***")
#check if CLIENT_SECRET is set
if CLIENT_SECRET:
    print(f"CLIENT_SECRET: ***")
else:
    print(f"CLIENT_SECRET: not set")
print(f"AUTHORITY: {AUTHORITY}")
print(f"PROVIDER: {PROVIDER}")
print(f"REDIRECT_URI: {REDIRECT_URI}")
print(f"SCOPE: {SCOPE}")


@app.get("/")
async def root(request: Request):
    session_id = request.cookies.get("session_id")
    print(f"Root route - Session ID: {session_id}")
    print(f"Root route - Available sessions: {list(sessions.keys())}")
    
    if not session_id or session_id not in sessions:
        print("Root route - No valid session found, serving login page")
        return FileResponse("static/index.html")
    
    print(f"Root route - Found session data: {sessions[session_id]}")
    return FileResponse("static/dashboard.html")

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
        print(f"Received code: {code}")
        print(f"Using TOKEN_URL: {TOKEN_URL}")
        print(f"Using REDIRECT_URI: {REDIRECT_URI}")
        
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
            
            print(f"Token response status: {token_response.status_code}")
            print(f"Token response body: {token_response.text}")
            
            if token_response.status_code != 200:
                raise HTTPException(
                    status_code=token_response.status_code,
                    detail=f"Token exchange failed: {token_response.text}"
                )
                
            token_data = token_response.json()
            
            # Get user info
            userinfo_response = await client.get(
                USERINFO_URL,
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )
            
            print(f"Userinfo response status: {userinfo_response.status_code}")
            print(f"Userinfo response body: {userinfo_response.text}")
            
            if userinfo_response.status_code != 200:
                raise HTTPException(
                    status_code=userinfo_response.status_code,
                    detail=f"Userinfo request failed: {userinfo_response.text}"
                )
                
            userinfo = userinfo_response.json()
            
            # Create session
            session_id = secrets.token_urlsafe(32)
            sessions[session_id] = userinfo
            
            response = RedirectResponse(url="/")
            response.set_cookie(key="session_id", value=session_id, httponly=True)
            return response
            
    except Exception as e:
        print(f"Error in get_token: {str(e)}")
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