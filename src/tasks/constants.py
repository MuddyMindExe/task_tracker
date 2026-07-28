from enum import Enum

class TaskStatus(str, Enum):
    NOT_COMPLETE = "not_complete"
    COMPLETE = "complete"
    IN_PROGRESS = "in_progress"
