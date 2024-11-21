# Stage 1: Use an official Python base image
FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1  # Prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED 1        # Ensure stdout and stderr are flushed immediately

# Set the working directory
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project to the container
COPY bend .

# Expose port 8000 for the Django development server
EXPOSE 3000

# Copy over start file
COPY start.sh .
RUN chmod +x start.sh

# Point command to start file
CMD ["./start.sh"]