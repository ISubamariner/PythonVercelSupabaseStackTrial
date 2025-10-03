# src/domain/entities.py

from typing import Optional

class Todo:
    """The core business entity for a To-Do item."""
    def __init__(self, task: str, id: Optional[str] = None, is_complete: bool = False):
        if not task:
            raise ValueError("Task cannot be empty.")
        self.id = id
        self.task = task
        self.is_complete = is_complete
    
    def __repr__(self):
        return f"Todo(id={self.id}, task='{self.task}', is_complete={self.is_complete})"