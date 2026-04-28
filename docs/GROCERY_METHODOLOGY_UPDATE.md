# Grocery Data Processing - Updated Methodology

## Overview
The grocery data processing has been updated to use **product-level price comparison** instead of median pricing. This provides a more accurate, apples-to-apples comparison of grocery costs across cities.

---

## Old Method vs New Method

### ❌ Old Method: Median of All Prices

**Process**:
1. Load all product prices for each city
2. Calculate median price across all products
3. Compare median values across cities

**Problems**:
- Compared different product mixes
- Affected by product availability differences
- Not a true cost comparison
- Example: Delhi ₹42, Mumbai ₹49.5

**Result**: Inaccurate comparison because cities might have different products.

---

### ✅ New Method: Product-Level Price Comparison

**Process**:
1. Load all products and prices for each city
2. Normalize product names (remove regional variations)
3. Identify common products across cities
4. Compare prices for the SAME products
5. Calculate average price ratio

**Advantages**:
- True apples-to-apples comparison
- Compares same products across cities
- More accurate cost difference measurement
- Accounts for regional availability

**Result**: Accurate comparison of actual grocery costs.

---

## Detailed Processing Steps

### Step 1: Data Loading

**Source**: `data/raw/grocery/blinkit_citywise/*.xlsx` (41 files)

**File Structure**:
```
Name                                    Original Price  Discounted Price
Onion (Pyaz)                           36              29
Potato (Alugadde)                      38              28
Coriander Bunch (Dhaniya Patta)        7               1
```

### Step 2: Product Name Normalization

**Purpose**: Enable matching of same products across cities despite regional name variations.

**Process**:
```python
# Original names (with regional variations)
"Onion (Pyaz)"           → "onion"
"Onion (Eerulli)"        → "onion"
"Potato (Alugadde)"      → "potato"
"Potato (Aloo)"          → "potato"
"Coriander (Dhaniya)"    → "coriander"
```

**Method**:
- Remove text in parentheses (regional names)
- Convert to lowercase
- Strip whitespace

### Step 3: Common Product Identification

**Process**:
- For each city, identify products also available in Delhi (base city)
- Require minimum 5 common products for valid comparison

**Statistics**:
- Average common products per city: **38 products**
- Range: 25-60 common products
- Common products include: onion, potato, tomato, rice, wheat, milk, eggs, etc.

**Example**:
```
Delhi has: [onion, potato, tomato, rice, wheat, milk, ...]
Mumbai has: [onion, potato, tomato, rice, wheat, milk, ...]
Common: [onion, potato, tomato, rice, wheat, milk, ...]
```

### Step 4: Price Ratio Calculation

**For each common product**:
```python
price_ratio = city_price / delhi_price
```

**Example**:
```
Product: Onion
Delhi Price: ₹29
Mumbai Price: ₹30
Ratio: 30/29 = 1.034 (3.4% more expensive)

Product: Potato  
Delhi Price: ₹28
Mumbai Price: ₹27
Ratio: 27/28 = 0.964 (3.6% cheaper)

Product: Tomato
Delhi Price: ₹35
Mumbai Price: ₹38
Ratio: 38/35 = 1.086 (8.6% more expensive)
```

### Step 5: Outlier Filtering

**Filter out extreme ratios**:
- Remove ratios < 0.1 (90% cheaper - likely error)
- Remove ratios > 10 (10x more expensive - likely error)

**Rationale**: Removes data entry errors, different product variants (organic vs regular), bulk vs retail pricing.

### Step 6: Average Ratio Calculation

**Formula**:
```python
avg_ratio = mean(all_price_ratios)
```

**Example (Mumbai)**:
```
Ratios: [1.034, 0.964, 1.086, 1.050, 0.980, ...]
Average: 1.039
```

**Interpretation**: On average, Mumbai groceries are 3.9% more expensive than Delhi.

### Step 7: Index Calculation

**Formula**:
```python
grocery_index = avg_ratio × 100
```

**Example**:
```
Mumbai: 1.039 × 100 = 103.9
Kozhikode: 1.512 × 100 = 151.2
Bengaluru: 0.998 × 100 = 99.8
```

### Step 8: Normalization

**Ensure Delhi = 100**:
```python
normalized_index = (grocery_index / delhi_index) × 100
```

---

## Results Comparison

### Top 10 Most Expensive (New Method)

| Rank | City | Grocery Index | Interpretation |
|------|------|---------------|----------------|
| 1 | Kozhikode | 151.2 | 51% more expensive than Delhi |
| 2 | Coimbatore | 140.2 | 40% more expensive than Delhi |
| 3 | Bhopal | 134.8 | 35% more expensive than Delhi |
| 4 | Raipur | 124.9 | 25% more expensive than Delhi |
| 5 | Bhubaneswar | 124.3 | 24% more expensive than Delhi |
| 6 | Jabalpur | 123.3 | 23% more expensive than Delhi |
| 7 | Thrissur | 121.9 | 22% more expensive than Delhi |
| 8 | Asansol | 121.8 | 22% more expensive than Delhi |
| 9 | Jaipur | 121.0 | 21% more expensive than Delhi |
| 10 | Erode | 119.7 | 20% more expensive than Delhi |

### Top 10 Most Affordable (New Method)

| Rank | City | Grocery Index | Interpretation |
|------|------|---------------|----------------|
| 1 | Nashik | 90.9 | 9% cheaper than Delhi |
| 2 | Mysuru | 95.1 | 5% cheaper than Delhi |
| 3 | Solapur | 96.0 | 4% cheaper than Delhi |
| 4 | Pune | 97.5 | 2.5% cheaper than Delhi |
| 5 | Kolhapur | 97.6 | 2.4% cheaper than Delhi |
| 6 | Bengaluru | 99.8 | 0.2% cheaper than Delhi |
| 7 | Delhi | 100.0 | Base city |
| 8 | Ludhiana | 100.8 | 0.8% more expensive |
| 9 | Meerut | 101.0 | 1% more expensive |
| 10 | Nagpur | 101.0 | 1% more expensive |

---

## Key Insights

### Distribution
- **43 cities** (86%) have higher grocery costs than Delhi
- **6 cities** (12%) have lower grocery costs than Delhi
- **1 city** (2%) is the base (Delhi)

### Price Variation
- **Maximum**: Kozhikode at 151.2 (51% more expensive)
- **Minimum**: Nashik at 90.9 (9% cheaper)
- **Range**: 60.3 index points
- **Standard Deviation**: ~12 index points

### Regional Patterns
**More Expensive**:
- Kerala cities (Kozhikode, Thrissur, Kollam)
- Tier-2 cities in central India (Bhopal, Raipur, Jabalpur)
- Some Tamil Nadu cities (Coimbatore, Erode)

**More Affordable**:
- Maharashtra cities (Nashik, Pune, Solapur)
- Karnataka cities (Mysuru, Bengaluru)
- Some northern cities (Ludhiana, Meerut)

---

## Impact on Overall Rankings

### Before (Old Method)
```
1. Mumbai - 167.85
2. Bengaluru - 109.64
3. Kozhikode - 101.16
4. Hyderabad - 100.18
5. Delhi - 100.00
```

### After (New Method)
```
1. Mumbai - 162.79
2. Bengaluru - 114.76
3. Kozhikode - 107.66
4. Hyderabad - 107.09
5. Patna - 100.72
```

**Changes**:
- Kozhikode moved up (higher grocery costs revealed)
- Patna entered top 5 (higher grocery costs revealed)
- Overall rankings more accurate

---

## Data Quality

### Coverage
- **Cities with data**: 41/50 (82%)
- **Missing cities**: 9 (filled with median)
- **Average common products**: 38 per city
- **Minimum common products**: 25 per city

### Validation
✅ All price ratios within reasonable range (0.1 - 10)  
✅ Sufficient common products for comparison  
✅ Delhi base index = 100.00  
✅ Results align with known cost patterns  

---

## Technical Implementation

### Code Location
`src/data_loader.py` → `load_blinkit_data()` method

### Key Functions
```python
# Product name normalization
normalized = re.sub(r'\s*\([^)]*\)', '', product_name)
normalized = normalized.strip().lower()

# Price ratio calculation
ratio = city_price / delhi_price

# Average ratio
avg_ratio = np.mean(price_ratios)

# Index calculation
grocery_index = avg_ratio * 100
```

### Dependencies
- pandas
- numpy
- re (regex)

---

## Reproducibility

### To Reproduce Results:

1. **Ensure data files present**:
   ```
   data/raw/grocery/blinkit_citywise/*.xlsx (41 files)
   ```

2. **Run analysis**:
   ```bash
   cd src
   python3 main.py
   ```

3. **Check output**:
   ```
   outputs/reports/cost_index_results.csv
   Column: grocery_index
   ```

### Expected Output
```
Grocery Price Comparison Summary:
  Base city: Delhi
  Cities with data: 41
  Avg common products: 38
  Method: Product-level price comparison
```

---

## Advantages Summary

### Accuracy
✅ True apples-to-apples comparison  
✅ Same products compared across cities  
✅ Eliminates product mix bias  

### Reliability
✅ Based on actual product prices  
✅ Robust to product availability differences  
✅ Transparent methodology  

### Interpretability
✅ Clear meaning: "X% more/less expensive than Delhi"  
✅ Based on common household items  
✅ Reflects actual shopping experience  

---

## Future Enhancements

### Potential Improvements
1. **Product Weighting**: Weight products by consumption frequency
2. **Seasonal Adjustment**: Account for seasonal price variations
3. **Product Categories**: Separate indices for vegetables, grains, dairy, etc.
4. **Quality Adjustment**: Account for organic vs regular products
5. **Basket Standardization**: Use standard grocery basket (WHO/FAO guidelines)

---

## Conclusion

The new product-level price comparison method provides a more accurate and meaningful measure of grocery costs across Indian cities. By comparing the same products, we eliminate the bias introduced by different product mixes and availability, resulting in a true cost-of-living comparison.

---

**Method**: Product-Level Price Comparison  
**Base City**: Delhi = 100  
**Coverage**: 41/50 cities (82%)  
**Average Common Products**: 38 per city  
**Status**: ✅ Implemented and Validated  

**Last Updated**: April 14, 2026
