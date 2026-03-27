from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Literal
import time
from datetime import datetime

app = FastAPI()

# In-memory storage
tasks = []
task_id_counter = 1


# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("api_logs.txt", "a") as f:
        f.write(
            f"{timestamp} | {request.method} {request.url.path} | "
            f"Status: {response.status_code} | Time: {round(process_time)}ms\n"
        )

    return response


class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.message = f"Task with id {task_id} not found"
        super().__init__(self.message)


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



def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None



@app.get("/health")
def health():
    return {"status": "healthy"}


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


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(status: Optional[str] = Query(None)):
    if status:
        return [t for t in tasks if t["status"] == status]
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = find_task(task_id)
    if not task:
        raise TaskNotFoundError(task_id)
    return task


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



def reset_data():
    global tasks, task_id_counter
    tasks = []
    task_id_counter = 1