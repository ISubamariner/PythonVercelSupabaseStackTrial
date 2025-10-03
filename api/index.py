import os
import json
from flask import Flask, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv # Import load_dotenv for local testing

# --- Configuration & Initialization ---

# 💡 EDUCATION: We try to get environment variables (credentials) first.
# Vercel provides these automatically at runtime.
# Docker/Local testing loads them using `dotenv`.
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        # Create the Supabase client object to interact with the database
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        # The API will log this error but continue to start (failing gracefully)

# --- Flask App Setup ---
# This initializes the lightweight web server
app = Flask(__name__)

# --- API Routes ---

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Fetches all todos from the Supabase 'todos' table."""
    # Check if the Supabase client was successfully initialized
    if not supabase:
        return jsonify({"error": "Supabase client not initialized. Check Vercel environment variables or your local .env file."}), 500

    try:
        # Connect to the 'todos' table and select all records
        response = supabase.table('todos').select('*').execute()
        
        # The results are in the 'data' field of the response object
        todos = response.data
        
        return jsonify(todos), 200

    except Exception as e:
        print(f"Database query error: {e}")
        return jsonify({"error": "Failed to fetch todos from the database"}), 500

# Simple health check endpoint for the root URL
@app.route('/', methods=['GET'])
def home():
    """A simple route to confirm the backend is running."""
    return "Python Backend is Running!"

# --- Local Testing Block ---
# 💡 EDUCATION: This block only runs when you execute the file directly, 
# not when Vercel or Docker runs it via an entry point command.
if __name__ == '__main__':
    # Load environment variables from the local .env file
    load_dotenv()
    
    # Re-initialize the client with local env vars if running directly
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Run the app locally on port 5000 and expose it to all interfaces (0.0.0.0)
    print("Running locally. Access API at http://127.0.0.1:5000/api/todos")
    app.run(host='0.0.0.0', port=5000, debug=True)