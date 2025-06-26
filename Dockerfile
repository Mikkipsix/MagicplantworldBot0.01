FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN chmod 644 secrets/google_credentials.json
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "iboga_bot.py"]
