

#!/bin/bash

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn or uWSGI server (choose one)
# For Gunicorn:
gunicorn harmonization.wsgi:application --bind 0.0.0.0:8000

# For uWSGI (uncomment and adjust as needed):
# uwsgi --socket :8000 --master --enable-threads --module harmonization.wsgi:application

