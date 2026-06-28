from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Mahashankh Internship API!"}
@app.get("/status")
def status():
    return {"status": "running", "version": "1.0"}

@app.get("/intern")
def intern_info():
    return {"name": "sujakko chakma ", "company": "Mahashankh Design and Technology", "track": "AIML Engineering"}
class Task(BaseModel):
    title: str
    description: str
    done: bool = False

@app.post("/tasks")
def create_task(task: Task):
    return {"message": "Task created!", "task": task}