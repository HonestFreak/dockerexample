from fastapi import FastAPI
from celery import Celery

# Create a Celery instance
celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",  # Assuming you are using Redis as the message broker
    backend="redis://redis:6379/0"  # Redis also used as the result backend
)

# FastAPI application instance
app = FastAPI()

# Example Celery task
@celery_app.task
def add(x, y):
    return x + y

# FastAPI route to trigger the Celery task
@app.get("/trigger-celery-task")
async def trigger_celery_task(x: int, y: int):
    result = add.delay(x, y)  # Asynchronously run the Celery task
    return {"task_id": result.id}

# FastAPI route to get the result of the Celery task
@app.get("/get-celery-task-result/{task_id}")
async def get_celery_task_result(task_id: str):
    result = celery_app.AsyncResult(task_id)
    if result.successful():
        return {"result": result.get()}
    else:
        return {"status": result.status}
