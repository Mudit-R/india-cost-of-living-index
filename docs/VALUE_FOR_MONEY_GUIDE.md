# Value-for-Money City Recommender Guide

## Overview

The Value-for-Money City Recommender is an advanced feature that helps you find cities where the **quality of life exceeds the cost of living** based on YOUR personal preferences.

## Concept

### The Formula

```
Value Score = Quality of Life Index / Cost of Living Index
```

- **Value Score > 1.0**: Quality exceeds cost (Good value!)
- **Value Score = 1.0**: Quality matches cost (Fair value)
- **Value Score < 1.0**: Cost exceeds quality (Poor value)

### Example

| City | Cost Index | Your Quality Rating | Value Score | Verdict |
|------|------------|---------------------|-------------|---------|
| Mumbai | 162.79 | 180 | 1.11 | Good value despite high cost! |
| Delhi | 100.00 | 100 | 1.00 | Baseline (fair value) |
| Bengaluru | 114.76 | 150 | 1.31 | Excellent value! |
| Solapur | 68.20 | 50 | 0.73 | Cheap but lower quality |

## How to Use

### Step 1: Choose Input Method

You have 3 options to provide your quality of life ratings:

#### Option A: Upload CSV File (Recommended for detailed analysis)

1. Download the template: `quality_of_life_template.csv`
2. Edit the `Quality_Index` column for each city
3. Use Delhi = 100 as your baseline
4. Upload the file to the website

**Template Format:**
```csv
City,Quality_Index,Notes
Delhi,100,Baseline
Mumbai,140,Great job market and culture
Bengaluru,135,Tech hub with good weather
Pune,120,Good balance of cost and quality
...
```

#### Option B: Quick Rating Tool (Fast and easy)

1. Group cities into tiers:
   - **Premium (120-150)**: Cities you consider high quality
   - **Above Average (100-120)**: Better than baseline
   - **Average (80-100)**: Around baseline
   - **Below Average (50-80)**: Lower quality

2. Assign a rating to each tier
3. Select cities for each tier
4. Unrated cities default to 100

#### Option C: Manual Entry (Full control)

Enter a quality rating for each of the 50 cities individually using sliders.

### Step 2: Calculate Rankings

Click "Calculate Value-for-Money Rankings" to see results.

### Step 3: Interpret Results

The tool shows:

- **Value Score**: Quality/Cost ratio (higher is better)
- **Quality Index**: Your rating for the city
- **Cost Index**: Actual cost data (Delhi = 100)
- **Surplus/Deficit**: Quality - Cost (positive = good value)

#### Value Categories

- **Excellent Value (≥1.20)**: Quality significantly exceeds cost
- **Good Value (1.05-1.19)**: Quality exceeds cost
- **Fair Value (0.95-1.04)**: Quality matches cost
- **Poor Value (<0.95)**: Cost exceeds quality

## Rating Guidelines

### What to Consider for Quality of Life

When rating cities, consider factors important to YOU:

**Career & Economy:**
- Job opportunities in your field
- Salary potential
- Business environment
- Industry presence

**Infrastructure:**
- Public transport quality
- Road conditions
- Internet connectivity
- Airport accessibility

**Lifestyle:**
- Cultural activities
- Entertainment options
- Dining scene
- Shopping facilities

**Environment:**
- Air quality
- Green spaces
- Climate
- Cleanliness

**Social:**
- Community vibe
- Safety
- Diversity
- Social opportunities

**Personal Factors:**
- Proximity to family
- Language comfort
- Cultural fit
- Personal history with the city

### Rating Scale

- **150+**: World-class city, exceptional quality
- **120-150**: Premium city, high quality
- **100-120**: Above average, good quality
- **80-100**: Average, acceptable quality
- **50-80**: Below average, limited quality
- **<50**: Poor quality, significant issues

**Remember**: Delhi = 100 is your baseline. Rate other cities relative to Delhi.

## Use Cases

### 1. Job Relocation Decision

**Scenario**: You have job offers in Mumbai (₹20L) and Pune (₹16L)

**Analysis**:
- Mumbai: Cost = 162.79, Quality = 140 → Value = 0.86
- Pune: Cost = 99.61, Quality = 120 → Value = 1.20

**Result**: Pune offers better value! Even with lower salary, the cost-quality ratio is superior.

### 2. Retirement Planning

**Scenario**: Looking for affordable cities with good healthcare and peace

**Strategy**:
- Rate cities high on: Healthcare access, peace, climate
- Rate cities low on: Job market, nightlife (not relevant)
- Find cities with Value Score > 1.1

### 3. Startup Location

**Scenario**: Choosing a city for your startup

**Strategy**:
- Rate cities high on: Talent pool, infrastructure, business environment
- Accept higher costs if quality justifies it
- Look for Value Score > 1.0 with high absolute quality

### 4. Student City Selection

**Scenario**: Choosing where to study

**Strategy**:
- Rate cities high on: Education quality, student life, safety
- Rate cities low on: Luxury amenities (not needed)
- Find affordable cities with good student experience

## Advanced Tips

### 1. Weighted Quality Ratings

Consider creating different quality indices for different life stages:

- **Young Professional**: Weight career opportunities heavily
- **Family**: Weight schools, safety, space heavily
- **Retiree**: Weight healthcare, peace, climate heavily

### 2. Sensitivity Analysis

Try different rating scenarios:
- Optimistic ratings (rate cities generously)
- Pessimistic ratings (rate cities conservatively)
- See which cities consistently rank high

### 3. Component-Specific Analysis

Focus your quality ratings on components that matter:
- If housing is your priority, rate cities based on housing quality
- If food culture matters, rate cities on dining options

### 4. Temporal Considerations

Update your quality ratings periodically:
- Cities change over time
- Your preferences evolve
- New infrastructure gets built

## Interpreting Results

### High Value Score Cities

**What it means**: These cities offer more quality than they cost.

**Action**: Strong candidates for relocation or investment.

**Caution**: Ensure the "quality" factors you rated are actually important to you.

### Low Value Score Cities

**What it means**: These cities cost more than the quality they provide (for you).

**Action**: Avoid unless specific factors override the analysis.

**Caution**: May still be worth it for unique opportunities (e.g., specific job).

### Surplus/Deficit Metric

- **Positive Surplus**: Quality exceeds cost by X points
- **Negative Deficit**: Cost exceeds quality by X points

**Example**: Mumbai with +17.21 surplus means your quality rating (180) exceeds cost (162.79) by 17.21 points.

## Limitations

1. **Subjective Ratings**: Quality ratings are personal and subjective
2. **Static Analysis**: Doesn't account for future changes
3. **Missing Factors**: Can't capture everything (family, friends, etc.)
4. **Relative Scale**: Only compares cities, doesn't give absolute answers

## Best Practices

1. **Be Honest**: Rate cities based on YOUR actual preferences, not what you think you should prefer
2. **Be Consistent**: Use the same criteria for all cities
3. **Research First**: Learn about cities before rating them
4. **Update Regularly**: Revisit ratings as you learn more
5. **Combine with Data**: Use this alongside the cost data, not instead of it
6. **Visit if Possible**: Nothing beats firsthand experience

## Example Scenarios

### Scenario 1: Tech Professional

**Quality Priorities**: Job market, tech ecosystem, infrastructure, lifestyle

**Sample Ratings**:
- Bengaluru: 150 (Tech capital)
- Hyderabad: 140 (Growing tech hub)
- Pune: 130 (Good tech presence)
- Delhi: 100 (Baseline)
- Tier-3 cities: 60-80 (Limited opportunities)

**Expected Results**: Bengaluru and Hyderabad likely to rank high despite higher costs.

### Scenario 2: Retiree

**Quality Priorities**: Healthcare, peace, climate, cost of living

**Sample Ratings**:
- Mysuru: 130 (Peaceful, good healthcare)
- Coimbatore: 125 (Pleasant climate)
- Pune: 120 (Good facilities)
- Delhi: 100 (Baseline)
- Mumbai: 90 (Too hectic)

**Expected Results**: Tier-2 cities with good healthcare likely to rank high.

### Scenario 3: Family with Kids

**Quality Priorities**: Schools, safety, space, community

**Sample Ratings**:
- Chandigarh: 140 (Planned city, good schools)
- Pune: 135 (Family-friendly)
- Bengaluru: 130 (Good schools)
- Delhi: 100 (Baseline)
- Industrial cities: 70-80 (Limited family amenities)

**Expected Results**: Well-planned cities with good schools rank high.

## Technical Details

### Calculation Method

```python
# For each city:
value_score = quality_index / cost_index

# Normalize so Delhi (100/100) = 1.00
# This makes interpretation intuitive
```

### Ranking Algorithm

Cities are ranked by Value Score in descending order:
1. Highest value score = Best value
2. Lowest value score = Worst value

### Data Sources

- **Cost Index**: Calculated from actual price data (8 components)
- **Quality Index**: Your subjective ratings
- **Value Score**: Derived from the ratio

## FAQ

**Q: What if I don't know a city well enough to rate it?**  
A: Leave it at 100 (default). It will be treated as baseline quality.

**Q: Can I rate a city higher than 200?**  
A: The tool caps at 200, but you can edit the CSV for higher values if needed.

**Q: Should I rate based on current state or future potential?**  
A: Rate based on current state unless you have specific knowledge of upcoming changes.

**Q: What if two cities have the same value score?**  
A: They're equally good value. Choose based on other factors (personal preference, specific opportunities).

**Q: Can I use this for international comparisons?**  
A: No, this tool is designed for Indian cities only. Cost data is India-specific.

**Q: How often should I update my ratings?**  
A: Annually, or when major life changes occur (new job, family, etc.).

## Conclusion

The Value-for-Money tool helps you make data-driven decisions by combining objective cost data with your subjective quality preferences. Use it as one input in your decision-making process, alongside other factors like personal circumstances, opportunities, and gut feeling.

Remember: The "best" city is the one that's best for YOU, not the one with the highest score!

---

**Need Help?** Check the main documentation or run the tool and use the built-in help sections.
