# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . .

# Expose port 5000 for Flask
EXPOSE 5000

# Run the Flask app with Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
