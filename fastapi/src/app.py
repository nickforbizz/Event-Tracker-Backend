from fastapi import FastAPI
from .routers import UserController, EventController
 
app = FastAPI()


# Use the `app` router from user_controller.py
app.include_router(UserController.routers, prefix="/users", tags=["Users"])
app.include_router(EventController.routers, prefix="/events", tags=["Events"])
 


@app.get('/home', tags=['ROOT'])
def root() -> dict:
    return {'msg': 'Welcome '}

    