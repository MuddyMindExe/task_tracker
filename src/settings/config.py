from pydantic_settings import BaseSettings

from src.settings.constants import Storage

class Settings(BaseSettings):
    storage: Storage = Storage.IN_MEMORY
