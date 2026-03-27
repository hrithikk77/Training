from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def add(self, entity): pass
    @abstractmethod
    def get_all(self): pass
    @abstractmethod
    def get_by_id(self, id): pass