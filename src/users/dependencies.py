from fastapi import Depends

from typing import Annotated

from src.settings.config import Settings, StorageType
from src.users.service import UserService
from src.users.storage import UserStorage, UserJsonStorage

settings_obj = Settings()

def get_settings():
    return settings_obj

def get_user_storage(settings: Annotated[Settings, Depends(get_settings)]):
    dbs = {
        StorageType.JSON: UserJsonStorage()
    }
    return dbs.get(settings.storage)

def get_user_service(storage: Annotated[UserStorage, Depends(get_user_storage)]):
    return UserService(storage)
