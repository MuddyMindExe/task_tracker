from pydantic import BaseModel

from src.tasks.constants import TaskStatus

class Task(BaseModel):
    id: int
    title: str
    status: TaskStatus = TaskStatus.NOT_COMPLETE
    user_id: int

    def change_status(self, new_status: TaskStatus):
        self.status = new_status
        return self

    def change_title(self, new_title: str):
        self.title = new_title
        return self

class TaskCreate(BaseModel):
    title: str
    status: TaskStatus = TaskStatus.NOT_COMPLETE
    user_id: int

class TaskUpdate(BaseModel):
    title: str | None = None
    status: TaskStatus | None = None
