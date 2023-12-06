from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated

import models
from config.database import engine, SessionLocal


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   

db_dependency = Anotated(Session, Depends(get_db))

@app.get('/', tags=['ROOT'])
def root() -> dict:
    return {'name': 'Nick'}