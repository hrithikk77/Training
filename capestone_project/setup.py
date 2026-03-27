import os
from pathlib import Path

# YOUR SPECIFIC PATH
BASE_DIR = Path(r"C:\Users\hrithik.k\Desktop\python\capestone_project")

files = [
    "main.py",
    "config.py",
    "database.py",
    ".env",
    "requirements.txt",
    "alembic.ini",
    "models/__init__.py",
    "models/schemas.py",
    "models/enums.py",
    "models/db_models.py",
    "services/__init__.py",
    "services/user_service.py",
    "services/loan_service.py",
    "services/analytics_service.py",
    "repositories/__init__.py",
    "repositories/base_repository.py",
    "repositories/sqlalchemy_repository.py",
    "routers/__init__.py",
    "routers/auth_router.py",
    "routers/loan_router.py",
    "routers/admin_router.py",
    "routers/analytics_router.py",
    "decorators/__init__.py",
    "decorators/timer.py",
    "decorators/retry.py",
    "decorators/auth.py",
    "middleware/__init__.py",
    "middleware/logging_middleware.py",
    "exceptions/__init__.py",
    "exceptions/custom_exceptions.py",
    "utils/__init__.py",
    "utils/notifications.py",
    "logs/app.log",
    "logs/notifications.log",
    "tests/__init__.py",
    "tests/test_auth.py",
    "tests/test_loans.py",
    "tests/test_admin.py"
]

def create_structure():
    # 1. Create the base directory if it doesn't exist
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    for file_path in files:
        # Combine base path with file relative path
        full_path = BASE_DIR / file_path
        
        # 2. Create parent folders
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 3. Create the empty file
        if not full_path.exists():
            full_path.touch()
            print(f"Successfully Created: {full_path}")
        else:
            print(f"Skipped (Already exists): {full_path}")

if __name__ == "__main__":
    create_structure()
    print(f"\n--- Done! Project is ready at: {BASE_DIR} ---")