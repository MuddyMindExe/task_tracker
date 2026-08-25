from pydantic_settings import BaseSettings

from src.settings.constants import StorageType

class Settings(BaseSettings):
    storage: StorageType = StorageType.JSON
