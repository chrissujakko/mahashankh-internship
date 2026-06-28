from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from database import Base, engine, get_db, TaskModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mahashankh Task Manager API")

class Task(BaseModel):
    title: str
    description: str
    done: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    done: bool
    class Config:
        from_attributes = True

@app.get("/")
def home():
    return {"message": "Welcome to Mahashankh Task Manager API!"}

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: Task, db: Session = Depends(get_db)):
    new_task = TaskModel(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted!"}
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: Task, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated_task.title
    task.description = updated_task.description
    task.done = updated_task.done
    db.commit()
    db.refresh(task)
    return task