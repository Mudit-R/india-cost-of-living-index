"""
Configuration file for Cost of Living Index Calculator
"""

# Weightages based on typical urban household expenditure patterns in India
# Source: Consumer Expenditure Survey patterns
COST_WEIGHTS = {
    'housing': 0.40,      # Rent/EMI is typically the largest expense
    'grocery': 0.25,      # Food and groceries
    'transportation': 0.15,  # Daily commute and travel
    'healthcare': 0.10,   # Medical consultations and healthcare
    'fuel': 0.10          # Personal vehicle fuel costs
}

# Base city for index calculation (index = 100)
BASE_CITY = 'Delhi'

# Data file paths
DATA_PATHS = {
    'fuel': 'Fuel Prices by city (1).csv',
    'uber': 'City Wise Uber Price Per km .xlsx',
    'doctor': 'General Physician Fee City wise.xlsx',
    'blinkit': 'blinkit_citywise',
    'housing': 'Magic Bricks data'
}

# Output settings
OUTPUT_DIR = 'visualizations'
RESULTS_FILE = 'cost_index_results.csv'

# Visualization settings
VIZ_CONFIG = {
    'top_n_cities': 10,
    'dpi': 300,
    'figsize': (12, 6),
    'color_expensive': '#e74c3c',
    'color_affordable': '#27ae60'
}
