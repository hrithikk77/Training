from fastapi import HTTPException, status

class UserNotFoundError(HTTPException):
    def __init__(self, detail="User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class TaskNotFoundError(HTTPException):
    def __init__(self, task_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")

class DuplicateUserError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=message)

class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

# ADD THIS CLASS:
class DataIntegrityError(HTTPException):
    def __init__(self, message: str = "Data integrity issue occurred."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )