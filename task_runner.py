import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_task(task_name: str, task_data: dict):
    logger.info(f"Task '{task_name}' started at {datetime.now()}")
    try:
        time.sleep(2)  # simulate work
        logger.info(f"Task '{task_name}' completed successfully!")
        return {"status": "success", "task": task_name, "data": task_data}
    except Exception as e:
        logger.error(f"Task '{task_name}' failed: {str(e)}")
        return {"status": "failed", "task": task_name, "error": str(e)}

def run_with_retry(task_name: str, task_data: dict, max_retries: int = 3):
    for attempt in range(max_retries):
        logger.info(f"Attempt {attempt + 1} of {max_retries}")
        result = run_task(task_name, task_data)
        if result["status"] == "success":
            return result
        logger.warning(f"Retrying in 2 seconds...")
        time.sleep(2)
    return {"status": "failed", "task": task_name, "error": "Max retries reached"}