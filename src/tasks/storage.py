import json
from abc import ABC, abstractmethod

from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from src.database import engine

from src.tasks.schemas import Task, TaskCreate
from src.tasks.models import tasks

class TaskStorage(ABC):
    @abstractmethod
    def show_all(self) -> dict[int, Task]:...

    @abstractmethod
    def get_task(self, task_id: int) -> Task | None:...

    @abstractmethod
    def add_task(self, task_data: TaskCreate):...

    @abstractmethod
    def delete_task(self, task_id: int) -> Task | None:...

    @abstractmethod
    def change_task(self, task_id: int, **changes) -> Task | None:...

class TaskInMemoryStorage(TaskStorage):
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.current_id = 1

    def show_all(self) -> dict[int, Task]:
        return self.tasks

    def get_task(self, task_id: int) -> Task | None:
        return self.tasks.get(task_id)

    def add_task(self, task_data) -> Task | None:
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            user_id=task_data.user_id
        )
        self.tasks[self.get_id()] = task
        self.current_id += 1
        return task

    def delete_task(self, task_id: int) -> Task | None:
        return self.tasks.pop(task_id, None)

    def change_task(self, task_id: int, **changes) -> Task | None:
        task = self.tasks.get(task_id)
        if not task:
            return None
        for param, value in changes.items():
            if hasattr(task, param):
                if value is not None:
                    setattr(task, param, value)

        return task

    def get_id(self):
        return self.current_id

    def set_id(self, new_id: int):
        if not isinstance(new_id, int):
            raise TypeError("Invalid new_id value")

        self.current_id = new_id

class TaskJsonStorage(TaskStorage):
    def __init__(self, file="src/storage/tasks.json"):
        self.file = file

    def show_all(self) -> dict[int, Task]:
        with open(self.file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return {task_id: Task.model_validate(task) for task_id, task in data.items()}

    def get_task(self, task_id: int) -> Task | None:
        with open(self.file, "r", encoding="utf-8") as file:
            data = json.load(file)
        raw = data.get(str(task_id))
        return Task.model_validate(raw) if raw else None

    def add_task(self, task_data) -> Task | None:
        with open(self.file, "r", encoding="utf-8") as file:
            data = json.load(file)
            task_id = str(self.get_id())

        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            user_id=task_data.user_id
        )
        task = task.model_dump()
        data[task_id] = task
        with open(self.file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
        return task

    def delete_task(self, task_id: int) -> Task | None:
        with open(self.file, "r", encoding="utf-8") as file:
            data = json.load(file)

        task = data.pop(str(task_id), None)

        with open(self.file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

        return Task.model_validate(task) if task else None

    def change_task(self, task_id: int, **changes) -> Task | None:
        with open(self.file, "r", encoding="utf-8") as file:
            data = json.load(file)

        task = Task.model_validate(data.pop(str(task_id), None))
        if not task:
            return None
        for param, value in changes.items():
            if hasattr(task, param):
                if value is not None:
                    setattr(task, param, value)
        data[str(task_id)] = task.model_dump()

        with open(self.file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

        return task

    def get_id(self):
        with open(self.file, "r", encoding="utf-8") as file:
            data = json.load(file)
            return max(map(int, data.keys()), default=0) + 1

class TaskSQLStorage(TaskStorage):
    def show_all(self) -> dict[int, Task]:
        query = select(tasks)

        with Session(engine) as session:
            return session.scalar(query)

    def get_task(self, task_id: int) -> Task | None:
        query = select(Tasks).where(Tasks.id==task_id)

        with Session(engine) as session:
            return session.scalar(query)

    def add_task(self, task_data: TaskCreate):
        with Session(engine) as session:
            task = Tasks(
                title=task_data.title,
                description=task_data.description,
                status=task_data.status,
                user_id=task_data.user_id
            )

            session.add(task)

    def delete_task(self, task_id: int) -> Task | None:
        query = delete(Tasks).where(Task.id==task_id)

        with Session(engine) as session:
            session.delete(query)

    def change_task(self, task_id: int, **changes) -> Task | None:
        query = update(Tasks).where(Tasks.id==task_id).values(**changes)

        with Session(engine) as session:
            session.execute(query)

            getq = select(Tasks).where(Tasks.id==task_id)
            return session.execute(getq).scalar()

tasks = TaskInMemoryStorage()
