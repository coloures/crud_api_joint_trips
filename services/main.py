from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


@app.get('/')
async def index():
    return {"Real": "Python"}