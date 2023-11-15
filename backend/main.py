from fastapi import FastAPI

from backend.api import user_router, session_router
from backend.database import create_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_tables()


@app.get("/")
def lol():
    return {"lol": "lol"}


app.include_router(session_router)
app.include_router(user_router)


if __name__ == "__main__":
    import json

    app_dict = app.openapi()


    print(app.openapi())

