# tests/test_domain.py

from typing import List
import pytest

# Import the core Clean Architecture components
from src.domain.entities import Todo
from src.domain.use_cases import CreateTodoUseCase
from src.application.interfaces import ITodoRepository # The contract

# --- Mock Implementation (OOP Principle: Abstraction & Polymorphism) ---

class MockTodoRepository(ITodoRepository):
    """
    A fake implementation of the ITodoRepository interface for testing.
    It fulfills the contract (implements all abstract methods) but uses 
    in-memory storage (a list) instead of Supabase.
    """
    def __init__(self):
        # In-memory storage for testing
        self._todos = []
        self._next_id = 1 

    def get_all(self) -> List[Todo]:
        return self._todos
    
    def add(self, todo: Todo) -> Todo:
        # Simulate ID generation and database interaction
        todo.id = str(self._next_id)
        self._next_id += 1
        self._todos.append(todo)
        return todo

# --- Unit Tests for the Domain Entity ---

def test_todo_creation_valid():
    """Test that a Todo entity can be created successfully."""
    task = "Buy milk"
    todo = Todo(task=task)
    assert todo.task == task
    assert todo.is_complete is False
    assert todo.id is None

def test_todo_creation_invalid_empty_task():
    """Test that the Todo entity raises a ValueError on empty input."""
    # We use pytest.raises to assert that a specific exception is raised
    with pytest.raises(ValueError, match="Task cannot be empty."):
        Todo(task="")

# --- Unit Tests for the CreateTodoUseCase ---

def test_create_todo_use_case_success():
    """
    Test the CreateTodoUseCase using the Mock Repository. 
    This isolates the Use Case logic from the database implementation.
    """
    # Arrange: Instantiate the mock repository
    repository = MockTodoRepository()
    
    # Instantiate the Use Case, injecting the mock repository
    use_case = CreateTodoUseCase(repository=repository)
    
    # Act: Execute the business operation
    task_description = "Finish unit tests"
    new_todo = use_case.execute(task=task_description)
    
    # Assert 1: Verify the returned object is correct
    assert isinstance(new_todo, Todo)
    assert new_todo.task == task_description
    assert new_todo.id is not None # ID should have been assigned by the mock repo
    
    # Assert 2: Verify the repository actually stored the item
    assert len(repository.get_all()) == 1
    assert repository.get_all()[0].task == task_description