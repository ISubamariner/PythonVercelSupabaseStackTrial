# api/index.py - The Vercel entry point

import os
from flask import Flask
from supabase import create_client, Client
from dotenv import load_dotenv

# Import Clean Architecture Components
from src.infrastructure.repositories.supabase_repo import SupabaseTodoRepository
# Import the new use cases
from src.domain.use_cases import GetTodosUseCase, CreateTodoUseCase, UpdateTodoUseCase, DeleteTodoUseCase 
from src.interface_adapters.routes import todo_routes

# --- 1. Infrastructure Setup (Supabase Client) ---

# Load .env for local running
load_dotenv() 

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase_client: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")

# --- 2. Dependency Injection / Wiring ---

# Inject the concrete Supabase Repository implementation
todo_repository = SupabaseTodoRepository(supabase_client=supabase_client)

# Instantiate Use Cases with the Repository (Dependency Inversion)
get_todos_uc = GetTodosUseCase(repository=todo_repository)
create_todo_uc = CreateTodoUseCase(repository=todo_repository)
update_todo_uc = UpdateTodoUseCase(repository=todo_repository)
delete_todo_uc = DeleteTodoUseCase(repository=todo_repository)


# --- 3. Flask App Setup ---
app = Flask(__name__)

# Register the Blueprint from the Interface Adapters layer
app.register_blueprint(todo_routes, url_prefix='/api')

# NOTE: Since Blueprints can't directly use custom arguments in Flask's default setup,
# we need a simple trick to inject the Use Cases into the route functions.
# This simple setup uses Flask's g object or request context variables.
# For simplicity in a serverless function, we'll manually wrap the route handler:

def wrap_route(f):
    """Wrapper to manually inject the correct use case instance."""
    def wrapper(*args, **kwargs):
        if f.__name__ == 'get_todos_route':
            return f(get_todos_uc, *args, **kwargs)
        elif f.__name__ == 'create_todo_route':
            return f(create_todo_uc, *args, **kwargs)
        elif f.__name__ == 'update_todo_route': # New injection
            return f(update_todo_uc, *args, **kwargs)
        elif f.__name__ == 'delete_todo_route': # New injection
            return f(delete_todo_uc, *args, **kwargs)
        else:
            return f(*args, **kwargs)
    wrapper.__name__ = f.__name__ # Preserve the function name for routing
    return wrapper

# Replace the original routes with the wrapped versions
for rule in app.url_map.iter_rules():
    if rule.endpoint.startswith('todo_routes.'):
        original_view = app.view_functions[rule.endpoint]
        app.view_functions[rule.endpoint] = wrap_route(original_view)


@app.route('/', methods=['GET'])
def home():
    """Simple root route check."""
    return "Python Backend is Running (Clean Architecture Applied!)"

# --- Local Testing Block ---
if __name__ == '__main__':
    # When running locally, Flask is responsible for routing
    print("Running locally. Access API at http://127.0.0.1:5000/api/todos")
    app.run(host='0.0.0.0', port=5000, debug=True)