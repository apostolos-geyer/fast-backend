from fastapi import FastAPI
from user.endpoints import user_router as user_router
from auth.endpoints import router as auth_router
from database import create_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_tables()


@app.get("/")
def lol():
    return {"lol": "lol"}


app.include_router(user_router)
app.include_router(auth_router)

