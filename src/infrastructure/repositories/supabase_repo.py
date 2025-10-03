# src/infrastructure/repositories/supabase_repo.py

from typing import List
from supabase import Client
from ...application.interfaces import ITodoRepository
from ...domain.entities import Todo
from ...domain.exceptions import TodoNotFoundError # NEW

class SupabaseTodoRepository(ITodoRepository):
    """Concrete implementation of ITodoRepository using Supabase."""
    
    def __init__(self, supabase_client: Client):
        self.client = supabase_client
        self.table = 'todos' # Hardcoded table name

    def get_all(self) -> List[Todo]:
        # Supabase API call
        response = self.client.table(self.table).select('id, task, is_complete').execute()
        
        # Mapping: Convert Supabase dicts to Domain Entities
        return [
            Todo(
                id=str(item['id']), 
                task=item['task'], 
                is_complete=item['is_complete']
            ) 
            for item in response.data
        ]

    def add(self, todo: Todo) -> Todo:
        # Data to insert (only task is needed, id/is_complete handled by Supabase)
        data = {'task': todo.task}
        
        # Supabase API call (insert)
        response = self.client.table(self.table).insert(data).execute()
        
        # Mapping: Use the returned data to update the original entity (with the generated ID)
        if response.data:
            new_data = response.data[0]
            todo.id = str(new_data['id'])
            todo.is_complete = new_data['is_complete']
        
        return todo
    
    # --- New Method: Update Status ---
    def update_status(self, todo_id: str, is_complete: bool) -> Todo:
        # Supabase API call (update a row matching the ID)
        response = self.client.table(self.table)\
            .update({'is_complete': is_complete})\
            .eq('id', todo_id)\
            .execute()
        
        # If successful, map the returned data to a Todo entity
        if response.data:
            data = response.data[0]
            return Todo(
                id=str(data['id']), 
                task=data['task'], 
                is_complete=data['is_complete']
            )
       # CHANGE: Raise the specific Domain Exception
        raise TodoNotFoundError(todo_id)

    def delete(self, todo_id: str) -> bool:
        # Supabase API call (delete a row matching the ID)
        response = self.client.table(self.table)\
            .delete()\
            .eq('id', todo_id)\
            .execute()
        
        # Supabase returns the deleted row in 'data'. If data is present, deletion was successful.
        return bool(response.data)
    