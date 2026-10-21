from fastapi import FastAPI

from src.database import Base, engine

from src.tasks.routers import tasks_router
from src.tasks.models import Tasks

from src.users.routers import users_router
from src.users.models import Users

app = FastAPI()
app.include_router(tasks_router)
app.include_router(users_router)

Base.metadata.create_all(engine)

@app.get("/")
def main():
    return {"message": "Task Tracker API"}
