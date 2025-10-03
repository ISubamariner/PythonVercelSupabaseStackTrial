# src/domain/exceptions.py

class DomainException(Exception):
    """Base exception for all domain-specific errors."""
    pass

class TodoNotFoundError(DomainException):
    """Raised when a requested Todo item (by ID) does not exist."""
    def __init__(self, todo_id: str):
        self.todo_id = todo_id
        super().__init__(f"Todo with ID '{todo_id}' not found.")

class InvalidInputError(DomainException):
    """Raised when data passed to a Use Case or Entity is invalid."""
    def __init__(self, message: str):
        super().__init__(message)