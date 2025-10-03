# src/application/factory.py

from supabase import Client
from ..infrastructure.repositories.supabase_repo import SupabaseTodoRepository
from ..domain.use_cases import (
    GetTodosUseCase, 
    CreateTodoUseCase, 
    UpdateTodoUseCase, 
    DeleteTodoUseCase
)

class TodoServiceFactory:
    """
    Factory class responsible for creating and wiring 
    all necessary dependencies (Repositories and Use Cases).
    """
    def __init__(self, supabase_client: Client):
        self.supabase_client = supabase_client
        # Instantiate the Repository once
        self._todo_repository = SupabaseTodoRepository(supabase_client=self.supabase_client)

    def get_get_todos_use_case(self) -> GetTodosUseCase:
        """Returns a wired instance of the GetTodos Use Case."""
        return GetTodosUseCase(repository=self._todo_repository)

    def get_create_todo_use_case(self) -> CreateTodoUseCase:
        """Returns a wired instance of the CreateTodo Use Case."""
        return CreateTodoUseCase(repository=self._todo_repository)

    def get_update_todo_use_case(self) -> UpdateTodoUseCase:
        """Returns a wired instance of the UpdateTodo Use Case."""
        return UpdateTodoUseCase(repository=self._todo_repository)

    def get_delete_todo_use_case(self) -> DeleteTodoUseCase:
        """Returns a wired instance of the DeleteTodo Use Case."""
        return DeleteTodoUseCase(repository=self._todo_repository)