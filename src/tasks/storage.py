from abc import ABC, abstractmethod

from src.tasks.schemas import Task
from src.tasks.constants import TaskStatus

class TaskStorage(ABC):
    @abstractmethod
    def show_all(self):...

    @abstractmethod
    def get_task(self, task_id: int) -> Task:...

    @abstractmethod
    def add_task(self, task: Task):...

    @abstractmethod
    def delete_task(self, task_id: int):...

    @abstractmethod
    def change_task(self, task_id: int, *params):...

class TaskInMemoryStorage:
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.current_id = 1

    def show_all(self):
        return list(self.tasks.values())

    def get_task(self, task_id: int) -> Task | None:
        return self.tasks.get(task_id)

    def add_task(self, task: Task) -> None:
        self.tasks[task.id] = task

    def delete_task(self, task_id: int) -> Task | None:
        return self.tasks.pop(task_id, None)

    def change_task(self, task_id: int,
                    new_title: str | None, new_description: str | None, new_status: TaskStatus | None) -> Task | None:
        task = self.tasks.get(task_id)
        if not task:
            return None
        if new_title:
            task.set_title(new_title)
        if new_description:
            task.set_description(new_description)
        if new_status:
            task.set_status(new_status)
        return task

    def get_id(self):
        return self.current_id

    def set_id(self, new_id: int):
        if not isinstance(new_id, int):
            raise TypeError("Invalid new_id value")

        self.current_id = new_id

tasks = TaskInMemoryStorage()
