# routers/task_router.py
from fastapi import APIRouter, Depends, status, Query, HTTPException, BackgroundTasks
from typing import List, Optional

from repositories.sqlalchemy_repository import SqlAlchemyRepository
from models.schemas import TaskCreate, TaskUpdate, TaskResponse
from models.enums import TaskStatus, TaskPriority
from services.task_service import TaskService
from repositories.base_repository import BaseRepository
# from repositories.json_repository import JsonRepository
from config import settings

from models.db_models import Task, User
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import datetime

import logging
logger = logging.getLogger(__name__)

# Create an APIRouter instance for task-related endpoints
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={404: {"description": "Task not found"}}
)


def write_notification(title: str, owner: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("notifications.log", mode="a") as file:
        file.write(f"[{timestamp}] Task '{title}' created by {owner} — notification sent\n")


# --- CHANGED: Inject Database Session ---
def get_task_repository(db: AsyncSession = Depends(get_db)) -> BaseRepository:
    return SqlAlchemyRepository(db, Task)

def get_user_repository_for_task_service(db: AsyncSession = Depends(get_db)) -> BaseRepository:
    return SqlAlchemyRepository(db, User)

def get_task_service(
    task_repo: BaseRepository = Depends(get_task_repository),
    user_repo: BaseRepository = Depends(get_user_repository_for_task_service)
) -> TaskService:
    return TaskService(task_repo, user_repo)


# --- CHANGED: Add BackgroundTasks to create_task endpoint ---
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks, # <-- Added here
    task_service: TaskService = Depends(get_task_service)
):
    logger.info(f"Received request to create task: {task_data.title} by {task_data.owner}")
    task = await task_service.create_task(task_data)
    
    # Trigger the background task!
    background_tasks.add_task(write_notification, task.title, task.owner)
    
    logger.info(f"Task '{task.title}' created with ID {task.id}. Background notification queued.")
    return task

# @router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
# async def create_task(
#     task_data: TaskCreate,
#     task_service: TaskService = Depends(get_task_service)
# ):
#     """
#     Creates a new task. The `owner` must be an existing user.
#     """
#     logger.info(f"Received request to create task: {task_data.title} by {task_data.owner}")
#     task = await task_service.create_task(task_data)
#     logger.info(f"Task '{task.title}' created with ID {task.id}.")
#     return task

@router.get("/", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
async def list_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter tasks by status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter tasks by priority"),
    owner: Optional[str] = Query(None, description="Filter tasks by owner username"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Retrieves a list of tasks with optional filtering and pagination.
    """
    logger.info(f"Received request to list tasks with filters: status={status}, priority={priority}, owner={owner}, page={page}, limit={limit}")
    tasks = await task_service.get_all_tasks(status=status, priority=priority, owner=owner, page=page, limit=limit)
    logger.info(f"Returning {len(tasks)} tasks.")
    return tasks

@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task_by_id(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """
    Retrieves a single task by its ID.
    """
    logger.info(f"Received request to get task with ID: {task_id}")
    task = await task_service.get_task_by_id(task_id) 
    logger.info(f"Task ID {task_id} retrieved successfully.")
    return task

@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task_full(
    task_id: int,
    task_data: TaskCreate, 
    task_service: TaskService = Depends(get_task_service)
):
    """
    Performs a full update on an existing task.
    All fields in the request body are required.
    """
    logger.info(f"Received request for full update of task ID: {task_id}")
    
    update_data = task_data.model_dump()
    updated_task = await task_service.update_task(task_id, TaskUpdate(**update_data)) 
    logger.info(f"Task ID {task_id} fully updated.")
    return updated_task

@router.patch("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task_partial(
    task_id: int,
    task_data: TaskUpdate, # Using TaskUpdate for partial update (fields are optional)
    task_service: TaskService = Depends(get_task_service)
):
    """
    Performs a partial update on an existing task.
    Only provided fields in the request body will be updated.
    """
    logger.info(f"Received request for partial update of task ID: {task_id}")
    updated_task = await task_service.update_task(task_id, task_data)
    logger.info(f"Task ID {task_id} partially updated.")
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """
    Deletes a task by its ID.
    """
    logger.info(f"Received request to delete task with ID: {task_id}")
    await task_service.delete_task(task_id) # Service raises TaskNotFoundError if not found
    logger.info(f"Task with ID {task_id} deleted successfully.")
    return {"message": f"Task with id {task_id} deleted successfully"}