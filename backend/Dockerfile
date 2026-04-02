FROM python:3.14-slim

# Инсталираме зависимостите
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копираме САМО съдържанието на папка backend в /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копираме останалото
COPY . .

# Поправяме Windows символите и даваме права
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Директно стартиране
ENTRYPOINT ["/app/entrypoint.sh"]
