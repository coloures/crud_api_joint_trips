FROM python:3.12-slim

Workdir /app

copy requirements.txt .
run pip install --no-cache-dir -r requirements.txt

copy . .

CMD ["uvicorn", "services.main:app", "--host", "0.0.0.0", "--port", "8001"]