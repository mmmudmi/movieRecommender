#!/bin/bash

# Create a .env file if it doesn't exist
touch .env

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production
export PORT=${PORT:-5000}

# Install Python dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi