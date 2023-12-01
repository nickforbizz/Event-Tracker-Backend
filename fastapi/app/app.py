from fastapi import FastAPI


app = FastAPI()



@app.get('/', tags=['ROOT'])
def root() -> dict:
    return {'name': 'Nick'}