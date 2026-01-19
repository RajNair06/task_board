from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.auth import router as auth_router
from routers.boards import router as boards_router
from routers.cards import router as cards_router
from routers.sockets import router as ws_router
import asyncio
from utils.connection_manager import manager
from utils.feed_utils import activity_feed_dispatcher,redis_listener
from db.init_db import init_db



@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    redis_task = asyncio.create_task(redis_listener(manager))
    yield
    
    redis_task.cancel()
    try:
        await redis_task
    except asyncio.CancelledError:
        pass


app=FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(boards_router)
app.include_router(cards_router)
app.include_router(ws_router)
