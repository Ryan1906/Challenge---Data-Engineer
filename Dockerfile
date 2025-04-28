FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY etl/ ./etl/
COPY data/ ./data/

CMD ["python", "etl/main.py"]