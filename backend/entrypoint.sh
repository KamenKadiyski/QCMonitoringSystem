#!/bin/bash

# Изчакваме базата данни (ако имате такава логика)
# ...

# Изпълняваме миграциите през модула backend
python backend/manage.py migrate --noinput
python backend/manage.py collectstatic --noinput

# Стартираме сървъра (Gunicorn или runserver)
# Важно: изпълняваме го от корена (/app)
exec python backend/manage.py runserver 0.0.0.0:8000
