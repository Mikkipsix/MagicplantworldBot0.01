FROM python:3.10-slim

WORKDIR /app

# Копируем всё
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "iboga_bot.py"]
