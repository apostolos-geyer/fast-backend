from fastapi import FastAPI

from app.api import user_router, session_router
from app.database import create_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_tables()


@app.get("/")
def lol():
    return {"lol": "lol"}


app.include_router(session_router)
app.include_router(user_router)

