from fastapi import FastAPI

from src.database import engine, metadata_obj

from src.tasks.routers import tasks_router
from src.tasks.models import tasks

from src.users.routers import users_router
from src.users.models import users

app = FastAPI()
app.include_router(tasks_router)
app.include_router(users_router)

metadata_obj.create_all(engine)

@app.get("/")
def main_page():
    return {"message": "Task Tracker API"}
