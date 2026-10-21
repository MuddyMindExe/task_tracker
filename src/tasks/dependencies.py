from fastapi import Depends

from typing import Annotated

from src.database import engine

from src.settings.config import Settings, StorageType

from src.tasks.service import TaskService
from src.tasks.storage import TaskStorage, TaskJsonStorage,  tasks

settings_obj = Settings()

def get_settings() -> Settings:
    return settings_obj

def get_task_storage(settings: Annotated[Settings, Depends(get_settings)]):
    dbs = {
        StorageType.IN_MEMORY: tasks,
        StorageType.JSON: TaskJsonStorage(),
        StorageType.MYSQL: engine
    }
    return dbs.get(settings.storage)

def get_task_service(storage: Annotated[TaskStorage, Depends(get_task_storage)]):
    return TaskService(storage)
