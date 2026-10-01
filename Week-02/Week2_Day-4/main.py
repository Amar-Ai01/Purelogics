"""
Week 2 - Lab 4
FastAPI To-Do List REST API
----------------------------
Task: Develop a To-Do List REST API that allows users to
create, view, update, and delete tasks.

Assignment Endpoints (5 total):
1. POST   /todos          -> Add a new task
2. GET    /todos          -> Get all tasks
3. GET    /todos/{id}     -> Get a task by ID
4. PUT    /todos/{id}     -> Update a task
5. DELETE /todos/{id}     -> Delete a task

Note: Data is stored in-memory using a Python list
(no database used, as per assignment instructions).
Data resets every time the server restarts.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="To-Do List REST API")


# =========================================================
# DATA MODELS (define the shape/structure of incoming data)
# =========================================================

class Task(BaseModel):
    """Used when CREATING a new task (POST request)."""
    title: str
    completed: bool = False  # optional, defaults to False


class TaskUpdate(BaseModel):
    """Used when UPDATING an existing task (PUT request)."""
    title: str
    completed: bool  # required, must be explicitly provided


# =========================================================
# IN-MEMORY DATA STORE (acts as our "fake database")
# =========================================================

todos = []      # stores all task dictionaries
next_id = 1     # counter used to auto-generate unique task IDs


# =========================================================
# TEST ROUTE (not part of the assignment's 5 endpoints)
# =========================================================

@app.get("/")
def home():
    """Basic health-check route to confirm the server is running."""
    return {"message": "Welcome to FastAPI!"}


# =========================================================
# ASSIGNMENT ENDPOINTS (5 required endpoints)
# =========================================================

# ---- 1. CREATE a new task ----
@app.post("/todos")
def create_task(task: Task):
    global next_id
    new_task = {
        "id": next_id,
        "title": task.title,
        "completed": task.completed
    }
    todos.append(new_task)
    next_id += 1
    return new_task


# ---- 2. READ all tasks ----
@app.get("/todos")
def get_all_tasks():
    return todos


# ---- 3. READ a single task by ID ----
@app.get("/todos/{task_id}")
def get_task(task_id: int):
    for task in todos:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# ---- 4. UPDATE an existing task ----
@app.put("/todos/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):
    for task in todos:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["completed"] = updated_task.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# ---- 5. DELETE a task ----
@app.delete("/todos/{task_id}")
def delete_task(task_id: int):
    for task in todos:
        if task["id"] == task_id:
            todos.remove(task)
            return {"message": f"Task with id {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")