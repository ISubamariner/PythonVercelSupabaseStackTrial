# src/interface_adapters/routes.py

import json
from flask import Blueprint, jsonify, request
from ..domain.use_cases import GetTodosUseCase, CreateTodoUseCase
from ..domain.entities import Todo # To handle input validation

# Create a Blueprint to organize routes
todo_routes = Blueprint('todo_routes', __name__)

# NOTE: The Use Case instances must be injected or passed to these route handlers.
# For simplicity, we define placeholders that will be initialized in api/index.py

@todo_routes.route('/todos', methods=['GET'])
def get_todos_route(get_todos_uc: GetTodosUseCase):
    """GET /api/todos - Retrieves all todos."""
    
    # 1. Orchestration: Call the Use Case
    todos = get_todos_uc.execute()
    
    # 2. Adaptation: Convert Domain Entities to JSON response format
    # The 'id' is converted to int in Supabase but we want to ensure it's JSON-safe string here.
    response_data = [
        {'id': todo.id, 'task': todo.task, 'is_complete': todo.is_complete} 
        for todo in todos
    ]
    return jsonify(response_data), 200


@todo_routes.route('/todos', methods=['POST'])
def create_todo_route(create_todo_uc: CreateTodoUseCase):
    """POST /api/todos - Creates a new todo item."""
    
    try:
        # 1. Adaptation: Get data from request and validate
        data = request.get_json()
        task = data.get('task')
        
        # Use the Entity for basic validation (domain validation)
        # This will raise a ValueError if the task is empty
        Todo(task=task) 
        
        # 2. Orchestration: Call the Use Case
        new_todo = create_todo_uc.execute(task=task)
        
        # 3. Adaptation: Convert Domain Entity to JSON response format
        response_data = {
            'id': new_todo.id, 
            'task': new_todo.task, 
            'is_complete': new_todo.is_complete
        }
        return jsonify(response_data), 201 # 201 Created

    except ValueError as e:
        # Handle Domain-level validation error
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle unexpected errors
        print(f"Error creating todo: {e}")
        return jsonify({"error": "Failed to create todo item."}), 500
    
@todo_routes.route('/todos/<string:todo_id>', methods=['PUT'])
def update_todo_route(update_todo_uc: UpdateTodoUseCase, todo_id: str):
    """PUT /api/todos/<id> - Updates a todo item's status."""
    try:
        # Get data from request (expecting is_complete status)
        data = request.get_json()
        is_complete = data.get('is_complete')
        
        if is_complete is None or not isinstance(is_complete, bool):
            return jsonify({"error": "Missing or invalid 'is_complete' status (must be boolean)."}), 400
        
        # Orchestration: Call the Update Use Case
        updated_todo = update_todo_uc.execute(todo_id=todo_id, is_complete=is_complete)
        
        # Adaptation: Convert Domain Entity to JSON
        response_data = {
            'id': updated_todo.id, 
            'task': updated_todo.task, 
            'is_complete': updated_todo.is_complete
        }
        return jsonify(response_data), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404 # 404 Not Found if ID is invalid
    except Exception as e:
        print(f"Error updating todo: {e}")
        return jsonify({"error": "Failed to update todo item."}), 500


@todo_routes.route('/todos/<string:todo_id>', methods=['DELETE'])
def delete_todo_route(delete_todo_uc: DeleteTodoUseCase, todo_id: str):
    """DELETE /api/todos/<id> - Deletes a todo item."""
    try:
        # Orchestration: Call the Delete Use Case
        success = delete_todo_uc.execute(todo_id=todo_id)
        
        if success:
            # 204 No Content is standard for a successful DELETE
            return '', 204
        else:
            return jsonify({"error": f"Todo with ID {todo_id} not found or failed to delete."}), 404
            
    except Exception as e:
        print(f"Error deleting todo: {e}")
        return jsonify({"error": "Failed to delete todo item."}), 500