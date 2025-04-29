# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Establish the environment variable for Python to not buffer output
WORKDIR /app

# Instal thwe necessary system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the container
COPY . /app

# Instal the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Comand for running the ETL process
CMD ["python", "etl/main.py"]