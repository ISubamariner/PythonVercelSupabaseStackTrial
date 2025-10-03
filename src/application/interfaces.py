# src/application/interfaces.py

from abc import ABC, abstractmethod
from typing import List
from ..domain.entities import Todo

class ITodoRepository(ABC):
    """Abstract interface (contract) for any Todo data storage."""
    
    @abstractmethod
    def get_all(self) -> List[Todo]:
        """Retrieves all Todo items."""
        pass
        
    @abstractmethod
    def add(self, todo: Todo) -> Todo:
        """Adds a new Todo item to the storage."""
        pass