from abc import ABC, abstractmethod
class BaseRepository(ABC):
    @abstractmethod
    async def get_all(self, **filters): pass
    @abstractmethod
    async def get_by_id(self, item_id: int): pass
    @abstractmethod
    async def create(self, item_data: dict): pass
    @abstractmethod
    async def update(self, item_id: int, item_data: dict): pass
    @abstractmethod
    async def delete(self, item_id: int): pass
    @abstractmethod
    async def find_one_by_field(self, field_name: str, field_value): pass