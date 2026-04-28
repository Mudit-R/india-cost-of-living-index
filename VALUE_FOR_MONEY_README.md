# 🌟 Value-for-Money City Recommender

## What's New?

We've added a powerful new feature that helps you find cities where **quality of life exceeds cost of living** based on YOUR personal preferences!

## The Concept

Instead of just looking at costs, this tool compares:
- **Cost Index** (objective data) vs **Quality of Life Index** (your ratings)
- Calculates a **Value Score** = Quality / Cost
- Recommends cities with the best value for YOUR priorities

## Example

| City | Cost | Your Quality Rating | Value Score | Verdict |
|------|------|---------------------|-------------|---------|
| **Bengaluru** | 114.76 | 150 | **1.31** | 🌟 Excellent value! |
| **Mumbai** | 162.79 | 180 | **1.11** | ✓ Good value despite high cost |
| **Delhi** | 100.00 | 100 | **1.00** | Baseline |
| **Solapur** | 68.20 | 50 | **0.73** | ⚠️ Cheap but lower quality |

## Quick Start

### Option 1: Run the Website

```bash
./run_value_website.sh
```

Or:

```bash
streamlit run website/app_value_for_money.py
```

### Option 2: Use the Template

1. Open `quality_of_life_template.csv`
2. Rate each city (Delhi = 100 baseline)
3. Upload to the website
4. Get personalized recommendations!

## Three Ways to Input Your Ratings

### 1. Upload CSV (Best for detailed analysis)
- Download template
- Edit quality ratings
- Upload and analyze

### 2. Quick Rating Tool (Fast and easy)
- Group cities into tiers
- Assign ratings to each tier
- Get instant results

### 3. Manual Entry (Full control)
- Rate each city individually
- Fine-tune your preferences
- Complete customization

## What Makes a City "Good Value"?

**Value Score ≥ 1.20**: Excellent value - Quality significantly exceeds cost  
**Value Score 1.05-1.19**: Good value - Quality exceeds cost  
**Value Score 0.95-1.04**: Fair value - Quality matches cost  
**Value Score < 0.95**: Poor value - Cost exceeds quality  

## Use Cases

### 🎯 Job Relocation
Compare offers in different cities considering both salary and quality of life.

**Example**: ₹20L in Mumbai vs ₹16L in Pune  
→ Pune might offer better value if quality/cost ratio is higher!

### 🏡 Retirement Planning
Find affordable cities with good healthcare and peaceful environment.

### 🚀 Startup Location
Balance talent availability, infrastructure, and costs.

### 🎓 Student City Selection
Find cities with good education and student life at reasonable costs.

## Rating Guidelines

Consider what matters to YOU:

**Career**: Job opportunities, salary potential, industry presence  
**Infrastructure**: Transport, connectivity, facilities  
**Lifestyle**: Culture, entertainment, dining, shopping  
**Environment**: Air quality, climate, green spaces  
**Social**: Safety, community, diversity  
**Personal**: Family proximity, language, cultural fit  

## Files Included

- `website/app_value_for_money.py` - Main web application
- `quality_of_life_template.csv` - Template for your ratings
- `docs/VALUE_FOR_MONEY_GUIDE.md` - Comprehensive guide
- `run_value_website.sh` - Quick launch script

## Example Workflow

1. **Research**: Learn about cities you're considering
2. **Rate**: Assign quality scores based on your priorities
3. **Analyze**: Run the tool to see value rankings
4. **Compare**: Look at value scores, surplus/deficit
5. **Decide**: Choose cities with best value for YOU

## Key Features

✅ **Personalized**: Based on YOUR quality preferences  
✅ **Data-Driven**: Uses actual cost data from our analysis  
✅ **Flexible**: Multiple input methods  
✅ **Visual**: Clear metrics and rankings  
✅ **Downloadable**: Export results as CSV  
✅ **Comprehensive**: All 50 cities analyzed  

## Technical Details

**Formula**: `Value Score = Quality Index / Cost Index`

**Normalization**: Delhi = 100 for both indices (baseline)

**Ranking**: Cities sorted by Value Score (descending)

**Output**: 
- Value Score (ratio)
- Quality Index (your rating)
- Cost Index (actual data)
- Surplus/Deficit (difference)

## Tips for Best Results

1. **Be Honest**: Rate based on YOUR actual preferences
2. **Be Consistent**: Use same criteria for all cities
3. **Research First**: Learn about cities before rating
4. **Update Regularly**: Revisit as you learn more
5. **Combine Data**: Use alongside cost data, not instead of it

## Comparison with Original Tool

| Feature | Original Tool | Value-for-Money Tool |
|---------|--------------|----------------------|
| Focus | Cost components | Cost vs Quality |
| Input | Component weights | City quality ratings |
| Output | Cost rankings | Value rankings |
| Use Case | Find cheap cities | Find best value cities |
| Personalization | Weight preferences | Quality preferences |

**Use Both!**
- Original tool: Understand costs
- Value tool: Find best value

## Example Scenarios

### Tech Professional
Rate Bengaluru, Hyderabad, Pune high (tech hubs)  
→ Likely to rank high despite higher costs

### Retiree
Rate Mysuru, Coimbatore, Pune high (peaceful, good healthcare)  
→ Tier-2 cities likely to offer best value

### Family with Kids
Rate Chandigarh, Pune, Bengaluru high (schools, safety)  
→ Well-planned cities rank high

## Limitations

- Quality ratings are subjective
- Doesn't account for future changes
- Can't capture everything (family, friends, etc.)
- Relative comparison only

## Support

- **Full Guide**: See `docs/VALUE_FOR_MONEY_GUIDE.md`
- **Template**: Use `quality_of_life_template.csv`
- **Original Tool**: `streamlit run website/app.py`

## Conclusion

This tool helps you make smarter decisions by combining:
- **Objective cost data** (what we calculated)
- **Subjective quality preferences** (what you value)
- **Value analysis** (where you get the most for your money)

The "best" city isn't the cheapest or the highest quality—it's the one that offers the best value for YOUR priorities!

---

**Ready to find your perfect city?**

```bash
./run_value_website.sh
```

🌟 Happy city hunting!
