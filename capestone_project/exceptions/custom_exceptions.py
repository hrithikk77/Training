from fastapi import HTTPException, status

class LoanHubException(HTTPException):
    def __init__(self, detail: str, status_code: int):
        super().__init__(status_code=status_code, detail=detail)

class UserNotFoundError(LoanHubException):
    def __init__(self, message="User not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)

class DuplicateUserError(LoanHubException):
    def __init__(self, message="Username or email already exists"):
        super().__init__(message, status.HTTP_409_CONFLICT)

class InvalidCredentialsError(LoanHubException):
    def __init__(self, message="Invalid username or password"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)

class MaxPendingLoansError(LoanHubException):
    def __init__(self):
        super().__init__(
            "You already have 3 pending loans. Wait for review before applying again.", 
            status.HTTP_422_UNPROCESSABLE_ENTITY
        )

class LoanNotFoundError(LoanHubException):
    def __init__(self):
        super().__init__("Loan ID does not exist", status.HTTP_404_NOT_FOUND)

class InvalidLoanReviewError(LoanHubException):
    def __init__(self, message="Trying to review an already reviewed loan"):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)

class ForbiddenError(LoanHubException):
    def __init__(self):
        super().__init__("You do not have permission to access this resource", status.HTTP_403_FORBIDDEN)