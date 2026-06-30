"""
Capstone Project - Mahashankh AIML Engineering Internship
Combines Project 1, 2, and 3 into one complete system
"""

from ml_model import predict_priority, analyze_sentiment
from task_runner import run_with_retry
from pipeline import run_pipeline

def smart_task_processor(title: str, description: str):
    """
    Capstone feature: Takes a task, analyzes it with AI,
    runs it through the pipeline, and returns full insights
    """
    priority = predict_priority(title)
    sentiment = analyze_sentiment(description)
    
    pipeline_tasks = [
        {"name": "analyze_task", "data": {"title": title}},
        {"name": "process_priority", "data": {"priority": priority}},
        {"name": "store_result", "data": {"sentiment": sentiment}}
    ]
    
    pipeline_result = run_pipeline(f"smart_process_{title}", pipeline_tasks)
    
    return {
        "task": title,
        "description": description,
        "ai_analysis": {
            "priority": priority,
            "sentiment": sentiment
        },
        "pipeline_status": pipeline_result["status"],
        "recommendation": get_recommendation(priority, sentiment)
    }

def get_recommendation(priority: str, sentiment: str) -> str:
    if priority == "high" and sentiment == "negative":
        return "URGENT: This needs immediate attention!"
    elif priority == "high":
        return "Important task - prioritize this soon"
    elif sentiment == "negative":
        return "May need extra care or support"
    else:
        return "Standard task - proceed as planned"