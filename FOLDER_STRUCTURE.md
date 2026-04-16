# Project Folder Structure

## Overview
This project analyzes the cost of living across 50 Indian cities using real-world data.

## Directory Structure

```
project_root/
│
├── data/                          # All data files
│   ├── raw/                       # Original data sources
│   │   ├── housing/               # Housing price data
│   │   │   ├── magic_bricks_data/ # MagicBricks property listings (50 cities)
│   │   ├── grocery/               # Grocery price data
│   │   │   └── blinkit_citywise/  # Blinkit grocery prices (41 cities)
│   │   ├── transport/             # Transportation costs
│   │   │   ├── Fuel Prices by city (1).csv
│   │   │   └── City Wise Uber Price Per km .xlsx
│   │   ├── healthcare/            # Healthcare costs
│   │   │   └── General Physician Fee City wise.xlsx
│   │   ├── education/             # Education costs
│   │   │   ├── TutorData.csv
│   │   │   └── TutorData_Filtered.xlsx
│   │   ├── utilities/             # Utility costs
│   │   │   ├── Electricity Price.xlsx
│   │   │   └── Electricity Price (1).xlsx
│   │   └── entertainment/         # Entertainment costs
│   │       └── Movieticketprices.xlsx
│   │
│   └── processed/                 # Cleaned/processed data (generated)
│
├── src/                           # Source code
│   ├── data_loader.py            # Data loading and preprocessing
│   ├── cost_calculator.py        # Cost index calculations
│   ├── visualizer.py             # Visualization generation
│   ├── main.py                   # Main execution script
│   ├── ml_classification.py      # ML classification models
│   ├── ml_demo.py                # ML demonstration script
│   └── city-recommendation/      # City recommendation system
│       ├── recommender.py
│       └── cost_index_results.csv
│
├── outputs/                       # Generated outputs
│   ├── visualizations/           # All charts and graphs
│   │   ├── cost_of_living_all_cities.png
│   │   ├── cost_of_living_components_breakdown.png
│   │   ├── top_bottom_cities.png
│   │   ├── component_breakdown.png
│   │   ├── distribution.png
│   │   ├── heatmap.png
│   │   └── ... (other visualizations)
│   │
│   └── reports/                  # Generated reports and data
│       └── cost_index_results.csv
│
├── docs/                          # Documentation
│   ├── README.md                 # Project overview
│   ├── SETUP.md                  # Installation instructions
│   ├── METHODOLOGY.md            # Calculation methodology
│   ├── EXPECTED_OUTPUTS.md       # Output interpretation
│   ├── QUICK_START_GUIDE.md      # Quick start guide
│   ├── PROJECT_SUMMARY.md        # Detailed project summary
│   ├── ML_APPLICATIONS.md        # ML applications guide
│   ├── EDUCATION_INTEGRATION.md  # Education component details
│   ├── GET_STARTED.md            # Getting started guide
│   ├── INDEX.md                  # Documentation index
│   ├── WORKFLOW_DIAGRAM.txt      # Workflow diagram
│   └── PROJECT_FILES.txt         # File listing
│
├── tests/                         # Test files (to be added)
│
├── .gitignore                    # Git ignore file
├── requirements.txt              # Python dependencies
├── config.py                     # Configuration settings
└── analysis.ipynb                # Jupyter notebook for analysis

```

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the analysis:**
   ```bash
   cd src
   python main.py
   ```

3. **View results:**
   - CSV report: `outputs/reports/cost_index_results.csv`
   - Visualizations: `outputs/visualizations/`

## Data Sources

- **Housing**: MagicBricks property listings (50 cities, 51 files)
- **Grocery**: Blinkit online grocery prices (41 cities, 41 files)
- **Transport**: Uber per-km pricing + fuel prices (50 cities)
- **Healthcare**: General physician consultation fees (50 cities)
- **Education**: Tutor hourly rates (50 cities, 60K+ listings)
- **Utilities**: Electricity rates (50 cities)
- **Entertainment**: Movie ticket prices + restaurant costs (50 cities)

## Component Weights

The cost of living index uses the following weights (normalized to 100%):

- Housing: 30.30%
- Grocery: 36.36%
- Transport: 10.91%
- Healthcare: 6.42%
- Education: 6.06%
- Restaurant: 4.85%
- Electricity: 3.03%
- Movies: 2.07%

## Key Features

- ✅ 50 Indian cities analyzed
- ✅ 8 cost components tracked
- ✅ 94+ data files processed
- ✅ Weighted index calculation
- ✅ Multiple visualizations
- ✅ ML classification models
- ✅ City recommendation system
- ✅ Comprehensive documentation

## Documentation

See the `docs/` folder for detailed documentation:
- Setup and installation
- Methodology and calculations
- Expected outputs and interpretation
- ML applications
- Education component integration

## Contact

For questions or issues, refer to the documentation in the `docs/` folder.
