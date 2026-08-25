from src.tasks.storage import TaskStorage
from src.tasks.schemas import Task
from src.tasks.schemas import TaskCreate, TaskUpdate
from src.tasks.constants import TaskStatus

class TaskService:
    def __init__(self, task_storage: TaskStorage):
        self.task_storage = task_storage

    def get_tasks(self, title: str | None, status: TaskStatus | None) -> dict[int, Task]:
        if title is None and status is None:
            return self.task_storage.show_all()

        return {
            task_id: task for task_id, task in self.task_storage.show_all().items()
            if (title is None or title.lower() in task.title.lower())
            and (status is None or status == task.status)
                }

    def get_task(self, task_id: int) -> Task | None:
        return self.task_storage.get_task(task_id)

    def add_task(self, task_data: TaskCreate) -> Task | None:
        task = self.task_storage.add_task(task_data)
        return task

    def delete_task(self, task_id: int) -> Task | None:
        return self.task_storage.delete_task(task_id)

    def change_task(self, task_id: int, task_data: TaskUpdate) -> Task | None:
        return self.task_storage.change_task(task_id, **task_data.model_dump())
