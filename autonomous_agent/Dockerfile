# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies (using eventlet for SocketIO)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a volume for memory persistence
VOLUME /app/memory.json

# Expose the web portal port
EXPOSE 5000

# Run the Soul Web Server
CMD ["python", "server.py"]
