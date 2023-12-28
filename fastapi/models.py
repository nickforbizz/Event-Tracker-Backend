from sqlalchemy import create_engine, Column, Integer, String, DateTime, Sequence, ForeignKey
from datetime import datetime

from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    active = Column(Integer, default = 0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, Sequence("event_id_seq"), primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(255))
    fk_user = Column(Integer)
    active = Column(Integer, default = 0)
    created_at = Column(DateTime, default=datetime.utcnow)
