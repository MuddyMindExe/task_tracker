from fastapi import Depends

from typing import Annotated

from src.settings.config import Settings, Storage
from src.tasks.service import TaskService
from src.tasks.storage import TaskStorage, tasks

settings_obj = Settings()

def get_settings() -> Settings:
    return settings_obj

def get_task_storage(settings: Annotated[Settings, Depends(get_settings)]):
    dbs = {
        Storage.IN_MEMORY: tasks
    }
    return dbs.get(settings.storage)

def get_task_service(storage: Annotated[TaskStorage, Depends(get_task_storage)]):
    return TaskService(storage)
