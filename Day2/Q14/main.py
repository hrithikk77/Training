from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Literal

app = FastAPI()

# -----------------------------
# In-memory storage
# -----------------------------
tasks = []
task_id_counter = 1


# -----------------------------
# Custom Exception
# -----------------------------
class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
        self.message = f"Task with id {task_id} not found"
        super().__init__(self.message)


# -----------------------------
# Global Exception Handler
# -----------------------------
@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "TaskNotFoundError",
            "message": exc.message,
            "status_code": 404
        }
    )


# -----------------------------
# Models
# -----------------------------
class TaskCreate(BaseModel):
    title: str
    description: str
    status: Literal["pending", "in_progress", "completed"]


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["pending", "in_progress", "completed"]] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str


# -----------------------------
# Helper function
# -----------------------------
def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "healthy"}


# -----------------------------
# Create Task
# -----------------------------
@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    global task_id_counter

    new_task = {
        "id": task_id_counter,
        "title": task.title,
        "description": task.description,
        "status": task.status
    }

    tasks.append(new_task)
    task_id_counter += 1

    return new_task


# -----------------------------
# Get All Tasks
# -----------------------------
@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(status: Optional[str] = Query(None)):
    if status:
        return [t for t in tasks if t["status"] == status]
    return tasks


# -----------------------------
# Get Task by ID (UPDATED)
# -----------------------------
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = find_task(task_id)
    if not task:
        raise TaskNotFoundError(task_id)
    return task


# -----------------------------
# Update Task (UPDATED)
# -----------------------------
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated: TaskUpdate):
    task = find_task(task_id)
    if not task:
        raise TaskNotFoundError(task_id)

    if updated.title is not None:
        task["title"] = updated.title
    if updated.description is not None:
        task["description"] = updated.description
    if updated.status is not None:
        task["status"] = updated.status

    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks

    task = find_task(task_id)
    if not task:
        raise TaskNotFoundError(task_id)

    tasks = [t for t in tasks if t["id"] != task_id]

    return {"message": "Task deleted successfully"}


