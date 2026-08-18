from pydantic import BaseModel

from src.tasks.constants import TaskStatus

class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.NOT_COMPLETE
    user_id: int

    def set_title(self, new_title: str):
        self.title = new_title

    def set_description(self, new_description: str):
        self.description = new_description

    def set_status(self, new_status: TaskStatus):
        self.status = new_status

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.NOT_COMPLETE
    user_id: int

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
