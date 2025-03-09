import click
import json  # To save and load tasks
import os  # To check if the file exists

TODO_FILE = "todo.json"

def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(TODO_FILE):
        return []  # Return an empty list if the file doesn't exist
    with open(TODO_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

@click.group()
def cli():
    """Simple Todo List Manager"""
    pass

@click.command()
@click.argument("task")
def add(task):
    """Add a new task"""
    tasks = load_tasks()
    tasks.append({"task": task, "done": False})
    save_tasks(tasks)
    click.echo(f"✅ Task added successfully: {task}")

@click.command(name="list")
def list_tasks():
    """List all tasks"""
    tasks = load_tasks()
    if not tasks:
        click.echo("❌ No tasks found.")
        return

    click.echo("📌 Your Tasks:")
    for index, task in enumerate(tasks, start=1):
        status = "✔" if task["done"] else "✘"
        click.echo(f"{index}. {task['task']} [{status}]")

@click.command()
@click.argument("task_number", type=int)
def complete(task_number):
    """Mark a task as completed"""
    tasks = load_tasks()
    
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]["done"] = True
        save_tasks(tasks)
        click.echo(f"✅ Task {task_number} marked as completed.")
    else:
        click.echo(f"❌ Invalid task number: {task_number}")

@click.command()
@click.argument("task_number", type=int)
def remove(task_number):
    """Remove a task"""
    tasks = load_tasks()
    
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        click.echo(f"🗑️ Task removed: '{removed_task['task']}'")
    else:
        click.echo(f"❌ Invalid task number: {task_number}")

# Register commands
cli.add_command(add)
cli.add_command(list_tasks)
cli.add_command(complete)
cli.add_command(remove)

if __name__ == "__main__":
    cli()
