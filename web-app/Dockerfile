# Use official Python image as base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy the app code into container
COPY web-app/ /app

# Copy machine-learning-client folder into container
COPY machine-learning-client/ /app/machine-learning-client

# Upgrade pip
RUN python -m pip install --upgrade pip
RUN pip install requests

# Install Python dependencies
RUN pip install -r requirements.txt

# Port that Flask runs on
EXPOSE 5001

# Run the Flask app
CMD ["python", "app.py"]
