# Use the official Python image
FROM python:3.12-slim

# Install necessary system packages
RUN apt-get update \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the default command to run when starting the container
CMD ["python", "app.py"]
