FROM python:3.14-slim

WORKDIR /app

# Копираме съдържанието на текущата папка в /app/backend
# ... (всичко до COPY . .)

# Копираме съдържанието на папка backend в /app на контейнера
COPY . .

# Поправяме символите за нов ред (CRLF -> LF) и даваме права
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Указваме директно името на файла, защото сме в WORKDIR /app
ENTRYPOINT ["./entrypoint.sh"]
