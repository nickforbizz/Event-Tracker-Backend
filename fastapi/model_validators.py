from pydantic import BaseModel, PositiveInt

class UserBase(BaseModel):
    username: str
    active: bool

class EventBase(BaseModel):
    name: str
    description: str
    fk_user: PositiveInt