from enum import Enum

class Storage(str, Enum):
    IN_MEMORY = "in_memory"
    JSON = "json"
    MYSQL = "mysql"
    PGSQL = "postgresql"
