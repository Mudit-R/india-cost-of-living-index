# Quick Reference - Cost of Living Project

## 🚀 Quick Start

### Run Complete Analysis
```bash
./run.sh
```

### Launch Website
```bash
./launch_website.sh
```

### Run Tests
```bash
python test_website.py
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `src/main.py` | Generate cost index data |
| `website/app.py` | Web interface |
| `outputs/reports/cost_index_results.csv` | Results data |
| `README.md` | Main documentation |

## 🎯 Common Tasks

### Generate New Data
```bash
cd src
python main.py
```

### View Results
```bash
# CSV file
cat outputs/reports/cost_index_results.csv

# Visualizations
open outputs/visualizations/
```

### Update Website
```bash
# After data changes
streamlit run website/app.py
```

## 📊 Project Stats

- **Cities**: 50 Indian cities
- **Categories**: 8 (Housing, Grocery, Transport, Healthcare, Education, Electricity, Restaurant, Movies)
- **Data Files**: 94+ files processed
- **Base City**: Delhi = 100

## 🔧 Installation

```bash
# Install all dependencies
pip install -r requirements.txt

# Or individually
pip install pandas numpy matplotlib seaborn openpyxl streamlit
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| `README.md` | Project overview |
| `docs/METHODOLOGY.md` | Calculation methods |
| `docs/DATA_PROCESSING_REPORT.md` | Data sources & processing |
| `docs/WEBSITE_GUIDE.md` | Website technical guide |
| `website/README.md` | Website usage |

## 🎨 Component Weights

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

## 🏆 Top Cities

### Most Expensive
1. Mumbai - 162.79
2. Bengaluru - 114.76
3. Kozhikode - 107.66

### Most Affordable
1. Solapur - 68.20
2. Malappuram - 69.54
3. Tiruchirappalli - 71.41

## 🌐 Website Features

- Interactive sliders for 8 categories
- Personalized recommendations
- Top 3 city matches
- View all 50 cities ranked
- Detailed cost breakdowns

## 🧪 Testing

```bash
# Test website components
python test_website.py

# Expected: 5/5 tests pass
```

## 🆘 Troubleshooting

### Data file not found
```bash
cd src && python main.py
```

### Streamlit not installed
```bash
pip install streamlit
```

### Port already in use
```bash
streamlit run website/app.py --server.port 8502
```

## 📞 Quick Links

- **Project Root**: `/Users/mudit/Desktop/BMP Data Modelling/`
- **Data**: `data/raw/`
- **Results**: `outputs/`
- **Website**: `website/`
- **Docs**: `docs/`

## ⚡ One-Liners

```bash
# Full pipeline
./run.sh && ./launch_website.sh

# Quick test
python test_website.py && streamlit run website/app.py

# Regenerate everything
cd src && python main.py && cd .. && streamlit run website/app.py
```

---

**Last Updated**: April 15, 2026  
**Status**: ✅ Production Ready
