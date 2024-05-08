celery -A src.agent.celery_app worker  --loglevel=info -E &
# uvicorn app.main:app --host 0.0.0.0 --reload --workers 2
gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 src.app:app