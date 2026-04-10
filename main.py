from fastapi import FastAPI
from database import init_db, engine
from routers.trip import router as trip_router
from routers.currencies import router as currencies_router
from routers.users import router as users_router
from routers.expenses import router as expenses_router
from routers.expense_allocations import router as expense_allocations_router
from routers.expense_types import router as expense_types_router
from routers.trip_members import router as trip_members_router
from routers.trip_budget_categories import router as trip_budget_categories_router
from routers.notifications import router as notifications_router

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(_):
    await init_db()
    print("Запуск")
    yield
    print("Выключение")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(trip_router)
app.include_router(currencies_router)
app.include_router(users_router)
app.include_router(expenses_router)
app.include_router(expense_allocations_router)
app.include_router(expense_types_router)
app.include_router(trip_members_router)
app.include_router(trip_budget_categories_router)
app.include_router(notifications_router)

@app.get('/')
def root():
    return {"Real": "Python"}