#!/bin/bash

# Setup and run Cost of Living Index Calculator

echo "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "Running analysis..."
python main.py

echo ""
echo "Done! Check the visualizations/ folder for charts."
