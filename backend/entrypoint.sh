#!/bin/bash
set -e
export DJANGO_SETTINGS_MODULE=backend.QCMonitoringSystem.settings
# Казваме на Python, че текущата папка (/app) е основният път за модули
export PYTHONPATH=$PYTHONPATH:/app

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Стартираме без префикса 'backend.'
exec gunicorn --bind 0.0.0.0:8000 QCMonitoringSystem.wsgi:application
