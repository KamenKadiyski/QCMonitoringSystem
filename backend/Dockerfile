FROM python:3.14-slim

# Инсталираме зависимостите
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копираме САМО съдържанието на папка backend в /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копираме останалото
COPY backend /app/backend
COPY manage.py /app/manage.py

# Поправяме Windows символите и даваме права
RUN sed -i 's/\r$//' backend/entrypoint.sh && chmod +x backend/entrypoint.sh

# Директно стартиране
ENTRYPOINT ["/app/backend/entrypoint.sh"]
