#!/bin/bash
set -e

echo "--- СЪДЪРЖАНИЕ НА ПАПКА /APP ---"
ls -la

echo "--- ИЗПЪЛНЯВАНЕ НА МИГРАЦИИ ---"
# Използваме директен път до manage.py
python /app/manage.py migrate --noinput

echo "--- СЪБИРАНЕ НА СТАТИКА ---"
python /app/manage.py collectstatic --noinput

echo "--- СТАРТИРАНЕ НА GUNICORN ---"
# Провери дали името QCMonitoringSystem е точно такова (с 'r' или 't')
exec gunicorn --bind 0.0.0.0:8000 QCMonitoringSystem.wsgi:application
