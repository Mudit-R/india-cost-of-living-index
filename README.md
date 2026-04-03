# Cost of Living Index - 50 Indian Cities

A comprehensive data analysis project that calculates Cost of Living Index for 50 Indian cities using real-world data from multiple e-commerce and online sources.

## 🎯 Project Overview

This project processes data from 5 different sources to create a weighted Cost of Living Index that reflects actual household expenditure patterns in urban India. The index helps compare living costs across cities with Delhi as the base (Index = 100).

## 📊 Data Sources

| Category | Source | Weight | Files |
|----------|--------|--------|-------|
| **Housing** | MagicBricks | 40% | 51 files (xlsx/csv) |
| **Groceries** | Blinkit | 25% | 41 files (xlsx) |
| **Transportation** | Uber | 15% | 1 file (xlsx) |
| **Healthcare** | Physician Fees | 10% | 1 file (xlsx) |
| **Fuel** | City Prices | 10% | 1 file (csv) |

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
./run.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run analysis
python main.py
```

### Option 3: Interactive Analysis
```bash
source venv/bin/activate
pip install jupyter
jupyter notebook analysis.ipynb
```

## 📁 Project Structure

```
.
├── main.py                    # Main execution script
├── data_loader.py             # Data loading & preprocessing
├── cost_calculator.py         # Index calculation engine
├── visualizer.py              # Visualization generator
├── config.py                  # Configuration settings
├── analysis.ipynb             # Jupyter notebook
├── test_data.py               # Data verification script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── SETUP.md                   # Detailed setup instructions
├── METHODOLOGY.md             # Calculation methodology
└── EXPECTED_OUTPUTS.md        # Output documentation
```

## 📈 Output Files

After running the analysis:

1. **cost_index_results.csv** - Complete dataset with all indices
2. **visualizations/** folder:
   - `top_bottom_cities.png` - Most expensive vs affordable cities
   - `component_breakdown.png` - Cost breakdown by component
   - `distribution.png` - Statistical distributions
   - `heatmap.png` - Component heatmap for top cities

## 🔍 Key Features

- **Weighted Index**: Reflects real household expenditure patterns
- **Missing Data Handling**: Automatic median imputation
- **City Name Normalization**: Handles variations in city names
- **Multiple Visualizations**: 4 different chart types
- **Comprehensive Output**: CSV export with all metrics
- **Interactive Analysis**: Jupyter notebook included

## 📊 Weightage Justification

Based on typical urban household expenditure in India:
- **Housing (40%)**: Largest fixed expense (rent/EMI)
- **Groceries (25%)**: Daily food consumption
- **Transportation (15%)**: Commute and travel
- **Healthcare (10%)**: Essential medical services
- **Fuel (10%)**: Personal vehicle costs

## 🧪 Testing

Verify your setup before running:
```bash
python test_data.py
```

## 📖 Documentation

- **SETUP.md** - Installation and troubleshooting
- **METHODOLOGY.md** - Detailed calculation methodology
- **EXPECTED_OUTPUTS.md** - Sample outputs and interpretation

## 🎓 Use Cases

- **Individuals**: Compare living costs before relocation
- **Businesses**: Set location-based compensation
- **Researchers**: Urban economics analysis
- **Policy Makers**: Urban planning insights

## ⚙️ Requirements

- Python 3.8+
- pandas
- openpyxl
- numpy
- matplotlib
- seaborn

## 📝 Example Output

```
Most Expensive City: Mumbai (Index = 125.34)
Most Affordable City: Patna (Index = 62.18)
Base City: Delhi (Index = 100.00)
```

## 🔄 Future Enhancements

- Add more expense categories (education, utilities)
- Temporal analysis (track changes over time)
- Quality-of-life metrics integration
- Income vs cost affordability analysis
- Regional clustering

## 📄 License

This project is for educational and research purposes.

## 🤝 Contributing

Feel free to fork, improve, and submit pull requests!
