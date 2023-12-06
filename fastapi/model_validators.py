from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class EventBase(BaseModel):
    name: str
    description: str
    fk_user: int