# Methodology: Cost of Living Index Calculation

## Overview
This project calculates a comprehensive Cost of Living Index for 50 Indian cities using real-world data from multiple sources.

## Data Sources

### 1. Grocery Prices (38.70% normalised weight, raw: 30)
- **Source**: Blinkit (online grocery delivery)
- **Format**: Excel files (.xlsx)
- **Metric**: IQR-cleaned median price per city
- **Rationale**: Daily food consumption is the largest household expense

### 2. Housing Prices (32.25% normalised weight, raw: 25)
- **Source**: MagicBricks property listings
- **Format**: Mixed (Excel .xlsx and CSV files)
- **Metric**: IQR-cleaned median price per sq ft
- **Rationale**: Rent/EMI is the second-largest fixed expense

### 3. Transportation (11.61% normalised weight, raw: 9)
- **Source**: Uber pricing data
- **Format**: Excel file (.xlsx)
- **Metric**: Price per kilometer
- **Rationale**: Daily commute is a significant recurring cost

### 4. Healthcare (6.84% normalised weight, raw: 5.3)
- **Source**: General physician consultation fees
- **Format**: Excel file (.xlsx) — wide format, all observations per city
- **Metric**: IQR-cleaned median consultation fee
- **Rationale**: Healthcare is an essential but less frequent expense

### 5. Restaurants (5.16% normalised weight, raw: 4)
- **Source**: Swiggy restaurant dataset
- **Format**: Excel file (.xlsx)
- **Metric**: IQR-cleaned median per-person meal cost
- **Rationale**: Dining out / food delivery is a regular urban expense

### 6. Electricity (3.23% normalised weight, raw: 2.5)
- **Source**: City-wise electricity tariff data
- **Format**: Excel file (.xlsx)
- **Metric**: Effective rate (₹/unit)
- **Rationale**: Monthly utility bill affects all households

### 7. Movies (2.21% normalised weight, raw: 1.71)
- **Source**: City-wise movie ticket prices
- **Format**: Excel file (.xlsx)
- **Metric**: IQR-cleaned median ticket price
- **Rationale**: Entertainment proxy for discretionary spending

## Calculation Method

### Step 1: Data Normalization
- City names are standardized across datasets
- Missing values are filled with median values to handle outliers
- All prices are converted to numeric format

### Step 2: Index Calculation
For each cost component, we calculate an index relative to the base city (Delhi):

```
Component_Index = (City_Price / Base_City_Price) × 100
```

### Step 3: Weighted Average
The overall Cost of Living Index is calculated as:

```
Cost_Index = (Grocery_Index   × 0.3870) +
             (Housing_Index   × 0.3225) +
             (Transport_Index × 0.1161) +
             (Healthcare_Index× 0.0684) +
             (Restaurant_Index× 0.0516) +
             (Electricity_Index×0.0323) +
             (Movie_Index     × 0.0221)
```

> Raw weights (30, 25, 9, 5.3, 4, 2.5, 1.71) sum to 77.51 and are re-normalised to 100% at runtime.

## Weightage Justification

The weights are based on typical urban household expenditure patterns in India. Raw values are re-normalised to 100% at runtime.

| Category | Raw Weight | Normalised | Justification |
|----------|-----------|------------|---------------|
| Groceries | 30 | 38.70% | Daily food consumption — largest expense |
| Housing | 25 | 32.25% | Rent/EMI — major fixed cost |
| Transportation | 9 | 11.61% | Daily commute via ride-hailing |
| Healthcare | 5.3 | 6.84% | Essential medical services |
| Restaurants | 4 | 5.16% | Dining out / food delivery |
| Electricity | 2.5 | 3.23% | Monthly utility bill |
| Movies | 1.71 | 2.21% | Entertainment proxy |
| **Total** | **77.51** | **100%** | |

## Handling Missing Data

When data is missing for a city:
1. Calculate the median value across all cities for that metric
2. Fill missing values with the median
3. Log the imputation for transparency

This approach is more robust than using mean values, as it's less affected by outliers.

## Base City Selection

**Delhi** is chosen as the base city (Index = 100) because:
- It's the national capital with diverse economic activity
- Data availability is comprehensive
- It represents a mid-to-high cost metropolitan area
- Widely recognized reference point for Indian cities

## Interpretation

- **Index = 100**: Same cost as Delhi
- **Index > 100**: More expensive than Delhi
- **Index < 100**: More affordable than Delhi

Example:
- Mumbai with Index = 120 means it's 20% more expensive than Delhi
- Patna with Index = 75 means it's 25% more affordable than Delhi

## Limitations

1. **Data Freshness**: Data is from specific time periods and may not reflect current prices
2. **Sample Size**: Limited to available data points per city
3. **Lifestyle Variations**: Doesn't account for individual lifestyle differences
4. **Quality Differences**: Doesn't adjust for quality variations in housing/services
5. **Missing Categories**: Excludes education, entertainment, utilities, etc.

## Future Enhancements

1. Include more expense categories (education, utilities, entertainment)
2. Add temporal analysis to track changes over time
3. Incorporate quality-of-life metrics
4. Add income data for affordability analysis
5. Regional clustering and comparison
