# repositories/json_repository.py
from datetime import datetime
import json
import os
import asyncio
from typing import List, Dict, Any, Optional
from filelock import FileLock # For concurrent file writes, needs `pip install python-filelock`
from aiofiles import open as aio_open

from repositories.base_repository import BaseRepository
from exceptions.custom_exceptions import DataIntegrityError

import logging
logger = logging.getLogger(__name__)

# Install `python-filelock` if you haven't: pip install python-filelock
# Note: For highly concurrent scenarios, a real database is recommended.
# File locking helps, but can still be a bottleneck.

class JsonRepository(BaseRepository):
    """
    Concrete implementation of BaseRepository for JSON file storage.
    Handles reading from and writing to a JSON file, including simple locking
    for concurrent access.
    Adheres to LSP because it correctly implements the BaseRepository contract.
    """

    def __init__(self, file_path: str, collection_name: str):
        super().__init__(file_path, collection_name)
        self.lock_file_path = f"{file_path}.lock"
        self.lock = FileLock(self.lock_file_path, timeout=5) 

    async def _read_data(self) -> Dict[str, Any]:
        """Reads data from the JSON file with a file lock."""
        try:
            with self.lock:
                
                async with asyncio.Lock(): 
                    async with aio_open(self.file_path, 'r', encoding='utf-8') as f:
                        content = await f.read()
                        if not content:
                            logger.warning(f"JSON file {self.file_path} is empty. Reinitializing.")
                            return {self.collection_name: []}
                        return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Corrupted JSON data in {self.file_path}: {e}", exc_info=True)
            #
            await self._ensure_file_exists() # Re-create with empty structure
            raise DataIntegrityError(f"Corrupted data in {self.file_path}. File was reset.")
        except FileNotFoundError:
            logger.warning(f"Data file {self.file_path} not found. Recreating.")
            await self._ensure_file_exists() 
            return {self.collection_name: []} 
        except Exception as e:
            logger.error(f"Error reading from {self.file_path}: {e}", exc_info=True)
            raise DataIntegrityError(f"Failed to read data from {self.file_path}")

    async def _write_data(self, data: Dict[str, Any]):
        """Writes data to the JSON file with a file lock."""
        try:
            with self.lock:
                
                async with asyncio.Lock(): 
                    async with aio_open(self.file_path, 'w', encoding='utf-8') as f:
                        await f.write(json.dumps(data, indent=2))
        except Exception as e:
            logger.error(f"Error writing to {self.file_path}: {e}", exc_info=True)
            raise DataIntegrityError(f"Failed to write data to {self.file_path}")

    async def get_all(self, **filters) -> List[Dict[str, Any]]:
        """
        Retrieves all items from the JSON file, optionally filtered.
        """
        data = await self._read_data()
        items = data.get(self.collection_name, [])

        if not filters:
            return items

        filtered_items = []
        for item in items:
            match = True
            for key, value in filters.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                filtered_items.append(item)
        return filtered_items

    async def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single item by its ID.
        """
        data = await self._read_data()
        items = data.get(self.collection_name, [])
        for item in items:
            if item.get("id") == item_id:
                return item
        return None

    async def create(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new item, assigning a unique ID and current timestamps.
        """
        data = await self._read_data()
        items = data.get(self.collection_name, [])

        new_id = 1
        if items:
            new_id = max(item.get("id", 0) for item in items) + 1

        now = datetime.now().isoformat()
        new_item = {
            "id": new_id,
            "created_at": now,
            "updated_at": now,
            **item_data
        }
        items.append(new_item)
        data[self.collection_name] = items
        await self._write_data(data)
        return new_item

    async def update(self, item_id: int, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Updates an existing item by its ID with new data.
        """
        data = await self._read_data()
        items = data.get(self.collection_name, [])
        found_item = None
        for i, item in enumerate(items):
            if item.get("id") == item_id:
                items[i].update(item_data)
                items[i]["updated_at"] = datetime.now().isoformat()
                found_item = items[i]
                break

        if found_item:
            data[self.collection_name] = items
            await self._write_data(data)
        return found_item

    async def delete(self, item_id: int) -> bool:
        """
        Deletes an item by its ID.
        """
        data = await self._read_data()
        items = data.get(self.collection_name, [])
        initial_length = len(items)
        items = [item for item in items if item.get("id") != item_id]
        data[self.collection_name] = items

        if len(items) < initial_length:
            await self._write_data(data)
            return True
        return False

    async def find_one_by_field(self, field_name: str, field_value: Any) -> Optional[Dict[str, Any]]:
        """
        Finds a single item by a specific field and its value.
        """
        data = await self._read_data()
        items = data.get(self.collection_name, [])
        for item in items:
            if item.get(field_name) == field_value:
                return item
        return None

    async def find_many_by_field(self, field_name: str, field_value: Any) -> List[Dict[str, Any]]:
        """
        Finds multiple items by a specific field and its value.
        """
        data = await self._read_data()
        items = data.get(self.collection_name, [])
        return [item for item in items if item.get(field_name) == field_value]