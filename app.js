// app.js (Located in the ROOT directory)

/**
 * 💡 OOP Principle: Encapsulation
 * The TodoApp class manages all view behavior and communication with the API.
 */
class TodoApp {
    constructor() {
        // Properties to hold DOM elements
        this.todoList = document.getElementById('todo-list');
        this.todoForm = document.getElementById('todo-form');
        this.taskInput = document.getElementById('task-input');
        
        if (!this.todoList || !this.todoForm || !this.taskInput) {
            console.error("DOM elements missing. Check index.html IDs.");
            return;
        }

        this.init();
    }

    /**
     * Sets up event listeners and loads the initial data.
     */
    init() {
        // Bind 'this' to maintain the class context
        this.todoForm.addEventListener('submit', this.handleFormSubmit.bind(this)); 
        this.fetchAndRenderTodos();
    }

    /**
     * Renders the list of todos to the DOM.
     * @param {Array<Object>} todos - Array of todo objects from the API.
     */
    renderTodos(todos) {
        this.todoList.innerHTML = '';
        if (todos.length === 0) {
            this.todoList.innerHTML = "<li>You have no tasks yet! Add one above.</li>";
            return;
        }

        todos.forEach(todo => {
            const li = document.createElement('li');
            li.textContent = `[${todo.is_complete ? 'DONE' : 'TODO'}] ${todo.task}`;
            this.todoList.appendChild(li);
        });
    }

    /**
     * Fetches the current list of todos from the backend API.
     */
    async fetchAndRenderTodos() {
        try {
            const response = await fetch('/api/todos');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            this.renderTodos(data);
        } catch (error) {
            console.error('Error fetching todos:', error);
            this.todoList.innerHTML = `<li>Error: ${error.message}. Check console.</li>`;
        }
    }

    /**
     * Handles the form submission event to create a new todo.
     */
    async handleFormSubmit(event) {
        event.preventDefault(); 
        const taskText = this.taskInput.value.trim();
        if (!taskText) return; 

        try {
            const response = await fetch('/api/todos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task: taskText }), 
            });

            if (response.status === 201) {
                this.taskInput.value = '';
                await this.fetchAndRenderTodos();
            } else {
                 const errorData = await response.json();
                 alert(`Failed to create task: ${errorData.error || 'Server error'}`);
            }
        } catch (error) {
            console.error('Error submitting todo:', error);
            alert('A network error occurred while submitting the task.');
        }
    }
}

// Instantiate the class to start the application
document.addEventListener('DOMContentLoaded', () => {
    new TodoApp(); 
});