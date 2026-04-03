# Quick Start Guide

## 🚀 Get Results in 3 Steps

### Step 1: Setup (One-time)
```bash
# Clone or download the project
cd "BMP Data Modelling"

# Run the automated setup script
./run.sh
```

That's it! The script will:
- Create a virtual environment
- Install all dependencies
- Run the complete analysis
- Generate all visualizations

### Step 2: View Results

After the script completes, check:

1. **Console Output** - Summary statistics and top/bottom cities
2. **cost_index_results.csv** - Complete data (open in Excel/Google Sheets)
3. **visualizations/** folder - 4 PNG charts

### Step 3: Interpret

Open the visualizations:
- `top_bottom_cities.png` - Quick comparison of extremes
- `component_breakdown.png` - See what drives costs in each city
- `distribution.png` - Statistical overview
- `heatmap.png` - Detailed component comparison

## 📊 Understanding the Index

- **Index = 100**: Same cost as Delhi (base city)
- **Index > 100**: More expensive than Delhi
- **Index < 100**: More affordable than Delhi

### Examples
- Mumbai (Index 125) = 25% more expensive than Delhi
- Patna (Index 75) = 25% more affordable than Delhi

## 🔧 Customization

### Change Base City
Edit `config.py`:
```python
BASE_CITY = 'Mumbai'  # Change from 'Delhi'
```

### Adjust Weights
Edit `config.py`:
```python
COST_WEIGHTS = {
    'housing': 0.35,      # Reduce from 0.40
    'grocery': 0.30,      # Increase from 0.25
    'transportation': 0.15,
    'healthcare': 0.10,
    'fuel': 0.10
}
```

Then run again:
```bash
source venv/bin/activate
python main.py
```

## 🐛 Troubleshooting

### Problem: "command not found: ./run.sh"
**Solution**: Make it executable
```bash
chmod +x run.sh
./run.sh
```

### Problem: "externally-managed-environment"
**Solution**: The script handles this automatically. If manual install needed:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Problem: "No module named 'pandas'"
**Solution**: Activate virtual environment
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: Missing data files
**Solution**: Ensure these exist in the project folder:
- `Fuel Prices by city (1).csv`
- `City Wise Uber Price Per km .xlsx`
- `General Physician Fee City wise.xlsx`
- `blinkit_citywise/` folder
- `Magic Bricks data/` folder

Run verification:
```bash
python test_data.py
```

## 📱 Interactive Analysis

For custom queries and exploration:

```bash
source venv/bin/activate
pip install jupyter
jupyter notebook analysis.ipynb
```

This opens an interactive notebook where you can:
- Filter cities
- Create custom visualizations
- Perform statistical analysis
- Export custom reports

## 💡 Tips

1. **First Time**: Run `python test_data.py` to verify everything is set up correctly

2. **Quick Re-run**: After first setup, just run:
   ```bash
   source venv/bin/activate
   python main.py
   ```

3. **Update Data**: Replace data files and re-run. The script handles everything automatically.

4. **Export for Presentation**: All visualizations are high-resolution (300 DPI) PNG files ready for presentations.

5. **Share Results**: The CSV file can be opened in Excel, Google Sheets, or any data tool.

## 📚 Learn More

- **METHODOLOGY.md** - How the index is calculated
- **EXPECTED_OUTPUTS.md** - Detailed output explanation
- **PROJECT_SUMMARY.md** - Complete project overview
- **SETUP.md** - Advanced setup options

## ⏱️ Time Estimates

- **First-time setup**: 2-3 minutes
- **Analysis execution**: 30-60 seconds
- **Subsequent runs**: 30 seconds

## 🎯 Common Use Cases

### Use Case 1: Compare Two Cities
```python
# In Python or Jupyter
import pandas as pd
df = pd.read_csv('cost_index_results.csv')
cities = df[df['City'].isin(['Mumbai', 'Pune'])]
print(cities[['City', 'cost_of_living_index', 'housing_index']])
```

### Use Case 2: Find Affordable Cities
```python
df = pd.read_csv('cost_index_results.csv')
affordable = df[df['cost_of_living_index'] < 80]
print(affordable[['City', 'cost_of_living_index']].sort_values('cost_of_living_index'))
```

### Use Case 3: Analyze Housing Costs
```python
df = pd.read_csv('cost_index_results.csv')
high_housing = df.nlargest(10, 'housing_index')
print(high_housing[['City', 'housing_index', 'housing_price']])
```

## ✅ Success Checklist

- [ ] Project files downloaded
- [ ] `./run.sh` executed successfully
- [ ] Console shows summary statistics
- [ ] `cost_index_results.csv` created
- [ ] `visualizations/` folder contains 4 PNG files
- [ ] Opened and reviewed at least one visualization

## 🎓 Next Steps

1. Review the visualizations
2. Open the CSV in your preferred tool
3. Read METHODOLOGY.md to understand the calculations
4. Customize weights if needed for your use case
5. Share insights with your team!

---

**Need Help?** Check the troubleshooting section above or review SETUP.md for detailed instructions.
