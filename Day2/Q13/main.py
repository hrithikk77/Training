from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Literal

app = FastAPI()

tasks = []
task_id_counter = 1

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

@app.get("/health")
def health():
    return {"status": "healthy"}


def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


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
        raise HTTPException(status_code=404, detail="Task not found")
    return task



@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated: TaskUpdate):
    task = find_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

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
        raise HTTPException(status_code=404, detail="Task not found")

    tasks = [t for t in tasks if t["id"] != task_id]

    return {"message": "Task deleted successfully"}