from fastapi import FastAPI

from routes import router


app = FastAPI()

app.include_router(router)


@app.get("/")
async def home():
    return {"message": "Async Library Management System is running"}