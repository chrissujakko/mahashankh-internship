from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Mahashankh Task Manager API")

# Temporary storage (list)
tasks = []
task_id_counter = 1

class Task(BaseModel):
    title: str
    description: str
    done: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    done: bool

@app.get("/")
def home():
    return {"message": "Welcome to Mahashankh Task Manager API!"}

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: Task):
    global task_id_counter
    new_task = {"id": task_id_counter, "title": task.title, "description": task.description, "done": task.done}
    tasks.append(new_task)
    task_id_counter += 1
    return new_task

@app.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return {"message": "Task deleted!"}
    raise HTTPException(status_code=404, detail="Task not found")