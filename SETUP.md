# Setup Instructions

## Quick Start

### Option 1: Using the run script (Recommended)
```bash
./run.sh
```

### Option 2: Manual setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the analysis
python main.py
```

### Option 3: Using Jupyter Notebook
```bash
# After setting up the virtual environment
source venv/bin/activate
pip install jupyter
jupyter notebook analysis.ipynb
```

## Output Files

After running the analysis, you'll get:

1. `cost_index_results.csv` - Complete dataset with all indices
2. `visualizations/` folder containing:
   - `top_bottom_cities.png` - Top 10 expensive vs affordable cities
   - `component_breakdown.png` - Breakdown by cost components
   - `distribution.png` - Distribution histograms
   - `heatmap.png` - Heatmap of cost components

## Project Structure

```
.
├── main.py                 # Main execution script
├── data_loader.py          # Data loading utilities
├── cost_calculator.py      # Index calculation logic
├── visualizer.py           # Visualization generation
├── config.py               # Configuration settings
├── analysis.ipynb          # Jupyter notebook for interactive analysis
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── SETUP.md               # This file
```

## Troubleshooting

### Issue: "externally-managed-environment" error
Solution: Use a virtual environment (see Option 2 above)

### Issue: Missing data files
Ensure all data files are in the correct locations:
- `Fuel Prices by city (1).csv`
- `City Wise Uber Price Per km .xlsx`
- `General Physician Fee City wise.xlsx`
- `blinkit_citywise/` folder
- `Magic Bricks data/` folder

### Issue: Import errors
Make sure you're in the virtual environment:
```bash
source venv/bin/activate
```
