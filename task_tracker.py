#!/usr/bin/env python3
import sys
import json
import os
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

# Constants
TASKS_FILE = 'tasks.json'

def load_tasks():
    """Load tasks from JSON file or create if doesn't exist"""
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f)
        return []
    
    with open(TASKS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli [command] [options]")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'add':
        add_task()
    elif command == 'list':
        list_tasks()
    elif command == 'update':
        update_task()
    elif command == 'delete':
        delete_task()
    elif command == 'mark-in-progress':
        mark_in_progress()
    elif command == 'mark-done':
        mark_done()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

def add_task():
    """Add a new task"""
    if len(sys.argv) < 3:
        print("Usage: task-cli add \"task description\"")
        return
    
    description = ' '.join(sys.argv[2:]).strip()
    if not description:
        print("Error: Task description cannot be empty")
        return
    
    if len(description) > 255:  # Example max length
        print("Error: Task description is too long (max 255 characters)")
        return
    
    try:
        tasks = load_tasks()
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return
    
    # Generate ID (max existing ID + 1 or 1 if empty)
    new_id = max([task['id'] for task in tasks], default=0) + 1
    
    new_task = {
        'id': new_id,
        'description': description,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    
    try:
        tasks.append(new_task)
        save_tasks(tasks)
        print(f"Task added successfully (ID: {new_id})")
    except Exception as e:
        print(f"Error saving task: {e}")

def list_tasks():
    """List tasks based on status filter if provided"""
    tasks = load_tasks()
    
    if len(sys.argv) > 2:
        status_filter = sys.argv[2].lower()
        valid_statuses = ['todo', 'in-progress', 'done']
        
        if status_filter not in valid_statuses:
            print(f"Invalid status filter. Use one of: {', '.join(valid_statuses)}")
            return
        
        filtered_tasks = [task for task in tasks if task['status'] == status_filter]
        print_tasks(filtered_tasks, f"Tasks ({status_filter}):")
    else:
        print_tasks(tasks, "All tasks:")

def print_tasks(tasks, title):
    """Helper function to print tasks in a formatted way"""
    if not tasks:
        print(f"{title}\n  No tasks found")
        return
    
    # Color codes using colorama
    COLORS = {
        'todo': Fore.YELLOW,
        'in-progress': Fore.CYAN,
        'done': Fore.GREEN,
        'reset': Style.RESET_ALL
    }
    
    print(title)
    for task in tasks:
        status_display = {
            'todo': 'To Do',
            'in-progress': 'In Progress',
            'done': 'Done'
        }.get(task['status'], task['status'])
        
        color = COLORS.get(task['status'], COLORS['reset'])
        
        print(f"  ID: {task['id']}")
        print(f"  Description: {task['description']}")
        print(f"  Status: {color}{status_display}{COLORS['reset']}")
        print(f"  Created: {task['createdAt']}")
        print(f"  Updated: {task['updatedAt']}")
        print("-" * 40)

def delete_task():
    """Delete a task"""
    if len(sys.argv) < 3:
        print("Usage: task-cli delete [id]")
        return
    
    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Error: ID must be a number")
        return
    
    tasks = load_tasks()
    initial_count = len(tasks)
    
    tasks = [task for task in tasks if task['id'] != task_id]
    
    if len(tasks) < initial_count:
        save_tasks(tasks)
        print(f"Task {task_id} deleted successfully")
    else:
        print(f"Task with ID {task_id} not found")

def mark_in_progress():
    """Mark a task as in progress"""
    change_task_status('in-progress')

def mark_done():
    """Mark a task as done"""
    change_task_status('done')

def change_task_status(new_status):
    """Helper function to change task status"""
    if len(sys.argv) < 3:
        print(f"Usage: task-cli {sys.argv[1]} [id]")
        return
    
    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Error: ID must be a number")
        return
    
    tasks = load_tasks()
    
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = new_status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {new_status}")
            return
    
    print(f"Task with ID {task_id} not found")