from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated

import models
from database import engine, SessionLocal
from model_validators import UserBase, EventBase

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   


@app.get('/', tags=['ROOT'])
def root() -> dict:
    return {'msg': 'Welcome '}


@app.get('/', status_code=status.HTTP_201_CREATED ,tags=['Users'])
async def createUser(user: UserBase, db: Session=Depends(get_db)):
    user = models.User(**user.model_dump())
    db.add(user)
    db.commit()
    return user