# City Recommender Website Guide

## Overview

The City Recommender is a Streamlit web application that helps you find cities matching your specific cost priorities across 50 Indian cities.

## How It Works

### Priority-Based Matching

Instead of asking "how important is housing to you?", the recommender asks **what kind of costs you want**:

- **Must be cheap**: You want LOW costs in this category (heavily penalized if expensive)
- **Don't care**: This category doesn't affect your decision (ignored in scoring)
- **Can be expensive**: You're willing to pay more for quality (lightly penalized if very cheap)

### Scoring Logic

The system calculates a "match score" for each city:
- Lower score = Better match to your priorities
- Cities are ranked by how well they match what you want

**For "Must be cheap" categories:**
- Cities with low index values get low penalty (good match)
- Cities with high index values get high penalty (poor match)
- Weight: 3.0x

**For "Can be expensive" categories:**
- Cities with high index values get small penalty
- Cities with very low index values get small penalty (might indicate lower quality)
- Weight: 0.5x

**For "Don't care" categories:**
- No penalty applied (ignored in scoring)

## Running the Website

### Prerequisites

1. Ensure you have generated the cost index data:
```bash
cd src
python main.py
```

This creates `outputs/reports/cost_index_results.csv`

2. Install Streamlit (if not already installed):
```bash
pip install streamlit
```

### Launch the Website

From the project root directory:

```bash
streamlit run website/app.py
```

Or from the website directory:

```bash
cd website
streamlit run app.py
```

The website will open in your browser at `http://localhost:8501`

## Using the Website

### Step 1: Set Your Priorities

For each of the 8 cost categories, select your priority:

**Example Scenarios:**

**Scenario 1: Budget Student**
- Housing: Must be cheap
- Grocery: Must be cheap
- Transport: Must be cheap
- Healthcare: Don't care
- Education: Can be expensive (want quality tutors)
- Electricity: Must be cheap
- Restaurant: Don't care
- Movies: Don't care

**Scenario 2: Working Professional**
- Housing: Can be expensive (want good location)
- Grocery: Don't care
- Transport: Must be cheap (daily commute)
- Healthcare: Can be expensive (want quality)
- Education: Don't care
- Electricity: Don't care
- Restaurant: Can be expensive (lifestyle)
- Movies: Don't care

**Scenario 3: Family with Kids**
- Housing: Must be cheap (need space)
- Grocery: Must be cheap (family expenses)
- Transport: Must be cheap
- Healthcare: Can be expensive (family health)
- Education: Can be expensive (kids' education)
- Electricity: Must be cheap
- Restaurant: Don't care
- Movies: Don't care

### Step 2: Choose Number of Results

Use the slider to select how many city recommendations you want (3-20).

### Step 3: Get Recommendations

Click "🔍 Find My Cities" to see your personalized recommendations.

## Understanding the Results

### City Cards

Each recommended city shows:

1. **Rank**: Position in the ranking (1 = best match)
2. **City Name**: The recommended city
3. **Explanation**: Why this city matches your priorities
   - Shows index values for categories you marked as "Must be cheap"
   - Shows index values for categories you marked as "Can be expensive"
4. **Overall Index**: The city's overall cost of living (Delhi = 100)
5. **Match Score**: How well it matches your priorities (lower = better)

### Cost Levels

Index values are categorized as:
- **Very Affordable**: < 70
- **Affordable**: 70-90
- **Moderate**: 90-110
- **Expensive**: 110-130
- **Very Expensive**: > 130

### Detailed Breakdown

Click "View all cost indices" under each city to see the index value for all 8 categories.

### All Cities View

Expand "View All 50 Cities" to see the complete ranking of all cities based on your priorities.

## Example Use Cases

### Use Case 1: "I want cheap housing, everything else doesn't matter"

**Priorities:**
- Housing: Must be cheap
- All others: Don't care

**Expected Results:**
Cities with the lowest housing index will rank highest, regardless of other costs.

Top cities likely include: Malappuram, Tiruchirappalli, Asansol

### Use Case 2: "I want cheap housing and groceries, but expensive education is OK"

**Priorities:**
- Housing: Must be cheap
- Grocery: Must be cheap
- Education: Can be expensive
- All others: Don't care

**Expected Results:**
Cities with low housing and grocery costs, where education costs can be high.

### Use Case 3: "I want everything cheap"

**Priorities:**
- All categories: Must be cheap

**Expected Results:**
Cities with the lowest overall cost of living.

Top cities likely include: Solapur, Malappuram, Ludhiana

## Technical Details

### Data Source

The website reads from: `outputs/reports/cost_index_results.csv`

This file contains:
- 50 Indian cities
- 8 cost category indices
- Overall cost of living index
- All indices are relative to Delhi (Delhi = 100)

### Categories and Weights

The original cost index uses these weights:
- Housing: 30.30%
- Grocery: 36.36%
- Transport: 10.91%
- Healthcare: 6.42%
- Education: 6.06%
- Restaurant: 4.85%
- Electricity: 3.03%
- Movies: 2.07%

**Note:** The recommender does NOT use these weights. Instead, it uses your priority selections to find matching cities.

### File Structure

```
website/
├── app.py           # Streamlit UI
└── recommender.py   # Recommendation logic
```

## Troubleshooting

### Error: "Data file not found"

**Solution:** Run the data generation script first:
```bash
cd src
python main.py
```

### Error: "Column not found in data"

**Solution:** The data file format may have changed. Regenerate it:
```bash
cd src
python main.py
```

### Website won't start

**Solution:** Check that Streamlit is installed:
```bash
pip install streamlit
```

### Results don't make sense

**Solution:** 
1. Check your priority selections - make sure they reflect what you want
2. Remember: "Must be cheap" heavily penalizes expensive cities
3. "Don't care" completely ignores that category
4. Try different combinations to see how results change

## Tips for Best Results

1. **Be selective with "Must be cheap"**: Only mark categories that truly matter to you. Marking everything as "Must be cheap" will just give you the cheapest cities overall.

2. **Use "Don't care" liberally**: If a category doesn't affect your decision, mark it as "Don't care" to focus on what matters.

3. **"Can be expensive" is for quality**: Use this when you're willing to pay more for better quality in that category.

4. **Compare multiple scenarios**: Try different priority combinations to explore trade-offs.

5. **Check the detailed breakdown**: Expand the city details to see all cost indices and understand the full picture.

## Next Steps

After finding cities that match your priorities:

1. Review the detailed cost breakdown for each city
2. Research other factors (job market, climate, culture, etc.)
3. Visit the cities if possible
4. Make an informed decision based on your complete needs

## Support

For issues or questions:
1. Check that data is up to date: `cd src && python main.py`
2. Verify Streamlit is installed: `pip install streamlit`
3. Check the console for error messages
4. Review the data file: `outputs/reports/cost_index_results.csv`
