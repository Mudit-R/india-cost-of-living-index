# Cost of Living Index - 50 Indian Cities

A comprehensive data analysis project that calculates and visualizes the cost of living across 50 major Indian cities using real-world data from multiple sources.

## 🎯 Quick Start

```bash
# Run the complete analysis
./run.sh

# Or manually:
cd src
python3 main.py
```

## 📊 Results

- **CSV Report**: `outputs/reports/cost_index_results.csv`
- **Visualizations**: `outputs/visualizations/`
- **Documentation**: `docs/`

## 🏗️ Project Structure

```
├── data/                    # All data files
│   ├── raw/                # Original data sources
│   │   ├── housing/        # MagicBricks data (50 cities)
│   │   ├── grocery/        # Blinkit data (41 cities)
│   │   ├── transport/      # Uber & fuel prices
│   │   ├── healthcare/     # Doctor consultation fees
│   │   ├── education/      # Tutor hourly rates (60K+ listings)
│   │   ├── utilities/      # Electricity rates
│   │   └── entertainment/  # Movies & restaurants
│   └── processed/          # Generated data
│
├── src/                     # Source code
│   ├── main.py             # Main execution script
│   ├── data_loader.py      # Data loading & preprocessing
│   ├── cost_calculator.py  # Index calculations
│   ├── visualizer.py       # Chart generation
│   ├── ml_classification.py # ML models
│   └── city-recommendation/ # Recommendation system
│
├── outputs/                 # Generated outputs
│   ├── visualizations/     # All charts & graphs
│   └── reports/            # CSV results
│
├── docs/                    # Documentation
│   ├── README.md           # Detailed project info
│   ├── METHODOLOGY.md      # Calculation methodology
│   ├── SETUP.md            # Installation guide
│   └── ... (more docs)
│
└── tests/                   # Test files

```

## 📈 Key Features

- ✅ **50 Indian cities** analyzed
- ✅ **8 cost components** tracked (Housing, Grocery, Transport, Healthcare, Education, Restaurant, Electricity, Movies)
- ✅ **94+ data files** processed
- ✅ **Weighted index** calculation (Delhi = 100)
- ✅ **Multiple visualizations** generated
- ✅ **ML classification** models included
- ✅ **City recommendation** system

## 🎨 Component Weights

The cost of living index uses the following normalized weights:

| Component | Weight |
|-----------|--------|
| Grocery | 36.36% |
| Housing | 30.30% |
| Transport | 10.91% |
| Healthcare | 6.42% |
| Education | 6.06% |
| Restaurant | 4.85% |
| Electricity | 3.03% |
| Movies | 2.07% |

## 📊 Sample Results

**Top 5 Most Expensive Cities:**
1. Mumbai - 167.85
2. Bengaluru - 109.64
3. Kozhikode - 101.16
4. Hyderabad - 100.18
5. Delhi - 100.00 (Base)

**Top 5 Most Affordable Cities:**
1. Malappuram - 61.83
2. Sangli - 65.86
3. Jamnagar - 67.56
4. Surat - 68.01
5. Asansol - 68.30

## 🔧 Requirements

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

## 📚 Documentation

See the `docs/` folder for detailed documentation:
- **SETUP.md** - Installation and setup instructions
- **METHODOLOGY.md** - Calculation methodology and formulas
- **EXPECTED_OUTPUTS.md** - Output interpretation guide
- **EDUCATION_INTEGRATION.md** - Education component details
- **ML_APPLICATIONS.md** - Machine learning applications

## 🗂️ Data Sources

- **Housing**: MagicBricks property listings (51 files, 50 cities)
- **Grocery**: Blinkit online grocery prices (41 files, 41 cities)
- **Transport**: Uber per-km pricing + fuel prices (50 cities)
- **Healthcare**: General physician consultation fees (50 cities)
- **Education**: Tutor hourly rates (60,233 listings, 50 cities)
- **Utilities**: Electricity rates (50 cities)
- **Entertainment**: Movie tickets + restaurant prices (50 cities)

## 🎯 Use Cases

- **Individuals**: Make informed relocation decisions
- **Companies**: Set location-based salaries
- **Researchers**: Study urban economics
- **Policy Makers**: Identify affordability gaps

## 📝 License

This project is for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Please see the documentation for guidelines.

## 📧 Contact

For questions or issues, refer to the documentation in the `docs/` folder.

---

**Last Updated**: April 2026  
**Status**: ✅ Complete and Ready to Use
