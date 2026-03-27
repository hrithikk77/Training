# models/enums.py
from enum import Enum

class TaskStatus(str, Enum):
    """
    Defines the possible statuses for a task.
    Inherits from str to allow direct string comparison and serialization in FastAPI.
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    """
    Defines the possible priority levels for a task.
    Inherits from str for string compatibility.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"