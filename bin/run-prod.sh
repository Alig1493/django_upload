urlwait &&
./manage.py migrate &&
gunicorn -w 1 --access-logfile=- --timeout=120 django_file_upload.wsgi:application --bind 0.0.0.0:$PORT
