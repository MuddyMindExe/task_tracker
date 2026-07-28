from fastapi import APIRouter, HTTPException

from src.tasks.service import task_service
from src.tasks.schemas import Task, TaskCreate, TaskUpdate
from src.tasks.constants import TaskStatus

tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@tasks_router.get("")
def show_tasks(title: str | None = None, status: TaskStatus | None = None) -> list[Task | None]:
    return task_service.get_tasks(title, status)

@tasks_router.post("")
def add_task(task_data: TaskCreate) -> Task:
    return task_service.add_task(task_data)

@tasks_router.get("/{task_id}")
def show_task(task_id: int) -> Task:
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@tasks_router.patch("/{task_id}")
def change_task(task_id: int, task_data: TaskUpdate) -> Task:
    task = task_service.change_task(task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@tasks_router.delete("/{task_id}")
def delete_task(task_id: int):
    task = task_service.delete_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
