#!/bin/bash

# Launch the Cost of Living City Recommender Website
# This script checks if data exists and launches the Streamlit app

echo "Cost of Living City Recommender"
echo "================================"
echo ""

# Check if cost index data exists
if [ ! -f "outputs/reports/cost_index_results.csv" ]; then
    echo "Warning: Data file not found"
    echo ""
    echo "Please generate the cost index data first:"
    echo "  cd src"
    echo "  python main.py"
    echo ""
    exit 1
fi

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Warning: Streamlit is not installed"
    echo ""
    echo "Please install it first:"
    echo "  pip install streamlit"
    echo ""
    exit 1
fi

echo "Data file found"
echo "Streamlit installed"
echo ""
echo "Launching website..."
echo ""
echo "The website will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

# Launch streamlit
streamlit run website/app.py
