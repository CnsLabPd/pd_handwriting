# Use a slim Python base
FROM python:3.11-slim

WORKDIR /app

# Install only the API dependencies
COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

# Copy everything in this folder (main.py, numpy files, etc.) into /app
COPY . .

EXPOSE 8000

# Launch Uvicorn pointing at main.py’s FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
