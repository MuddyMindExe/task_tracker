from fastapi import FastAPI

from src.tasks.routers import tasks_router
from src.users.routers import users_router

app = FastAPI()
app.include_router(tasks_router)
app.include_router(users_router)

@app.get("/")
def main():
    return {"message": "Task Tracker API"}
