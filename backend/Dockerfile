FROM python:3.14-slim

WORKDIR /app

# Копираме съдържанието на текущата папка в /app/backend
COPY . /app/backend/

# Правим entrypoint скрипта изпълним
RUN chmod +x /app/backend/entrypoint.sh

# Инсталираме зависимостите
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Указваме entrypoint (пътят е вътре в папката backend)
ENTRYPOINT ["/app/backend/entrypoint.sh"]
