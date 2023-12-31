from fastapi import FastAPI
from .routers import UserController
 
app = FastAPI()


# Use the `app` router from user_controller.py
app.include_router(UserController.routers, prefix="/users", tags=["Users"])
 


@app.get('/home', tags=['ROOT'])
def root() -> dict:
    return {'msg': 'Welcome '}

    