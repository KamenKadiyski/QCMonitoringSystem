# Използваме стабилен Python
FROM python:3.14-slim

# Инсталираме системни зависимости за PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Инсталираме Python библиотеките
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копираме целия бекенд код
COPY . .

# Правим скрипта за стартиране изпълним
RUN chmod +x entrypoint.sh

# Портът, на който Django/Gunicorn ще слуша (Azure ползва 8000 по подразбиране)
EXPOSE 8000

CMD ["./entrypoint.sh"]
