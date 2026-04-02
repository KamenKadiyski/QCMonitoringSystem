# Използваме стабилен Python 3.12
FROM python:3.14-slim

# Инсталираме системни зависимости за PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копираме requirements и инсталираме библиотеките
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копираме целия бекенд код
COPY . .

# ВАЖНО: Превръщаме Windows окончанията (CRLF) в Linux (LF) и даваме права
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Портът за Gunicorn
EXPOSE 8000

# Използваме ENTRYPOINT вместо CMD за по-добра стабилност на скриптове
ENTRYPOINT ["./entrypoint.sh"]
