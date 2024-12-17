# Base image
FROM python:3.11-slim

# Copy alle filer i den mappe hvor min Dockerfile er til /app mappen i mit image
COPY . /app

# Skift til mappen /app (svarer til CD kommandoen)
WORKDIR /app

# Install all dependencies
RUN pip install -r requirements.txt

# Make port 5004 available to the world outside this container
EXPOSE 5004

# Eksekver denne kommando når Containeren køres
CMD ["python", "api-gateway.py"]