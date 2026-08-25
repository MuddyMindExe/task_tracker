from enum import Enum

class StorageType(str, Enum):
    IN_MEMORY = "in_memory"
    JSON = "json"
    MYSQL = "mysql"
    PGSQL = "postgresql"
