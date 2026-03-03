FROM python:3:12-slim

Workdir /app

copy requirements.txt .
run pip install --no-cache-dir -r requirements.txt

copy . .

cmd ["python", "app.py"]