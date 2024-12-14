#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Export environment variables
export FLASK_APP=backend/app.py
export FLASK_ENV=development

# Start the Flask server
python -m flask run
