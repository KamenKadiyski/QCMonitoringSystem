#!/bin/bash
set -e

# Казваме на Python, че текущата папка (/app) е основният път за модули
export PYTHONPATH=$PYTHONPATH:/app

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Стартираме без префикса 'backend.'
exec gunicorn --bind 0.0.0.0:8000 QCMonitoringSystem.wsgi:application
