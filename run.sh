#!/bin/bash

# Cost of Living Index Analysis - Run Script
# This script runs the complete analysis from the project root

echo "=========================================="
echo "Cost of Living Index - 50 Indian Cities"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "src" ] || [ ! -d "data" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python3 -c "import pandas, numpy, matplotlib, seaborn, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: Required packages not installed"
    echo "Please run: pip install pandas numpy matplotlib seaborn openpyxl"
    exit 1
fi

echo "✓ All dependencies found"
echo ""

# Run the analysis
echo "Running analysis..."
echo ""
cd src
python3 main.py
cd ..

echo ""
echo "=========================================="
echo "Analysis Complete!"
echo "=========================================="
echo ""
echo "Results saved to:"
echo "  • CSV Report: outputs/reports/cost_index_results.csv"
echo "  • Visualizations: outputs/visualizations/"
echo ""
echo "Documentation available in: docs/"
echo ""
