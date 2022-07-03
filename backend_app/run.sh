celery -A backend_app flower --loglevel=info

celery -A backend_app worker -l info



