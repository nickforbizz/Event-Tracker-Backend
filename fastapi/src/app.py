from fastapi import FastAPI, Depends, HTTPException, requests, status, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from google.oauth2 import id_token
from dotenv import load_dotenv
import os

from .routers import UserController, EventController
 
app = FastAPI()
# Load .env file
load_dotenv()


# Define OAuth 2.0 configuration
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="token",
    authorizationUrl="authorize",
)

# Set up your Google OAuth 2.0 credentials
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# Google OAuth 2.0 authorization URL
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"

# Define callback URL
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# Define scopes (e.g., profile information)
GOOGLE_SCOPES = ["openid", "profile", "email"]




# Use the `app` router from user_controller.py
app.include_router(UserController.routers, prefix="/users", tags=["Users"])
app.include_router(EventController.routers, prefix="/events", tags=["Events"])
 

# Add routes for authentication
# Google callback
@app.get('/login')
async def login():
    google_provider_cfg_url = 'https://accounts.google.com/.well-known/openid-configuration'
    google_provider_cfg = requests.get(google_provider_cfg_url).json()
    
    # Redirect users to Google for authentication
    return {
        "redirect_uri": "http://localhost:8000/callback",
        "authorization_url": google_provider_cfg["authorization_endpoint"],
        "client_id": CLIENT_ID,
    }

# Google callback
@app.get('/callback')
async def callback(code: str, state: str, token: str = Depends(oauth2_scheme)):
    token_endpoint = 'https://oauth2.googleapis.com/token'
    token_response = id_token.fetch_token(token_endpoint,
                                          authorization_response=code,
                                          client_id=CLIENT_ID)
    
    # Use token_response to get user information
    user_info = id_token.verify_oauth2_token(token_response['id_token'],
                                             requests.Request(),
                                             CLIENT_ID)
    
    # Your logic after authentication
    return {"token": token, "user_info": user_info}
@app.get('/home', tags=['ROOT'])
def root() -> dict:
    return {'msg': 'Welcome '}

    