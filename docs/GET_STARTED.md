# 🚀 GET STARTED - Your First Run

## ✅ Pre-Flight Checklist

Before running the analysis, verify you have:

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] All data files in place (see below)
- [ ] Terminal/command line access
- [ ] 5 minutes of time

## 📂 Required Data Files

Ensure these files/folders exist in your project directory:

```
BMP Data Modelling/
├── Fuel Prices by city (1).csv          ✓ Check
├── City Wise Uber Price Per km .xlsx    ✓ Check
├── General Physician Fee City wise.xlsx ✓ Check
├── blinkit_citywise/                    ✓ Check (41 files)
└── Magic Bricks data/                   ✓ Check (51 files)
```

## 🎯 Three Ways to Run

### Method 1: Automated (Easiest) ⭐
```bash
./run.sh
```
**Time**: 2-3 minutes (first run), 30 seconds (subsequent runs)

### Method 2: Manual
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
**Time**: 3-4 minutes

### Method 3: Test First (Recommended for first-timers)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python test_data.py    # Verify everything is OK
python main.py         # Run the analysis
```
**Time**: 4-5 minutes

## 📊 What You'll Get

After successful execution:

### 1. Console Output
```
================================================================================
COST OF LIVING INDEX - 50 INDIAN CITIES
================================================================================

[1/5] Loading data from all sources...
  ✓ Loaded fuel prices for 45 cities
  ✓ Loaded Uber prices for 42 cities
  ...

Most Expensive City: Mumbai (Index = 125.34)
Most Affordable City: Patna (Index = 62.18)
```

### 2. CSV File
- **cost_index_results.csv** - Open in Excel/Google Sheets
- Contains all cities with complete metrics

### 3. Visualizations
- **visualizations/top_bottom_cities.png** - Quick comparison
- **visualizations/component_breakdown.png** - Detailed breakdown
- **visualizations/distribution.png** - Statistical view
- **visualizations/heatmap.png** - Component heatmap

## 🎓 First-Time User Path

Follow this sequence for the best experience:

1. **Verify Setup**
   ```bash
   python test_data.py
   ```
   Should show all green checkmarks ✓

2. **Run Analysis**
   ```bash
   ./run.sh
   ```
   Wait for completion (~2 minutes)

3. **Check Console Output**
   - Read the summary statistics
   - Note the top 10 expensive cities
   - Note the top 10 affordable cities

4. **Open Visualizations**
   - Navigate to `visualizations/` folder
   - Open `top_bottom_cities.png` first
   - Review other charts

5. **Explore CSV**
   - Open `cost_index_results.csv` in Excel
   - Sort by `cost_of_living_index`
   - Filter by your cities of interest

6. **Read Documentation**
   - **QUICK_START_GUIDE.md** - Detailed instructions
   - **METHODOLOGY.md** - Understand the calculations
   - **EXPECTED_OUTPUTS.md** - Interpret results

## 🔍 Quick Verification

After running, verify success:

```bash
# Check if output files exist
ls -lh cost_index_results.csv
ls -lh visualizations/*.png

# Quick preview of results
head -20 cost_index_results.csv
```

## 💡 Pro Tips

1. **First run takes longer** - Virtual environment setup and package installation
2. **Subsequent runs are fast** - Just activate venv and run
3. **Keep venv activated** - For multiple runs or customization
4. **Check visualizations first** - Easier to understand than raw CSV
5. **Use Jupyter for exploration** - More interactive than CSV

## 🐛 Common Issues & Fixes

### Issue: Permission denied
```bash
chmod +x run.sh
./run.sh
```

### Issue: Python not found
```bash
# Try python instead of python3
python --version
# Update run.sh if needed
```

### Issue: Missing packages
```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Data files not found
```bash
# Verify you're in the correct directory
pwd
# Should show: .../BMP Data Modelling

# List data files
ls -lh *.csv *.xlsx
ls -lh blinkit_citywise/ | head
ls -lh "Magic Bricks data/" | head
```

## 📞 Need Help?

1. **Run test script**: `python test_data.py`
2. **Check SETUP.md**: Detailed troubleshooting
3. **Review error messages**: Usually self-explanatory
4. **Verify data files**: Ensure all files are present

## 🎉 Success Indicators

You'll know it worked when you see:

✅ Console shows "Analysis complete!"
✅ `cost_index_results.csv` file exists
✅ `visualizations/` folder has 4 PNG files
✅ No error messages in console
✅ File sizes look reasonable (CSV ~50KB, PNGs ~200KB each)

## ⏭️ Next Steps

After your first successful run:

1. **Explore Results**
   - Open visualizations
   - Review CSV in Excel
   - Read key findings

2. **Customize** (Optional)
   - Edit `config.py` to change weights
   - Change base city
   - Re-run analysis

3. **Interactive Analysis** (Advanced)
   ```bash
   source venv/bin/activate
   pip install jupyter
   jupyter notebook analysis.ipynb
   ```

4. **Share Results**
   - Export visualizations for presentations
   - Share CSV with team
   - Discuss insights

## 📚 Learning Path

- **Beginner**: Run → View visualizations → Read summary
- **Intermediate**: Run → Explore CSV → Customize weights → Re-run
- **Advanced**: Jupyter notebook → Custom analysis → Modify code

---

**Ready?** Open your terminal and run: `./run.sh`

**Questions?** Check QUICK_START_GUIDE.md for detailed help.

**Time to results**: 2-3 minutes ⏱️
