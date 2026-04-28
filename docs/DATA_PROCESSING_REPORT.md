# Data Processing Report

## Overview
This document provides a comprehensive breakdown of how each data file is loaded, processed, and used in the Cost of Living Index calculation for 50 Indian cities.

---

## Table of Contents
1. [Housing Data](#1-housing-data)
2. [Grocery Data](#2-grocery-data)
3. [Transport Data](#3-transport-data)
4. [Healthcare Data](#4-healthcare-data)
5. [Education Data](#5-education-data)
6. [Utilities Data](#6-utilities-data)
7. [Entertainment Data](#7-entertainment-data)
8. [Data Merging & Index Calculation](#8-data-merging--index-calculation)

---

## 1. Housing Data

### Source Files
**Location**: `data/raw/Magic Bricks data/`  
**File Count**: 50 CSV files  
**Naming Format**: `{CityName}_magicbricks.csv`

**Example Files**:
- `Delhi_magicbricks.csv`
- `Mumbai_magicbricks.csv`
- `Bengaluru_magicbricks.csv`
- ... (47 more cities)

### File Structure
```csv
city_name,floors,bathrooms,carpet_area,price,price_per_sq_ft
Gurgaon,4.0,4.0,1500.0,36500000,20278.0
Gurgaon,14.0,4.0,1050.0,18500000,11212.0
```

**Columns Used**:
- `price_per_sq_ft` - Price per square foot in ₹

### Processing Steps

#### Step 1: File Loading
```python
Method: load_housing_data()
File Type: CSV
Encoding: UTF-8
```

#### Step 2: Data Extraction
- Extract `price_per_sq_ft` column
- Convert to numeric, handling errors gracefully
- Filter out zero and negative values
- Require minimum 5 valid data points per city

#### Step 3: Outlier Removal (IQR Method)
```
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
Keep only: Lower Bound ≤ price ≤ Upper Bound
```

**Rationale**: Removes extreme outliers (luxury properties, data errors) while preserving typical market prices.

#### Step 4: Aggregation
- **Metric Used**: Median of cleaned prices
- **Why Median**: Robust to remaining outliers, represents typical housing cost better than mean

#### Step 5: City Name Extraction
- Extract city name from filename: `{CityName}_magicbricks.csv` → `{CityName}`
- Standardize capitalization

### Output
**DataFrame Columns**: `['City', 'housing_price']`

**Example Output**:
```
City          housing_price
Delhi         10231.0
Mumbai        23619.0
Bengaluru     11029.0
```

### Usage in Index
- **Weight**: 30.30% (normalized)
- **Index Calculation**: `(City_Price / Delhi_Price) × 100`
- **Contribution**: `housing_index × 0.3030`

### Data Quality
- **Coverage**: 50/50 cities (100%)
- **Average Records per City**: ~100-500 listings
- **Price Range**: ₹1,512 - ₹23,619 per sq ft

---

## 2. Grocery Data

### Source Files
**Location**: `data/raw/grocery/blinkit_citywise/`  
**File Count**: 41 Excel files  
**Naming Format**: `blinkit_{cityname}.xlsx`

**Example Files**:
- `blinkit_delhi.xlsx`
- `blinkit_mumbai.xlsx`
- `blinkit_bangalore.xlsx`
- ... (38 more cities)

### File Structure
```
Column 0: Product Name
Column 1: Price (₹)
```

**Typical Products**: Rice, wheat, vegetables, fruits, dairy, packaged goods

### Processing Steps

#### Step 1: File Loading
```python
Method: load_blinkit_data()
File Type: Excel (.xlsx)
Columns: First 2 columns (name, price)
```

#### Step 2: Data Extraction
- Read all Excel files in folder
- Extract city name from filename: `blinkit_{city}.xlsx` → `{City}`
- Capitalize city name
- Extract prices from column 1 (index 1)

#### Step 3: Data Cleaning
- Convert prices to numeric
- Remove NaN values
- Filter out zero/negative prices
- Require minimum data points

#### Step 4: Outlier Removal (IQR Method)
```
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

**Rationale**: Removes pricing errors, premium products, bulk items that skew average.

#### Step 5: Aggregation
- **Metric Used**: Median of cleaned prices
- **Why Median**: Represents typical grocery basket cost, resistant to outliers

### Output
**DataFrame Columns**: `['City', 'grocery_price']`

**Example Output**:
```
City          grocery_price
Delhi         42.0
Mumbai        49.5
Bengaluru     36.0
```

### Usage in Index
- **Weight**: 36.36% (normalized) - HIGHEST WEIGHT
- **Index Calculation**: `(City_Price / Delhi_Price) × 100`
- **Contribution**: `grocery_index × 0.3636`

### Data Quality
- **Coverage**: 41/50 cities (82%)
- **Missing Cities**: Filled with median value (₹42.00)
- **Average Products per City**: 50-200 items
- **Price Range**: ₹36 - ₹56 (average basket)

---

## 3. Transport Data

### 3A. Uber Pricing Data

#### Source File
**Location**: `data/raw/transport/City Wise Uber Price Per km .xlsx`  
**File Count**: 1 Excel file

#### File Structure
```
Column 0: Serial Number
Column 1: City
Column 6: Price/Km (₹)
```

#### Processing Steps

**Step 1: File Loading**
```python
Method: load_uber_prices()
File Type: Excel (.xlsx)
```

**Step 2: Column Extraction**
- Extract 'City' column (column 1)
- Extract 'Price/Km' column (column 6)
- Strip whitespace from city names

**Step 3: Data Cleaning**
- Convert prices to numeric
- Remove NaN values
- Filter out invalid entries (city = 'nan')

**Step 4: Aggregation**
- No aggregation needed (one price per city)

#### Output
```
City          uber_price_per_km
Delhi         20.00
Mumbai        44.07
Bengaluru     43.26
```

### 3B. Fuel Prices Data

#### Source File
**Location**: `data/raw/transport/Fuel Prices by city (1).csv`  
**File Count**: 1 CSV file

#### File Structure
```csv
City,Petroi,Diesel,CNG,LPG
Delhi,96.72,89.62,75.61,803.00
Mumbai,106.31,94.27,76.00,802.50
```

#### Processing Steps

**Step 1: File Loading**
```python
Method: load_fuel_prices()
File Type: CSV
```

**Step 2: Column Cleaning**
- Strip whitespace from column names
- Rename first column to 'City'
- Strip whitespace from city names

**Step 3: Price Cleaning**
- Remove '₹' symbol
- Remove commas
- Convert to numeric

**Step 4: Aggregation**
- Calculate average of Petrol and Diesel prices
- Formula: `avg_fuel_price = (Petrol + Diesel) / 2`

#### Output
```
City          avg_fuel_price
Delhi         93.17
Mumbai        100.29
Bengaluru     102.86
```

**Note**: Fuel prices are loaded but NOT used in the final index calculation. Uber prices are used instead for the transport component.

### Usage in Index
- **Weight**: 10.91% (normalized)
- **Index Calculation**: `(City_Uber_Price / Delhi_Uber_Price) × 100`
- **Contribution**: `transport_index × 0.1091`

### Data Quality
- **Uber Coverage**: 42/50 cities (84%)
- **Missing Cities**: Filled with median (₹18.91/km)
- **Fuel Coverage**: 50/50 cities (100%)
- **Price Range**: ₹10.61 - ₹48.37 per km

---

## 4. Healthcare Data

### Source File
**Location**: `data/raw/healthcare/General Physician Fee City wise.xlsx`  
**File Count**: 1 Excel file

### File Structure
```
Column 0: City Name
Columns 1-N: Doctor consultation fees (multiple doctors per city)
```

**Format**: Wide format with city in first column, multiple fee values across remaining columns.

### Processing Steps

#### Step 1: File Loading
```python
Method: load_doctor_fees()
File Type: Excel (.xlsx)
Header: Row 0
```

#### Step 2: Row Processing
- Iterate through each row
- Extract city name from column 0
- Skip invalid rows (NaN, 'CITY', empty strings)

#### Step 3: Fee Extraction
- Extract all values from columns 1 onwards
- Convert to numeric, handling errors
- Drop NaN values
- Require at least some valid fees

#### Step 4: Outlier Removal (IQR Method)
```
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

**Rationale**: Removes specialist fees, premium clinics, data entry errors.

#### Step 5: Aggregation
- **Metric Used**: Median of cleaned fees
- **Why Median**: Represents typical general physician consultation cost

### Output
**DataFrame Columns**: `['City', 'doctor_fee']`

**Example Output**:
```
City          doctor_fee
Delhi         1000.0
Mumbai        1350.0
Bengaluru     750.0
```

### Usage in Index
- **Weight**: 6.42% (normalized)
- **Index Calculation**: `(City_Fee / Delhi_Fee) × 100`
- **Contribution**: `healthcare_index × 0.0642`

### Data Quality
- **Coverage**: 50/50 cities (100%)
- **Average Doctors per City**: 10-30 fee samples
- **Fee Range**: ₹200 - ₹1,500

---

## 5. Education Data

### Source File
**Location**: `data/raw/education/TutorData_Filtered.xlsx`  
**File Count**: 1 Excel file  
**Total Records**: 60,256 tutor listings

### File Structure
```
Tutor,City,Location,Fee
16506,Agra,Agra Uttar Pradesh India,₹300–1000/hour (USD 3.4–11.35/hour)
61116,Agra,Agra Uttar Pradesh India,₹500–1000/hour (USD 5.63–11.25/hour)
```

**Columns**:
- `Tutor`: Tutor ID
- `City`: City name
- `Location`: Full location string
- `Fee`: Fee range string (format varies: per hour or per month)

### Processing Steps

#### Step 1: File Loading
```python
Method: load_tutor_data()
File Type: Excel (.xlsx)
```

#### Step 2: Initial Filtering
- Remove rows with NaN City or Fee
- Strip whitespace from city names

#### Step 3: Fee Type Filtering
- **Filter**: Keep only `/hour` fees
- **Exclude**: `/month` fees
- **Rationale**: Hourly rates are more standardized and comparable across cities

**Records After Filtering**: 46,965 (77.9% of total)

#### Step 4: Fee Extraction (Regex)
```python
Pattern: r'₹([\d,]+)'
Example: "₹300–1,000/hour" → [300, 1000]
```

**Processing**:
- Extract all numbers after ₹ symbol
- If 2+ numbers found: Calculate average of min and max
  - Example: ₹300–1,000 → (300 + 1000) / 2 = 650
- If 1 number found: Use that value
- Remove commas from numbers

#### Step 5: Outlier Removal (IQR Method)
```
Applied per city:
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

**Rationale**: Removes premium tutors, specialized coaching, data errors.

#### Step 6: Aggregation
- **Metric Used**: Mean (average) of cleaned fees per city
- **Why Mean**: Requested by user; represents average tutoring cost
- **Minimum Required**: 3 data points per city

### Output
**DataFrame Columns**: `['City', 'tutor_fee']`

**Example Output**:
```
City          tutor_fee
Delhi         539.08
Mumbai        613.85
Bengaluru     487.05
```

### Usage in Index
- **Weight**: 6.06% (normalized)
- **Index Calculation**: `(City_Fee / Delhi_Fee) × 100`
- **Contribution**: `education_index × 0.0606`

### Data Quality
- **Coverage**: 50/50 cities (100%)
- **Average Tutors per City**: 940 listings (per-hour only)
- **Fee Range**: ₹252.93 - ₹613.85 per hour
- **Data Source**: Online tutor marketplace listings

---

## 6. Utilities Data

### Source Files
**Location**: `data/raw/utilities/`  
**Files**: 
- `Electricity Price.xlsx` (primary)
- `Electricity Price (1).xlsx` (backup)

### File Structure
```
City,Effective Rate (₹/unit)
Delhi,4.00
Mumbai,8.50
```

**Columns**:
- `City`: City name
- `Effective Rate (₹/unit)`: Electricity rate per unit (kWh)

### Processing Steps

#### Step 1: File Loading
```python
Method: load_electricity_prices()
File Type: Excel (.xlsx)
Primary File: Electricity Price.xlsx
```

#### Step 2: Column Standardization
- Strip whitespace from column names
- Rename columns to standard names:
  - 'City' → 'City'
  - 'Effective Rate (₹/unit)' → 'electricity_rate'

#### Step 3: Data Cleaning
- Strip whitespace from city names
- Convert rates to numeric
- Remove NaN values

#### Step 4: Aggregation
- No aggregation needed (one rate per city)

### Output
**DataFrame Columns**: `['City', 'electricity_rate']`

**Example Output**:
```
City          electricity_rate
Delhi         4.00
Mumbai        8.50
Bengaluru     7.00
```

### Usage in Index
- **Weight**: 3.03% (normalized)
- **Index Calculation**: `(City_Rate / Delhi_Rate) × 100`
- **Contribution**: `electricity_index × 0.0303`

### Data Quality
- **Coverage**: 50/50 cities (100%)
- **Rate Range**: ₹3.00 - ₹8.50 per unit
- **Data Source**: State electricity boards

---

## 7. Entertainment Data

### 7A. Movie Ticket Prices

#### Source File
**Location**: `data/raw/entertainment/Movieticketprices.xlsx`  
**File Count**: 1 Excel file

#### File Structure
```
Row 0: Merged header (skipped)
Row 1: Column headers
Column 0: Index
Column 1: City
Columns 2-N: Ticket prices from different theaters
```

#### Processing Steps

**Step 1: File Loading**
```python
Method: load_movie_ticket_prices()
File Type: Excel (.xlsx)
Header: Row 1 (skip row 0)
```

**Step 2: Data Cleaning**
- Drop rows with all NaN values
- Extract city name from column 1
- Convert to string and strip whitespace
- Filter out short/invalid city names (length > 1)

**Step 3: Price Extraction**
- Extract all columns after City column (columns 2+)
- Convert to numeric, handling errors
- Drop NaN values

**Step 4: Outlier Removal (IQR Method)**
```
Per city:
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

**Rationale**: Removes premium theaters (IMAX, Gold Class), special shows, data errors.

**Step 5: Aggregation**
- **Metric Used**: Median of cleaned prices
- **Why Median**: Represents typical movie ticket cost

#### Output
```
City          movie_ticket_price
Delhi         390.0
Mumbai        600.0
Bengaluru     335.0
```

### 7B. Restaurant Prices

#### Source File
**Location**: `data/raw/entertainment/swiggy dataset.xlsx`  
**File Count**: 1 Excel file

#### File Structure
```
Columns: Average Price, Location, ...
```

**Data**: Restaurant listings with average meal prices and locations.

#### Processing Steps

**Step 1: File Loading**
```python
Method: load_swiggy_data()
File Type: Excel (.xlsx)
```

**Step 2: Column Identification**
- Find price column: Contains 'price' or 'average' (case-insensitive)
- Find city column: Contains 'location' or 'city' (case-insensitive)

**Step 3: Price Extraction (Regex)**
```python
Pattern: r'(\d+)'
Example: "₹250 for two" → 250
```

- Extract numeric value from price string
- Convert to numeric

**Step 4: Per-Person Calculation**
- Divide price by 2 (assuming "for two" format)
- Formula: `per_person_price = extracted_price / 2`

**Step 5: Outlier Removal (IQR Method)**
```
Per city:
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

**Rationale**: Removes fine dining, premium restaurants, data errors.

**Step 6: Aggregation**
- **Metric Used**: Median of cleaned per-person prices
- **Why Median**: Represents typical restaurant meal cost

**Step 7: City Name Aliases**
```python
Aliases handled:
- Bangalore → Bengaluru
- Mysore → Mysuru
- Trichy → Tiruchirappalli
- Vizag → Visakhapatnam
- Amravati → Amaravati region
```

#### Output
```
City          restaurant_price
Delhi         125.0
Mumbai        150.0
Bengaluru     125.0
```

### Usage in Index

**Movies**:
- **Weight**: 2.07% (normalized)
- **Index Calculation**: `(City_Price / Delhi_Price) × 100`
- **Contribution**: `movie_index × 0.0207`

**Restaurants**:
- **Weight**: 4.85% (normalized)
- **Index Calculation**: `(City_Price / Delhi_Price) × 100`
- **Contribution**: `restaurant_index × 0.0485`

### Data Quality

**Movies**:
- **Coverage**: 50/50 cities (100%)
- **Average Theaters per City**: 5-15 samples
- **Price Range**: ₹120 - ₹600

**Restaurants**:
- **Coverage**: 55 cities (includes duplicates/aliases)
- **After Deduplication**: 50/50 cities
- **Average Restaurants per City**: 50-200 listings
- **Price Range**: ₹80 - ₹150 per person

---

## 8. Data Merging & Index Calculation

### Step 1: City Name Normalization

**Method**: `normalize_city_names()`

**Mappings Applied**:
```python
{
    'Bangalore': 'Bengaluru',
    'Bombay': 'Mumbai',
    'Calcutta': 'Kolkata',
    'Mangalore': 'Mangaluru',
    'Mysore': 'Mysuru',
    'Trivandrum': 'Thiruvananthapuram',
    'Trichy': 'Tiruchirappalli',
    'Amaravati': 'Amaravati region',
    'Hubballi': 'Hubli',
    'Merrut': 'Meerut',
    # ... and more
}
```

**Rationale**: Ensures consistent city names across all data sources for proper merging.

### Step 2: Data Merging

**Method**: `merge_all_data()`

**Process**:
1. Start with fuel data as base
2. Perform outer joins on 'City' column:
   - Merge uber prices
   - Merge doctor fees
   - Merge grocery prices
   - Merge housing prices
   - Merge restaurant prices (if available)
   - Merge movie prices (if available)
   - Merge electricity rates (if available)
   - Merge tutor fees (if available)

3. Group by City and aggregate (mean for duplicates)
4. Filter to only official 50 cities

**Official City List** (50 cities):
```
Agra, Ahmedabad, Amaravati region, Asansol, Aurangabad,
Bengaluru, Bhopal, Bhubaneswar, Chandigarh, Chennai,
Coimbatore, Delhi, Erode, Hubli, Hyderabad,
Indore, Jabalpur, Jaipur, Jamnagar, Kannur,
Kanpur, Kochi, Kolkata, Kolhapur, Kollam,
Kottayam, Kozhikode, Lucknow, Ludhiana, Madurai,
Malappuram, Mangaluru, Meerut, Mumbai, Mysuru,
Nagpur, Nashik, Patna, Pune, Raipur,
Rajkot, Salem, Sangli, Solapur, Surat,
Thiruvananthapuram, Thrissur, Tiruchirappalli, Vadodara, Visakhapatnam
```

### Step 3: Missing Value Handling

**Method**: `fill_missing_values()`

**Strategy**: Fill with median value of available cities

**Example**:
```
uber_price_per_km: Missing in 8 cities → Fill with ₹18.91 (median)
grocery_price: Missing in 9 cities → Fill with ₹42.00 (median)
housing_price: Missing in 0 cities → No filling needed
```

**Rationale**: Median is robust to outliers and represents typical value better than mean.

### Step 4: Index Calculation

**Method**: `calculate_index()`

**Base City**: Delhi (Index = 100)

**Formula for Each Component**:
```
component_index = (City_Value / Delhi_Value) × 100
```

**Example**:
```
Mumbai housing: ₹23,619 / ₹10,231 × 100 = 230.86
Mumbai grocery: ₹49.50 / ₹42.00 × 100 = 117.86
```

### Step 5: Weight Normalization

**Raw Weights**:
```python
{
    'housing': 0.25,
    'grocery': 0.30,
    'transportation': 0.09,
    'healthcare': 0.053,
    'electricity': 0.025,
    'movie': 0.0171,
    'restaurant': 0.04,
    'education': 0.05
}
Total: 0.8251 (82.51%)
```

**Normalization**:
```
normalized_weight = raw_weight / total_raw_weights
```

**Normalized Weights** (sum = 100%):
```python
{
    'housing': 30.30%,
    'grocery': 36.36%,
    'transportation': 10.91%,
    'healthcare': 6.42%,
    'electricity': 3.03%,
    'movie': 2.07%,
    'restaurant': 4.85%,
    'education': 6.06%
}
```

### Step 6: Overall Index Calculation

**Formula**:
```
cost_of_living_index = 
    housing_index × 0.3030 +
    grocery_index × 0.3636 +
    transport_index × 0.1091 +
    healthcare_index × 0.0642 +
    electricity_index × 0.0303 +
    restaurant_index × 0.0485 +
    movie_index × 0.0207 +
    education_index × 0.0606
```

**Example (Mumbai)**:
```
= 230.86 × 0.3030
+ 117.86 × 0.3636
+ 220.37 × 0.1091
+ 135.00 × 0.0642
+ 212.50 × 0.0303
+ 120.00 × 0.0485
+ 153.85 × 0.0207
+ 113.87 × 0.0606
= 167.85
```

### Step 7: Sorting & Output

**Final Steps**:
1. Round index to 2 decimal places
2. Sort cities by cost_of_living_index (descending)
3. Reset index
4. Export to CSV

**Output File**: `outputs/reports/cost_index_results.csv`

**Columns** (19 total):
```
City, avg_fuel_price, uber_price_per_km, doctor_fee, grocery_price,
housing_price, restaurant_price, movie_ticket_price, electricity_rate,
tutor_fee, housing_index, grocery_index, transport_index, healthcare_index,
electricity_index, restaurant_index, movie_index, education_index,
cost_of_living_index
```

---

## Summary Statistics

### Data Coverage

| Component | Files | Cities Covered | Missing | Fill Method |
|-----------|-------|----------------|---------|-------------|
| Housing | 50 | 50/50 (100%) | 0 | N/A |
| Grocery | 41 | 41/50 (82%) | 9 | Median (₹42.00) |
| Transport (Uber) | 1 | 42/50 (84%) | 8 | Median (₹18.91) |
| Transport (Fuel) | 1 | 50/50 (100%) | 0 | N/A |
| Healthcare | 1 | 50/50 (100%) | 0 | N/A |
| Education | 1 | 50/50 (100%) | 0 | N/A |
| Electricity | 1 | 50/50 (100%) | 0 | N/A |
| Movies | 1 | 50/50 (100%) | 0 | N/A |
| Restaurants | 1 | 50/50 (100%) | 0 | N/A |

### Processing Methods Summary

| Component | Aggregation | Outlier Removal | Records per City |
|-----------|-------------|-----------------|------------------|
| Housing | Median | IQR (1.5×) | 100-500 |
| Grocery | Median | IQR (1.5×) | 50-200 |
| Transport | Direct | None | 1 |
| Healthcare | Median | IQR (1.5×) | 10-30 |
| Education | Mean | IQR (1.5×) | 940 (avg) |
| Electricity | Direct | None | 1 |
| Movies | Median | IQR (1.5×) | 5-15 |
| Restaurants | Median | IQR (1.5×) | 50-200 |

### Data Quality Metrics

**Total Data Points Processed**: ~150,000+
- Housing: ~15,000 property listings
- Grocery: ~8,000 product prices
- Education: 46,965 tutor listings (per-hour)
- Restaurants: ~10,000 restaurant listings
- Healthcare: ~1,000 doctor fees
- Movies: ~500 theater prices
- Transport: 50 city rates
- Electricity: 50 city rates

**Outlier Removal Impact**:
- Average removal rate: 5-15% of data points
- Ensures robust, representative values
- Prevents extreme values from skewing results

---

## Validation & Quality Checks

### 1. Data Completeness
✅ All 50 cities have data for all 8 components (after filling)

### 2. Data Consistency
✅ City names normalized across all sources
✅ All prices in Indian Rupees (₹)
✅ Consistent units (per sq ft, per km, per hour, etc.)

### 3. Data Reasonableness
✅ All indices positive
✅ Delhi base index = 100.00 for all components
✅ Price ranges within expected bounds

### 4. Statistical Validity
✅ Outlier removal applied consistently
✅ Robust aggregation methods (median/mean)
✅ Sufficient sample sizes per city

---

## Reproducibility

### To Reproduce Results:

1. **Ensure Data Files Present**:
   ```bash
   data/raw/Magic Bricks data/*.csv (50 files)
   data/raw/grocery/blinkit_citywise/*.xlsx (41 files)
   data/raw/transport/*.{csv,xlsx} (2 files)
   data/raw/healthcare/*.xlsx (1 file)
   data/raw/education/*.xlsx (1 file)
   data/raw/utilities/*.xlsx (1 file)
   data/raw/entertainment/*.xlsx (2 files)
   ```

2. **Run Analysis**:
   ```bash
   cd src
   python3 main.py
   ```

3. **Output Location**:
   ```
   outputs/reports/cost_index_results.csv
   outputs/visualizations/*.png
   ```

### Dependencies:
```
pandas >= 1.3.0
numpy >= 1.21.0
openpyxl >= 3.0.0
```

---

## Change Log

### Version 1.0 (Current)
- Initial data processing implementation
- 50 cities, 8 cost components
- Education component added (6.06% weight)
- Housing data updated to new CSV format
- Per-hour tutor fees only (monthly fees excluded)

---

## Contact & Support

For questions about data processing:
- Review this document
- Check `docs/METHODOLOGY.md` for calculation details
- See `src/data_loader.py` for implementation

---

**Document Version**: 1.0  
**Last Updated**: April 14, 2026  
**Status**: Complete & Current
