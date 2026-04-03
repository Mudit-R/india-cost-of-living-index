# Methodology: Cost of Living Index Calculation

## Overview
This project calculates a comprehensive Cost of Living Index for 50 Indian cities using real-world data from multiple sources.

## Data Sources

### 1. Housing Prices (40% weight)
- **Source**: MagicBricks property listings
- **Format**: Mixed (Excel .xlsx and CSV files)
- **Metric**: Average property prices/rent per city
- **Rationale**: Housing is typically the largest expense for urban households

### 2. Grocery Prices (25% weight)
- **Source**: Blinkit (online grocery delivery)
- **Format**: Excel files (.xlsx)
- **Metric**: Average price of fruits and vegetables
- **Rationale**: Food is the second-largest household expense

### 3. Transportation (15% weight)
- **Source**: Uber pricing data
- **Format**: Excel file (.xlsx)
- **Metric**: Price per kilometer
- **Rationale**: Daily commute is a significant recurring cost

### 4. Healthcare (10% weight)
- **Source**: General physician consultation fees
- **Format**: Excel file (.xlsx)
- **Metric**: Average consultation fee
- **Rationale**: Healthcare is an essential but less frequent expense

### 5. Fuel Prices (10% weight)
- **Source**: City-wise fuel pricing data
- **Format**: CSV file
- **Metric**: Average of petrol and diesel prices
- **Rationale**: Fuel costs affect personal transportation

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
Cost_Index = (Housing_Index × 0.40) + 
             (Grocery_Index × 0.25) + 
             (Transport_Index × 0.15) + 
             (Healthcare_Index × 0.10) + 
             (Fuel_Index × 0.10)
```

## Weightage Justification

The weights are based on typical urban household expenditure patterns in India:

| Category | Weight | Justification |
|----------|--------|---------------|
| Housing | 40% | Rent/EMI is the largest fixed expense for most households |
| Groceries | 25% | Daily food consumption is the second-largest expense |
| Transportation | 15% | Daily commute and travel costs |
| Healthcare | 10% | Essential but less frequent expense |
| Fuel | 10% | Affects personal vehicle owners |

**Total**: 100%

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
