FROM python:3.12-slim

WORKDIR /app
COPY src/ ./src/
COPY requirements.txt .
COPY tests/ ./tests/  
COPY src/data/ ./src/data/ 
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app/src
CMD ["python", "-m", "bashnet"]
