from fastapi import FastAPI
from database import init_db, engine
from routers.trip import router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(_):
    await init_db()
    print("Запуск")
    yield
    print("Выключение")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(router)



@app.get('/')
def root():
    return {"Real": "Python"}