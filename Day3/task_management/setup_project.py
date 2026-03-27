# import os
# import stat

# def create_project_structure(root_dir="task_management"):
#     """
#     Creates the specified directory structure and empty files for the FastAPI project.
#     """
#     print(f"Creating project structure in '{os.path.abspath(root_dir)}'...")

#     # Define the directory structure
#     directories = [
#         "models",
#         "services",
#         "repositories",
#         "routers",
#         "middleware",
#         "exceptions",
#         "tests",
#         "data",
#         "logs"
#     ]

#     # Define the files with their initial content (if any)
#     files_with_content = {
#         "main.py": "",
#         "config.py": "",
#         "requirements.txt": """fastapi
# uvicorn[standard]
# pydantic
# pydantic-settings
# python-jose[cryptography]
# passlib[bcrypt]
# aiofiles # For async file operations, useful for JSON repo
# """,
#         ".env": """APP_NAME="My Awesome Task API"
# SECRET_KEY="a_very_secret_and_long_random_string_for_security_purposes_12345"
# ACCESS_TOKEN_EXPIRE_MINUTES=60
# LOG_LEVEL="DEBUG"
# """,
#         "models/schemas.py": "",
#         "models/enums.py": "",
#         "services/task_service.py": "",
#         "services/user_service.py": "",
#         "repositories/base_repository.py": "",
#         "repositories/json_repository.py": "",
#         "routers/task_router.py": "",
#         "routers/user_router.py": "",
#         "middleware/logging_middleware.py": "",
#         "exceptions/custom_exceptions.py": "",
#         "tests/test_tasks.py": "",
#         "tests/test_users.py": "",
#         "data/tasks.json": '{\n  "tasks": []\n}',
#         "data/users.json": '{\n  "users": []\n}',
#     }

#     # Create root directory
#     os.makedirs(root_dir, exist_ok=True)

#     # Create subdirectories
#     for d in directories:
#         path = os.path.join(root_dir, d)
#         os.makedirs(path, exist_ok=True)
#         print(f"Created directory: {path}")

#     # Create __init__.py files for packages
#     package_dirs = ["models", "services", "repositories", "routers", "middleware", "exceptions", "tests"]
#     for p_dir in package_dirs:
#         path = os.path.join(root_dir, p_dir, "__init__.py")
#         with open(path, 'w') as f:
#             f.write("") # Empty __init__.py
#         print(f"Created file: {path}")

#     # Create other files and populate initial content
#     for file_path, content in files_with_content.items():
#         full_path = os.path.join(root_dir, file_path)
#         os.makedirs(os.path.dirname(full_path), exist_ok=True) # Ensure parent dir exists
#         with open(full_path, 'w') as f:
#             f.write(content)
#         print(f"Created file: {full_path}")

#     # Ensure data files have appropriate permissions (optional, good practice)
#     for data_file in ["data/tasks.json", "data/users.json"]:
#         full_path = os.path.join(root_dir, data_file)
#         try:
#             os.chmod(full_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH) # rw-r--r--
#         except OSError as e:
#             print(f"Warning: Could not set permissions for {full_path}. {e}")

#     print("\nProject structure created successfully!")
#     print("\n--- Next Steps ---")
#     print(f"1. Navigate into your project directory: cd {root_dir}")
#     print("2. Create a virtual environment: python -m venv venv")
#     print("3. Activate the virtual environment:")
#     print("   - macOS/Linux: source venv/bin/activate")
#     print("   - Windows: .\\venv\\Scripts\\activate")
#     print("4. Install dependencies: pip install -r requirements.txt")
#     print("5. Once dependencies are installed, you can start building your app!")

# if __name__ == "__main__":
#     create_project_structure()




import os

def update_project_structure(root_dir="task_management"):
    print(f"Updating project structure in '{os.path.abspath(root_dir)}' for Day 3...")

    # New files to create
    files_to_create = [
        "database.py",
        "models/db_models.py",
        "repositories/sqlalchemy_repository.py",
        "alembic.ini",
    ]

    for file_path in files_to_create:
        full_path = os.path.join(root_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        if not os.path.exists(full_path):
            with open(full_path, 'w') as f:
                f.write("") # Create empty file
            print(f"Created file: {full_path}")
        else:
            print(f"File already exists: {full_path}")

    print("\nStructure updated! Proceed to paste the code.")

if __name__ == "__main__":
    update_project_structure()