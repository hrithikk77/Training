
from fastapi import HTTPException, status


class UserNotFoundError(HTTPException):
    """Exception raised when a user is not found."""
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found."
        )

class DuplicateUserError(HTTPException):
    """Exception raised when attempting to create a user with an existing username or email."""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )

class InvalidCredentialsError(HTTPException):
    """Exception raised for incorrect username or password during login."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}, 
        )


class TaskNotFoundError(HTTPException):
    """Exception raised when a task is not found."""
    def __init__(self, task_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found."
        )

class NotTaskOwnerError(HTTPException):
    """Optional: Exception raised when a user tries to modify a task they don't own."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to modify this task."
        )


class DataIntegrityError(HTTPException):
    """Exception raised for issues with data consistency (e.g., file corruption)."""
    def __init__(self, message: str = "Data integrity issue occurred."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )