# Education Cost Integration

## Overview
Successfully integrated tutor/education fees data into the Cost of Living Index with a **5% weightage** for education costs.

## Data Source
- **File**: `TutorData_Filtered.xlsx`
- **Records**: 62,848 tutor listings
- **Cities Covered**: 50 cities
- **Columns**: Tutor ID, City, Location, Fee

## Data Processing

### Fee Extraction
The tutor fees are provided in ranges (e.g., "₹300–1,000/hour"). The processing:
1. Extracts numeric values from fee ranges
2. Calculates the average of min and max fees
3. Groups by city
4. Removes outliers using IQR method (1.5 × IQR)
5. Uses median for robustness against outliers

### Example Fee Ranges
- Agra: ₹200–1,000/hour
- Mumbai: ₹300–1,500/hour
- Delhi: ₹400–1,200/hour
- Smaller cities: ₹150–800/hour

## Updated Weightage Distribution

### Raw Weights (Before Normalization)
```
Housing:        25.0%
Grocery:        30.0%
Transport:       9.0%
Healthcare:      5.3%
Electricity:     2.5%
Restaurant:      4.0%
Movies:          1.71%
Education:       5.0%  ← NEW
─────────────────────
Total:          82.51%
```

### Normalized Weights (After Re-normalization to 100%)
```
Housing:        30.30%
Grocery:        36.36%
Transport:      10.91%
Healthcare:      6.42%
Electricity:     3.03%
Restaurant:      4.85%
Movies:          2.07%
Education:       6.06%  ← NEW
─────────────────────
Total:         100.00%
```

## Sample Education Index Values

| City | Median Tutor Fee (₹/hour) | Education Index (Delhi=100) |
|------|---------------------------|----------------------------|
| Delhi | 500 | 100.0 |
| Mumbai | 500 | 100.0 |
| Bengaluru | 500 | 100.0 |
| Hyderabad | 500 | 100.0 |
| Kolkata | 600 | 120.0 |
| Chennai | 400 | 80.0 |
| Kozhikode | 300 | 60.0 |
| Pune | 500 | 100.0 |
| Ahmedabad | 500 | 100.0 |
| Jaipur | 500 | 100.0 |

## Code Changes

### 1. data_loader.py
Added new method `load_tutor_data()`:
- Reads TutorData_Filtered.xlsx
- Extracts fee ranges using regex
- Calculates median fees per city
- Applies IQR outlier removal
- Returns DataFrame with City and tutor_fee columns

### 2. cost_calculator.py
Updated to include education:
- Added 'education': 0.05 to WEIGHTS dictionary
- Added tutor_df parameter to merge_all_data()
- Added education_index calculation
- Included education in active_weights normalization
- Added education component to cost_of_living_index formula

### 3. main.py
Updated workflow:
- Added tutor_df = loader.load_tutor_data()
- Passed tutor_df to calculator.merge_all_data()
- Added "Education" to weightage display

## Impact on Cost of Living Index

The addition of education costs (5% raw weight, 6.06% normalized) provides a more comprehensive view of living costs, especially important for:
- Families with school-age children
- Students seeking tutoring/coaching
- Cities with varying education costs

### Key Insights
1. **Metro cities** (Mumbai, Delhi, Bengaluru) show higher tutor fees (₹500/hour median)
2. **Tier-2 cities** show moderate fees (₹400-500/hour)
3. **Smaller cities** show lower fees (₹300-400/hour)
4. Education costs add **6.06%** to the overall cost calculation

## Verification

Run the analysis:
```bash
python3 main.py
```

Check results:
```bash
# View education data in results
python3 -c "import pandas as pd; df = pd.read_csv('cost_index_results.csv'); print(df[['City', 'tutor_fee', 'education_index']].head(20))"
```

## Output Files

All output files now include education data:
- **cost_index_results.csv**: Contains tutor_fee and education_index columns
- **Visualizations**: Updated to reflect new weightage distribution
- **Console output**: Shows education in weightage breakdown

## Next Steps

Consider adding:
1. School fees data (primary/secondary education)
2. College/university tuition fees
3. Coaching center costs
4. Online education platform costs

This would provide an even more comprehensive education cost component.

---

**Status**: ✅ Successfully Integrated
**Weightage**: 5% (raw) → 6.06% (normalized)
**Cities Covered**: 50/50
**Data Quality**: High (62,848 records with outlier removal)
