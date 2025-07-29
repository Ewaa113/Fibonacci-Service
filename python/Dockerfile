# Build the Python container
# Use an official Python image as base
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and buffering logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the Python app into the container
COPY requirements.txt /app/requirements.txt
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the port the app runs on
EXPOSE 8000
EXPOSE 8001

# Start the Python HTTP server automatically
CMD ["python", "main.py"]
