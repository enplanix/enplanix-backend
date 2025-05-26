# When you change hardware, check workers-help.txt

gunicorn backend.asgi:application \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 1 \
    --threads 2 \
    --bind 0.0.0.0:8000 \
    --timeout 60 \
    --keep-alive 5

