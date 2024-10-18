# Base image
FROM python:3.9-slim

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Start Flask app with Gunicorn
CMD ["sh", "-c", "gunicorn app:asgi_app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT} --workers 4"]
