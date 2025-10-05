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

class UpdateTodoUseCase:
    """Updates the status (e.g., is_complete) of an existing Todo."""
    def __init__(self, repository: ITodoRepository):
        self.repository = repository
        
    def execute(self, todo_id: str, is_complete: bool) -> Todo:
        # Business logic: Validation that the ID exists would go here.
        # We assume the ID is valid for now and let the repository handle the lookup/update.
        return self.repository.update_status(todo_id, is_complete)

class DeleteTodoUseCase:
    """Deletes an existing Todo item."""
    def __init__(self, repository: ITodoRepository):
        self.repository = repository
        
    def execute(self, todo_id: str) -> bool:
        return self.repository.delete(todo_id)
    
class UpdateTodoUseCase:
    """Updates the status (e.g., is_complete) of an existing Todo."""
    def __init__(self, repository: ITodoRepository):
        self.repository = repository
        
    def execute(self, todo_id: str, is_complete: bool) -> Todo:
        # Business logic: Validation that the ID exists would go here.
        # We assume the ID is valid for now and let the repository handle the lookup/update.
        return self.repository.update_status(todo_id, is_complete)

class DeleteTodoUseCase:
    """Deletes an existing Todo item."""
    def __init__(self, repository: ITodoRepository):
        self.repository = repository
        
    def execute(self, todo_id: str) -> bool:
        return self.repository.delete(todo_id)