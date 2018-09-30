web: bash -c "./bin/run-prod.sh"
worker: celery -A upload worker -l info --concurrency=2 --beat
