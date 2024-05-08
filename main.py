import logging
from fastapi import FastAPI
from celery import Celery

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a Celery instance
celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",  # Assuming you are using Redis as the message broker
    backend="redis://redis:6379/0"  # Redis also used as the result backend
)

app = FastAPI()

@celery_app.task
def add(x, y):
    logger.debug(f"Running task 'add' with arguments x={x}, y={y}")
    return x + y

# FastAPI route to trigger the Celery task
@app.get("/trigger-celery-task")
async def trigger_celery_task(x: int, y: int):
    logger.debug("Triggering Celery task...")
    result = add.delay(x, y)  # Asynchronously run the Celery task
    logger.debug(f"Celery task ID: {result.id}")
    return {"task_id": result.id}

# FastAPI route to get the result of the Celery task
@app.get("/get-celery-task-result/{task_id}")
async def get_celery_task_result(task_id: str):
    logger.debug(f"Checking result for Celery task ID: {task_id}")
    result = celery_app.AsyncResult(task_id)
    if result.successful():
        logger.debug("Celery task completed successfully.")
        return {"result": result.get()}
    else:
        logger.debug(f"Celery task status: {result.status}")
        return {"status": result.status}
