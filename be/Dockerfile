# Base image
FROM python:3.9-slim

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Use Uvicorn to run the app, which supports WebSockets
CMD ["python", "app.py"]