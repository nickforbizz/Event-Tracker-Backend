from fastapi import FastAPI, Depends, HTTPException, status
from dotenv import load_dotenv
import os

from .routers import UserController, EventController
 
app = FastAPI()
# Load .env file
load_dotenv()
# Use the `app` router from user_controller.py
app.include_router(UserController.routers, prefix="/users", tags=["Users"])
app.include_router(EventController.routers, prefix="/events", tags=["Events"])

# Set up your Google OAuth 2.0 credentials
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_SCOPES = ["openid", "profile", "email"]




@app.get('/home', tags=['ROOT'])
def root() -> dict:
    return {'msg': 'Welcome '}
  