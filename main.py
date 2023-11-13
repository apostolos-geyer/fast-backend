from fastapi import FastAPI
from user.endpoints import router as user_router
from database import create_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_tables()


@app.get("/")
def lol():
    return {"lol": "lol"}


app.include_router(user_router)