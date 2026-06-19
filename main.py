from contextlib import asynccontextmanager

from fastapi import FastAPI

from sqlalchemy.future import select

import models

from auth import hash_password

from database import AsyncSessionLocal

from routes import router

import os

from dotenv import load_dotenv


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with AsyncSessionLocal() as db:

        admin_email = os.getenv(
            "ADMIN_EMAIL"
        )

        result = await db.execute(

            select(models.User).where(

                models.User.email
                == admin_email
            )
        )

        admin = result.scalar_one_or_none()

        if admin is None:

            admin_user = models.User(

                name=os.getenv(
                    "ADMIN_NAME"
                ),

                email=admin_email,

                phone_number="00000000000",

                password=hash_password(

                    os.getenv(
                        "ADMIN_PASSWORD"
                    )
                ),

                role="admin"
            )

            db.add(
                admin_user
            )

            await db.commit()

    yield


app = FastAPI(

    lifespan=lifespan
)


app.include_router(
    router
)


@app.get("/")
async def home():

    return {

        "message":
        "Async Library Management System is running"
    }