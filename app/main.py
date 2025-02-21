import asyncio
from fastapi import FastAPI
from app.routes import users, referrals
from app.database import init_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    """Инициализирует базу данных при запуске приложения."""
    await init_db()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(referrals.router, prefix="/referrals", tags=["Referrals"])