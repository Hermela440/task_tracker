# Task Tracker CLI

A simple command-line task tracker that stores tasks in a JSON file.

## Installation

1. Clone this repository
2. Ensure you have Python 3 installed
3. Make the script executable: `chmod +x task_tracker.py`

## Usage

```
./task_tracker.py [command] [options]

Commands:
  add "description"       Add a new task
  update [id] "desc"      Update a task's description
  delete [id]             Delete a task
  mark-in-progress [id]   Mark task as in progress
  mark-done [id]          Mark task as done
  list                    List all tasks
  list todo               List todo tasks
  list in-progress        List in-progress tasks
  list done               List done tasks
```

## Examples

```bash
# Add a task
./task_tracker.py add "Buy groceries"

# List all tasks
./task_tracker.py list

# Mark task 1 as in progress
./task_tracker.py mark-in-progress 1

# Update task 1
./task_tracker.py update 1 "Buy groceries and cook dinner"

# Delete task 1
./task_tracker.py delete 1
```