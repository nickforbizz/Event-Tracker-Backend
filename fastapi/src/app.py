from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
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
router = APIRouter()
models.Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   


@app.get('/home', tags=['ROOT'])
def root() -> dict:
    return {'msg': 'Welcome '}

@app.get('/', status_code=status.HTTP_200_OK, tags=['Users'])
async def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@app.get('/user/{user_id}', status_code=status.HTTP_200_OK ,tags=['Users'])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@app.post('/user', status_code=status.HTTP_201_CREATED ,tags=['Users'])
async def createUser(user: UserBase, db: Session=Depends(get_db)):
    user = models.User(**user.model_dump())
    db.add(user)
    db.commit()
    return user

@app.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Users'])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return None  # Return None with status_code=204 (No Content)