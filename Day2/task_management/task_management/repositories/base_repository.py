# repositories/base_repository.py
from abc import ABC, abstractmethod
import json
from typing import List, Dict, Any, Optional
import asyncio
from aiofiles import open as aio_open
import os

# This logger will be configured in main.py, but we can import it here.
# For now, it's a placeholder. We'll ensure proper logging setup is globally available.
import logging
logger = logging.getLogger(__name__)

class BaseRepository(ABC):
    """
    Abstract Base Class for repositories.
    Defines the contract for data access operations.
    Adheres to ISP by only including data access methods.
    Adheres to DIP by providing an abstraction that services will depend on.
    """

    def __init__(self, file_path: str, collection_name: str):
        self.file_path = file_path
        self.collection_name = collection_name
        # Ensure data file exists with initial empty structure if not present
        asyncio.run(self._ensure_file_exists())

    async def _ensure_file_exists(self):
        """Ensures the JSON file exists and contains a valid empty structure."""
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            initial_data = {self.collection_name: []}
            try:
                async with aio_open(self.file_path, 'w', encoding='utf-8') as f:
                    await f.write(json.dumps(initial_data, indent=2))
                logger.info(f"Created initial data file: {self.file_path}")
            except Exception as e:
                logger.error(f"Failed to create initial data file {self.file_path}: {e}", exc_info=True)
                # Depending on severity, you might want to raise DataIntegrityError here
                pass # Allow the app to start, but log the error

    @abstractmethod
    async def get_all(self, **filters) -> List[Dict[str, Any]]:
        """
        Retrieves all items from the repository, optionally filtered.
        """
        pass

    @abstractmethod
    async def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single item by its ID.
        """
        pass

    @abstractmethod
    async def create(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new item and adds it to the repository.
        """
        pass

    @abstractmethod
    async def update(self, item_id: int, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Updates an existing item by its ID with new data.
        """
        pass

    @abstractmethod
    async def delete(self, item_id: int) -> bool:
        """
        Deletes an item by its ID.
        Returns True if deleted, False if not found.
        """
        pass

    @abstractmethod
    async def find_one_by_field(self, field_name: str, field_value: Any) -> Optional[Dict[str, Any]]:
        """
        Finds a single item by a specific field and its value.
        """
        pass

    @abstractmethod
    async def find_many_by_field(self, field_name: str, field_value: Any) -> List[Dict[str, Any]]:
        """
        Finds multiple items by a specific field and its value.
        """
        pass