from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Union

import models
from database import engine, SessionLocal
from model_validators import EventBase
from src.dependencies import get_db 

routers = APIRouter()
models.Base.metadata.create_all(bind=engine)




@routers.get('/events', status_code=status.HTTP_200_OK, tags=['Events'])
async def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = db.query(models.User).offset(skip).limit(limit).all()
    return events


@routers.get('/event/{event_id}', status_code=status.HTTP_200_OK ,tags=['Events'])
async def get_event(event_id: int, q: Union[str, None] = None, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return event

@routers.post('/event', status_code=status.HTTP_201_CREATED ,tags=['Events'])
async def createEvent(event: EventBase, db: Session=Depends(get_db)):
    event = models.Event(**event.model_dump())
    db.add(event)
    db.commit()
    return event

#function to update event
@routers.put('/event/{event_id}', status_code=status.HTTP_202_ACCEPTED, tags=['Events'])
async def update_event(event_id: int, event: EventBase, db: Session = Depends(get_db)):
    event_query = db.query(models.Event).filter(models.Event.id == event_id)

    if event_query.first() is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event_query.update(event.model_dump(), synchronize_session=False)
    db.commit()

    return event_query.first()

@routers.delete('/event/{event_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Events'])
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()

    # Return None with status_code=204 (No Content)
    return None  