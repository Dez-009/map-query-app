# Dockerfile
FROM python:3.11-slim

# Install netcat for database connection check
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Make the startup script executable
RUN chmod +x ./scripts/startup.sh

# Use bash to run the script
CMD ["/bin/bash", "./scripts/startup.sh"]
