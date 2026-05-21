from contextlib import asynccontextmanager

from fastapi import FastAPI

import models
from database import engine
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.get("/")
async def home():
    return {"message": "Async Library Management System is running"}