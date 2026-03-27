# services/task_service.py
from datetime import datetime
from typing import List, Dict, Any, Optional

from models.schemas import TaskCreate, TaskUpdate, TaskResponse
from models.enums import TaskPriority, TaskStatus
from repositories.base_repository import BaseRepository
from exceptions.custom_exceptions import TaskNotFoundError, UserNotFoundError

import logging
logger = logging.getLogger(__name__)

class TaskService:
    """
    Handles task-related business logic, including creation, retrieval,
    and updates. Depends on abstract BaseRepository for tasks and users.
    Adheres to SRP (only task business logic) and DIP (depends on abstraction).
    """

    def __init__(self, task_repository: BaseRepository, user_repository: BaseRepository):
        self.task_repository = task_repository
        self.user_repository = user_repository # To validate task owner existence

    async def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """
        Creates a new task. Validates the owner exists.
        Sets initial status to PENDING.
        """
        # Validate owner exists
        owner_exists = await self.user_repository.find_one_by_field("username", task_data.owner)
        if not owner_exists:
            logger.warning(f"Attempted to create task for non-existent owner: {task_data.owner}")
            raise UserNotFoundError(f"Owner '{task_data.owner}' not found.")

        task_to_create_dict = task_data.model_dump()
        task_to_create_dict["status"] = TaskStatus.PENDING # Default status
        # Repository will add id, created_at, updated_at

        created_task_dict = await self.task_repository.create(task_to_create_dict)
        logger.info(f"Task '{created_task_dict.get('title')}' created with ID {created_task_dict.get('id')} for owner '{created_task_dict.get('owner')}'.")
        return TaskResponse(**created_task_dict)

    async def get_all_tasks(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        owner: Optional[str] = None,
        page: int = 1,
        limit: int = 10
    ) -> List[TaskResponse]:
        """
        Retrieves tasks with filtering and pagination.
        """
        filters = {}
        if status:
            filters["status"] = status.value # Use .value for string comparison in repo
        if priority:
            filters["priority"] = priority.value
        if owner:
            # Validate owner existence if filtering by owner
            owner_exists = await self.user_repository.find_one_by_field("username", owner)
            if not owner_exists:
                logger.warning(f"Attempted to filter tasks by non-existent owner: {owner}")
                # For filtering, we might return an empty list rather than raising an error,
                # as a filter for something that doesn't exist should yield no results.
                return []
            filters["owner"] = owner

        all_tasks = await self.task_repository.get_all(**filters)

        # Pagination logic
        start_index = (page - 1) * limit
        end_index = start_index + limit
        paginated_tasks = all_tasks[start_index:end_index]

        logger.info(f"Retrieved {len(paginated_tasks)} tasks (page {page}, limit {limit}) with filters: {filters}")
        return [TaskResponse(**task) for task in paginated_tasks]

    async def get_task_by_id(self, task_id: int) -> TaskResponse:
        """
        Retrieves a single task by its ID.
        """
        task_in_db = await self.task_repository.get_by_id(task_id)
        if not task_in_db:
            logger.warning(f"Attempted to retrieve non-existent task with ID: {task_id}")
            raise TaskNotFoundError(task_id)
        logger.info(f"Task with ID {task_id} retrieved.")
        return TaskResponse(**task_in_db)

    async def update_task(self, task_id: int, task_data: TaskUpdate) -> TaskResponse:
        """
        Updates an existing task by its ID.
        Performs partial updates, ignoring None values in task_data.
        """
        existing_task = await self.task_repository.get_by_id(task_id)
        if not existing_task:
            logger.warning(f"Attempted to update non-existent task with ID: {task_id}")
            raise TaskNotFoundError(task_id)

        # Convert Pydantic model to dictionary, exclude None values for partial update
        update_data_dict = task_data.model_dump(exclude_unset=True, exclude_none=True)

        if "owner" in update_data_dict:
            # If owner is provided in update_data_dict, validate its existence
            new_owner = update_data_dict["owner"]
            owner_exists = await self.user_repository.find_one_by_field("username", new_owner)
            if not owner_exists:
                logger.warning(f"Attempted to change task owner to non-existent user: {new_owner}")
                raise UserNotFoundError(f"New owner '{new_owner}' not found.")

        updated_task_dict = await self.task_repository.update(task_id, update_data_dict)
        if not updated_task_dict: # Should not happen if existing_task was found
            logger.error(f"Failed to update task ID {task_id} in repository after finding it.")
            raise TaskNotFoundError(task_id) # Re-raise if repository failed unexpectedly
        logger.info(f"Task with ID {task_id} updated.")
        return TaskResponse(**updated_task_dict)

    async def delete_task(self, task_id: int) -> bool:
        """
        Deletes a task by its ID.
        """
        # First, check if the task exists
        task_exists = await self.task_repository.get_by_id(task_id)
        if not task_exists:
            logger.warning(f"Attempted to delete non-existent task with ID: {task_id}")
            raise TaskNotFoundError(task_id)

        is_deleted = await self.task_repository.delete(task_id)
        if is_deleted:
            logger.info(f"Task with ID {task_id} deleted successfully.")
        else:
            logger.error(f"Failed to delete task with ID {task_id} even after existence check.")
        return is_deleted