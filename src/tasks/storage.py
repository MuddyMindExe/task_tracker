from src.tasks.schemas import Task
from src.tasks.constants import TaskStatus

class TaskStorage:
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.current_id = 3 #temp, default=0

    def show_all(self):
        return list(self.tasks.values())

    def get_task(self, task_id: int) -> Task | None:
        return self.tasks.get(task_id)

    def add_task(self, task: Task):
        self.tasks[task.id] = task

    def delete_task(self, task_id: int) -> Task | None:
        return self.tasks.pop(task_id, None)

    def change_task(self, task_id: int, new_status: TaskStatus, new_title: str | None = None) -> Task | None:
        task = self.tasks.get(task_id)

        if new_title:
            task.change_title(new_title)

        return None if not task else task.change_status(new_status)

    def get_id(self):
        return self.current_id

    def set_id(self, new_id: int):
        if not isinstance(new_id, int):
            raise TypeError("Invalid new_id value")

        self.current_id = new_id
