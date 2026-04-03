# Project Summary: Cost of Living Index for 50 Indian Cities

## Executive Summary

This project analyzes cost of living across 50 Indian cities using real-world data from e-commerce and online platforms. It produces a weighted Cost of Living Index that reflects actual household expenditure patterns, with Delhi as the base city (Index = 100).

## Problem Statement

Understanding cost of living variations across Indian cities is crucial for:
- Individuals making relocation decisions
- Companies setting location-based salaries
- Policy makers planning urban development
- Researchers studying urban economics

However, comprehensive, data-driven cost comparisons are often unavailable or outdated.

## Solution

A Python-based analytical tool that:
1. Aggregates data from 5 different sources (94+ data files)
2. Processes mixed formats (Excel, CSV, Numbers)
3. Handles missing data intelligently
4. Calculates weighted indices based on real expenditure patterns
5. Generates visualizations for easy interpretation
6. Exports results in CSV format

## Data Collection

### Sources & Coverage
- **Housing**: 51 files from MagicBricks (property listings)
- **Groceries**: 41 files from Blinkit (online grocery prices)
- **Transportation**: Uber per-km pricing data
- **Healthcare**: General physician consultation fees
- **Fuel**: City-wise petrol, diesel, CNG, LPG prices

### Data Quality
- Mixed formats handled automatically
- Missing values filled with median (robust to outliers)
- City name variations normalized
- Total coverage: ~50 cities across India

## Methodology

### Weightage System
Based on typical urban household expenditure (raw weights re-normalised to 100%):

```
Cost Index = (Groceries × 38.70%) + (Housing × 32.25%) +
             (Transport × 11.61%) + (Healthcare × 6.84%) +
             (Restaurants × 5.16%) + (Electricity × 3.23%) + (Movies × 2.21%)
```

### Calculation Process
1. Load and clean data from all sources
2. Normalize city names across datasets
3. Merge datasets on city
4. Fill missing values with median
5. Calculate component indices (Base city = 100)
6. Compute weighted overall index
7. Generate visualizations and export results

## Technical Implementation

### Architecture
- **Modular Design**: Separate modules for loading, calculation, visualization
- **Configurable**: Easy to adjust weights and base city
- **Extensible**: Simple to add new data sources
- **Reproducible**: Virtual environment with pinned dependencies

### Technology Stack
- **Language**: Python 3.8+
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **File Handling**: openpyxl (Excel), csv

### Code Structure
```
data_loader.py      → Load & preprocess data
cost_calculator.py  → Calculate indices
visualizer.py       → Generate charts
config.py           → Configuration
main.py             → Orchestration
```

## Deliverables

### 1. Code & Documentation
- 10 Python/config files
- 4 markdown documentation files
- Jupyter notebook for interactive analysis
- Test script for verification
- Setup automation script

### 2. Output Files
- **cost_index_results.csv**: Complete dataset with all metrics
- **4 Visualization files**: Charts showing different perspectives

### 3. Documentation
- **README.md**: Project overview and quick start
- **SETUP.md**: Detailed installation instructions
- **METHODOLOGY.md**: Calculation methodology
- **EXPECTED_OUTPUTS.md**: Output interpretation guide

## Key Insights (Expected)

### Cost Variation
- **Range**: 2-3x difference between most/least expensive cities
- **Primary Driver**: Grocery costs (38.70% weight)
- **Most Stable**: Fuel prices (government regulated)

### City Tiers
- **Tier-1 Metro**: Index 100-140 (Mumbai, Bangalore, Delhi)
- **Tier-2 Cities**: Index 70-100 (Jaipur, Lucknow, Indore)
- **Tier-3 Cities**: Index 50-70 (Smaller cities)

### Component Analysis
- **Housing**: Highest variation (2-3x)
- **Groceries**: Moderate variation (online platforms reduce gaps)
- **Transport**: Low variation (standardized pricing)
- **Healthcare**: Moderate variation (metro premium)
- **Fuel**: Minimal variation (state taxes only)

## Business Value

### For Individuals
- Make informed relocation decisions
- Negotiate location-based compensation
- Plan budgets for new cities

### For Businesses
- Set fair location-based salaries
- Optimize office location strategies
- Understand market dynamics

### For Policy Makers
- Identify affordability gaps
- Plan infrastructure investments
- Design targeted interventions

## Limitations & Future Work

### Current Limitations
1. Limited to 5 expense categories
2. Point-in-time data (not temporal)
3. Doesn't account for quality variations
4. Missing some smaller cities
5. No income/affordability analysis

### Proposed Enhancements
1. Add education, utilities, entertainment costs
2. Implement temporal tracking (monthly/yearly)
3. Include quality-of-life metrics
4. Add income data for affordability index
5. Implement regional clustering
6. Create web dashboard for interactive exploration

## Conclusion

This project successfully creates a data-driven, reproducible Cost of Living Index for Indian cities. The modular architecture makes it easy to update data, adjust weights, or add new categories. The comprehensive documentation ensures the project can be understood and extended by others.

The weighted approach (Groceries 38.70%, Housing 32.25%, Transport 11.61%, etc.) reflects real household expenditure patterns, making the index practical and relevant for decision-making.

## How to Use This Project

1. **Quick Analysis**: Run `./run.sh` to get results in minutes
2. **Custom Analysis**: Modify `config.py` to adjust weights or base city
3. **Interactive Exploration**: Use `analysis.ipynb` for custom queries
4. **Integration**: Import modules into your own Python projects

## Contact & Support

For questions or issues:
1. Check documentation files (SETUP.md, METHODOLOGY.md)
2. Run test script: `python test_data.py`
3. Review expected outputs: EXPECTED_OUTPUTS.md

---

**Project Status**: ✅ Complete and Ready to Use
**Last Updated**: March 2026
**Python Version**: 3.8+
