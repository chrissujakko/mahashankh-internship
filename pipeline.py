import logging
from task_runner import run_task

logger = logging.getLogger(__name__)

def run_pipeline(pipeline_name: str, tasks: list):
    logger.info(f"Pipeline '{pipeline_name}' started!")
    results = []
    for task in tasks:
        logger.info(f"Running task: {task['name']}")
        result = run_task(task['name'], task.get('data', {}))
        results.append(result)
        if result['status'] == 'failed':
            logger.error(f"Pipeline stopped at task: {task['name']}")
            return {"pipeline": pipeline_name, "status": "failed", "results": results}
    logger.info(f"Pipeline '{pipeline_name}' completed!")
    return {"pipeline": pipeline_name, "status": "success", "results": results}