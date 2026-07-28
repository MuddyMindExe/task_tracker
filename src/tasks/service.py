from src.tasks.storage import TaskStorage
from src.tasks.schemas import Task
from src.tasks.schemas import TaskCreate, TaskUpdate
from src.tasks.constants import TaskStatus

class TaskService:
    def __init__(self, task_storage: TaskStorage):
        self.task_storage = task_storage

    def get_tasks(self, title: str | None, status: TaskStatus | None) -> list[Task | None]:
        if title is None and status is None:
            return self.task_storage.show_all()

        return [
            task for task in self.task_storage.show_all()
            if (title is None or title.lower() in task.title.lower())
            and (status is None or status == task.status)
                ]

    def get_task(self, task_id: int) -> Task | None:
        return self.task_storage.get_task(task_id)

    def add_task(self, task_data: TaskCreate) -> Task:
        task_id = self.task_storage.get_id()

        task = Task(id=task_id, title=task_data.title, status=task_data.status, user_id=task_data.user_id)

        self.task_storage.add_task(task)
        self.task_storage.set_id(task_id+1)
        return task

    def delete_task(self, task_id: int) -> Task | None:
        return self.task_storage.delete_task(task_id)

    def change_task(self, task_id: int, task_data: TaskUpdate) -> Task | None:
        return self.task_storage.change_task(task_id, task_data.status, task_data.title)

tasks = TaskStorage()
task_service = TaskService(tasks)

t1 = Task(id=1, title="Изучить FastAPI", status=TaskStatus.IN_PROGRESS, user_id=1)
t2 = Task(id=2, title="Купить молоко", status=TaskStatus.COMPLETE, user_id=1)

tasks.add_task(t1)
tasks.add_task(t2)
