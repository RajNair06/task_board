from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.auth import router as auth_router
from routers.boards import router as boards_router
from routers.cards import router as cards_router

from db.init_db import init_db



@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield


app=FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(boards_router)
app.include_router(cards_router)
