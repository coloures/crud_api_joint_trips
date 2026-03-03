FROM python:3.12-slim

Workdir /services

copy requirements.txt .
run pip install --no-cache-dir -r requirements.txt

copy . .

cmd ["python", "main.py"]