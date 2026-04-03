# Expected Outputs & Observations

## Output Files

### 1. cost_index_results.csv
Complete dataset with the following columns:
- `City` - City name
- `avg_fuel_price` - Average fuel price (Petrol + Diesel)
- `uber_price_per_km` - Uber price per kilometer
- `doctor_fee` - General physician consultation fee
- `grocery_price` - Average grocery item price
- `housing_price` - Average housing price
- `housing_index` - Housing cost index (base = 100)
- `grocery_index` - Grocery cost index (base = 100)
- `transport_index` - Transportation cost index (base = 100)
- `healthcare_index` - Healthcare cost index (base = 100)
- `fuel_index` - Fuel cost index (base = 100)
- `cost_of_living_index` - Overall weighted cost index

### 2. Visualizations

#### a) top_bottom_cities.png
- Side-by-side bar charts
- Left: Top 10 most expensive cities
- Right: Top 10 most affordable cities
- Color-coded (red for expensive, green for affordable)

#### b) component_breakdown.png
- Grouped bar chart for top 10 cities
- Shows all 5 cost components side by side
- Helps identify which factors drive costs in each city

#### c) distribution.png
- 6 histogram subplots
- Shows distribution of each index across all cities
- Includes mean and base (100) reference lines

#### d) heatmap.png
- Color-coded matrix for top 20 cities
- Rows: Cities
- Columns: Cost components
- Color intensity shows relative cost (red = expensive, green = affordable)

## Expected Key Findings

### Typical Patterns

1. **Metropolitan Tier-1 Cities** (Expected High Index)
   - Mumbai, Bangalore, Delhi, Pune, Hyderabad
   - Driven primarily by housing costs
   - Index range: 100-140

2. **Tier-2 Cities** (Expected Medium Index)
   - Jaipur, Lucknow, Chandigarh, Indore, Bhopal
   - More balanced cost distribution
   - Index range: 70-100

3. **Tier-3 Cities** (Expected Low Index)
   - Smaller cities with lower housing costs
   - Index range: 50-70

### Component Insights

**Housing (40% weight)**
- Highest variation across cities
- Metropolitan areas 2-3x more expensive
- Primary driver of overall index differences

**Groceries (25% weight)**
- More uniform across cities
- Online platforms (Blinkit) reduce regional variation
- Typically 80-120 index range

**Transportation (15% weight)**
- Uber pricing relatively standardized
- Slight variations based on local regulations
- Range: 85-115

**Healthcare (10% weight)**
- Moderate variation
- Metropolitan areas have higher consultation fees
- Range: 70-130

**Fuel (10% weight)**
- Least variation (government regulated)
- Differences mainly due to state taxes
- Range: 90-110

## Sample Console Output

```
================================================================================
COST OF LIVING INDEX - 50 INDIAN CITIES
================================================================================

[1/5] Loading data from all sources...
  ✓ Loaded fuel prices for 45 cities
  ✓ Loaded Uber prices for 42 cities
  ✓ Loaded doctor fees for 48 cities
  ✓ Loaded grocery prices for 41 cities
  ✓ Loaded housing prices for 47 cities

[2/5] Merging datasets and calculating cost index...
  ✓ Merged data for 50 cities
  ✓ Calculated cost index (Base: Delhi = 100)

[3/5] Saving results...
  ✓ Saved complete results to: cost_index_results.csv

[4/5] Generating visualizations...
  ✓ All visualizations saved to 'visualizations/' folder

================================================================================
[5/5] SUMMARY & KEY FINDINGS
================================================================================

Total Cities Analyzed: 50
Base City: Delhi (Index = 100)

Most Expensive City: Mumbai (Index = 125.34)
Most Affordable City: Patna (Index = 62.18)

Average Index: 87.45
Median Index: 84.32

================================================================================
TOP 10 MOST EXPENSIVE CITIES
================================================================================

         City  cost_of_living_index  housing_index  grocery_index  transport_index
       Mumbai                125.34          145.2          108.5            112.3
    Bangalore                118.67          138.4          105.2            110.8
         Pune                112.45          128.9          102.1            108.5
    Hyderabad                108.23          122.5          101.8            106.2
        Delhi                100.00          100.0          100.0            100.0
      Chennai                 98.76          110.2           98.5            102.1
   Chandigarh                 95.34          105.8           96.2            101.5
      Kolkata                 92.18          102.3           95.8             99.8
    Ahmedabad                 89.45           98.7           94.5             98.2
       Jaipur                 86.23           95.4           93.1             97.5

================================================================================
KEY OBSERVATIONS
================================================================================

1. Housing costs vary significantly across cities
   Highest: Mumbai, Bangalore, Pune
   Lowest: Patna, Asansol, Jabalpur

2. Cost spread: 125.3 / 62.2 = 2.01x difference

3. 15 cities are more expensive than Delhi
   35 cities are more affordable than Delhi

================================================================================
✓ Analysis complete! Check 'visualizations/' folder for charts.
================================================================================
```

## Interpretation Guide

### For Individuals
- **Index < 80**: Significantly more affordable than Delhi
- **Index 80-95**: Moderately more affordable
- **Index 95-105**: Similar to Delhi
- **Index 105-120**: Moderately more expensive
- **Index > 120**: Significantly more expensive

### For Businesses
Use this data to:
- Set location-based salary adjustments
- Plan expansion strategies
- Optimize supply chain costs
- Understand market dynamics

### For Policy Makers
Insights for:
- Urban planning and development
- Affordable housing initiatives
- Transportation infrastructure
- Healthcare accessibility
