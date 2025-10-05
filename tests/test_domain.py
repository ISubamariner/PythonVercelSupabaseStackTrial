# tests/test_domain.py

from typing import List
import pytest

# Import the core Clean Architecture components
from src.domain.entities import Todo
from src.domain.use_cases import (
    GetTodosUseCase, 
    CreateTodoUseCase, 
    UpdateTodoUseCase, 
    DeleteTodoUseCase
)
from src.application.interfaces import ITodoRepository
from src.domain.exceptions import TodoNotFoundError, InvalidInputError # Import custom exceptions


# --- Mock Implementation (OOP Principle: Abstraction & Polymorphism) ---

class MockTodoRepository(ITodoRepository):
    """
    A fake implementation of the ITodoRepository interface for testing.
    It fulfills the contract but uses in-memory storage (a list).
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

    def update_status(self, todo_id: str, is_complete: bool) -> Todo:
        """Finds and updates the status of a todo."""
        for todo in self._todos:
            if todo.id == todo_id:
                todo.is_complete = is_complete
                return todo
        # Raise the specific Domain Exception if not found
        raise TodoNotFoundError(todo_id)

    def delete(self, todo_id: str) -> bool:
        """Deletes a todo by ID."""
        initial_length = len(self._todos)
        self._todos = [todo for todo in self._todos if todo.id != todo_id]
        # Returns True if the list length changed (item was deleted)
        return len(self._todos) < initial_length


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
    """Test the CreateTodoUseCase using the Mock Repository."""
    # Arrange
    repository = MockTodoRepository()
    use_case = CreateTodoUseCase(repository=repository)
    
    # Act
    task_description = "Finish unit tests"
    new_todo = use_case.execute(task=task_description)
    
    # Assert
    assert isinstance(new_todo, Todo)
    assert new_todo.task == task_description
    assert new_todo.id is not None
    assert len(repository.get_all()) == 1
    
    
# --- Unit Tests for the UpdateTodoUseCase ---

def test_update_todo_use_case_to_complete():
    """Test updating a task's status from False to True."""
    # Arrange: Add a new task first
    repo = MockTodoRepository()
    create_uc = CreateTodoUseCase(repository=repo)
    initial_todo = create_uc.execute(task="Task to complete")
    
    # Arrange: Instantiate the Update Use Case
    update_uc = UpdateTodoUseCase(repository=repo)
    
    # Act: Mark the task as complete
    updated_todo = update_uc.execute(todo_id=initial_todo.id, is_complete=True)
    
    # Assert
    assert updated_todo.is_complete is True
    assert repo.get_all()[0].is_complete is True

def test_update_todo_use_case_not_found():
    """Test error handling when attempting to update a non-existent ID."""
    # Arrange
    repo = MockTodoRepository()
    update_uc = UpdateTodoUseCase(repository=repo)
    
    # Act & Assert: Expect TodoNotFoundError
    with pytest.raises(TodoNotFoundError, match="Todo with ID '999' not found."):
        update_uc.execute(todo_id="999", is_complete=True)


# --- Unit Tests for the DeleteTodoUseCase ---

def test_delete_todo_use_case_success():
    """Test successful deletion of a task."""
    # Arrange: Add a new task
    repo = MockTodoRepository()
    create_uc = CreateTodoUseCase(repository=repo)
    todo_to_delete = create_uc.execute(task="Task to delete")
    
    # Arrange: Instantiate the Delete Use Case
    delete_uc = DeleteTodoUseCase(repository=repo)
    
    # Act: Delete the task
    success = delete_uc.execute(todo_id=todo_to_delete.id)
    
    # Assert
    assert success is True
    assert len(repo.get_all()) == 0

def test_delete_todo_use_case_not_found():
    """Test deletion attempt on a non-existent ID."""
    # Arrange
    repo = MockTodoRepository()
    delete_uc = DeleteTodoUseCase(repository=repo)
    
    # Act
    success = delete_uc.execute(todo_id="999")
    
    # Assert
    assert success is False