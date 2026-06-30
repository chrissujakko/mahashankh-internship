from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from task_runner import run_with_retry
from sqlalchemy.orm import Session
from typing import List
from database import Base, engine, get_db, TaskModel
from ml_model import predict_priority, analyze_sentiment
from pipeline import run_pipeline
from capstone import smart_task_processor

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
@app.post("/predict-priority")
def get_priority(task: Task):
    priority = predict_priority(task.title)
    return {"title": task.title, "predicted_priority": priority}
@app.post("/analyze")
def analyze_task(task: Task):
    priority = predict_priority(task.title)
    sentiment = analyze_sentiment(task.description)
    return {
        "title": task.title,
        "description": task.description,
        "predicted_priority": priority,
        "sentiment": sentiment
    }

@app.post("/run-task")
def trigger_task(task_name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_with_retry, task_name, {"triggered_at": "now"})
    return {"message": f"Task '{task_name}' started in background!"}
@app.post("/run-pipeline")
def trigger_pipeline(pipeline_name: str, background_tasks: BackgroundTasks):
    tasks = [
        {"name": "validate_data", "data": {}},
        {"name": "process_data", "data": {}},
        {"name": "save_results", "data": {}}
    ]
    background_tasks.add_task(run_pipeline, pipeline_name, tasks)
    return {"message": f"Pipeline '{pipeline_name}' started in background!"}
@app.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    total_tasks = db.query(TaskModel).count()
    done_tasks = db.query(TaskModel).filter(TaskModel.done == True).count()
    pending_tasks = db.query(TaskModel).filter(TaskModel.done == False).count()
    
    return {
        "total_tasks": total_tasks,
        "done_tasks": done_tasks,
        "pending_tasks": pending_tasks,
        "completion_rate": f"{(done_tasks/total_tasks*100) if total_tasks > 0 else 0:.1f}%"
    }
@app.get("/analytics/summary")
def get_summary(db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).all()
    
    high_priority = 0
    medium_priority = 0
    low_priority = 0
    
    for task in tasks:
        priority = predict_priority(task.title)
        if priority == "high":
            high_priority += 1
        elif priority == "medium":
            medium_priority += 1
        else:
            low_priority += 1
    
    return {
        "total_tasks": len(tasks),
        "priority_breakdown": {
            "high": high_priority,
            "medium": medium_priority,
            "low": low_priority
        },
        "ai_insights": f"You have {high_priority} high priority tasks that need attention!"
    }
@app.post("/capstone/smart-process")
def smart_process(task: Task):
    result = smart_task_processor(task.title, task.description)
    return result