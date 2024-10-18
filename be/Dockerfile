# Base image
FROM python:3.9-slim

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Start the Flask app using Gunicorn, binding to the Heroku-provided $PORT
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]