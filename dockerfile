# Use a base image with Python
FROM python:3.10-slim

# Set a working directory
WORKDIR /app

# Install Node.js and npm (required for Gemini CLI)
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Install the Gemini CLI globally
RUN npm install -g @google/gemini-cli

# Copy your application files
COPY ./ ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8080

# The command to run your application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]