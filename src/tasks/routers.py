from fastapi import APIRouter, HTTPException, Path, Query, Depends
from fastapi import status as statuscode

from typing import Annotated

from src.tasks.dependencies import TaskService, get_task_service
from src.tasks.schemas import Task, TaskCreate, TaskUpdate
from src.tasks.constants import TaskStatus

tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@tasks_router.get("")
def show_tasks(
        task_service: Annotated[TaskService, Depends(get_task_service)],
        title: Annotated[str | None, Query(min_length=1, max_length=256, description="Filter tasks by title")] = None,
        status: Annotated[TaskStatus | None, Query(description="Filter tasks by status")] = None) -> dict[int, Task]:

    return task_service.get_tasks(title, status)

@tasks_router.get("/{task_id}")
def show_task(task_service: Annotated[TaskService, Depends(get_task_service)],
              task_id: Annotated[int, Path(ge=1, description="Task identifier")]) -> Task:

    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=statuscode.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@tasks_router.post("", status_code=statuscode.HTTP_201_CREATED)
def add_task(task_data: TaskCreate, task_service: Annotated[TaskService, Depends(get_task_service)]) -> Task:

    return task_service.add_task(task_data)

@tasks_router.patch("/{task_id}")
def change_task(
        task_id: Annotated[int, Path(ge=1, description="Task identifier")],
        task_data: TaskUpdate,
        task_service: Annotated[TaskService, Depends(get_task_service)]) -> Task:

    task = task_service.change_task(task_id, task_data)
    if not task:
        raise HTTPException(status_code=statuscode.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@tasks_router.delete("/{task_id}", status_code=statuscode.HTTP_204_NO_CONTENT)
def delete_task(
        task_id: Annotated[int, Path(ge=1, description="Task identifier")],
        task_service: Annotated[TaskService, Depends(get_task_service)]) -> None:

    task = task_service.delete_task(task_id)
    if not task:
        raise HTTPException(status_code=statuscode.HTTP_404_NOT_FOUND, detail="Task not found")
