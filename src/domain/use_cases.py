# src/domain/use_cases.py

from typing import List
from .entities import Todo
from ..application.interfaces import ITodoRepository # Dependency pointing INWARD (abstraction)

class GetTodosUseCase:
    """Gets the entire list of Todos."""
    def __init__(self, repository: ITodoRepository):
        self.repository = repository
        
    def execute(self) -> List[Todo]:
        return self.repository.get_all()

class CreateTodoUseCase:
    """Creates a new Todo item."""
    def __init__(self, repository: ITodoRepository):
        self.repository = repository
        
    def execute(self, task: str) -> Todo:
        # Business logic: validate the input before creation
        new_todo = Todo(task=task) 
        return self.repository.add(new_todo)