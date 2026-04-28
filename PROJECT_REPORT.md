# Project Report: India Cost of Living Index
### Comprehensive Analysis of 50 Indian Cities
**Date:** April 2026 | **Status:** Complete

---

## 1. Executive Summary

This project delivers a **data-driven Cost of Living Index** for 50 major Indian cities, built from over 94 raw data files sourced from real-world platforms (MagicBricks, Blinkit, Uber, Swiggy, and more). The index uses an expenditure-weighted formula — Delhi anchored at 100 — to compare the true cost of everyday life across India.

> [!IMPORTANT]
> **Key Finding:** Mumbai is 62.8% more expensive than Delhi. The cheapest city (Malappuram) costs only 69.5 on the index — nearly 43% less than Mumbai.

**Top 5 Most Expensive Cities:**
| Rank | City | Index |
|------|------|-------|
| 1 | Mumbai | 162.79 |
| 2 | Bengaluru | 114.76 |
| 3 | Kozhikode | 107.66 |
| 4 | Hyderabad | 107.09 |
| 5 | Patna | 100.72 |

**Top 5 Most Affordable Cities:**
| Rank | City | Index |
|------|------|-------|
| 1 | Malappuram | 69.54 |
| 2 | Solapur | 68.20 |
| 3 | Tiruchirappalli | 71.41 |
| 4 | Ludhiana | 72.50 |
| 5 | Jamnagar | 72.77 |

---

## 2. Data Sources & Files Used

### 2.1 Housing Data — MagicBricks
**Location:** `data/raw/Magic Bricks data/` 
**Format:** CSV | **Files:** 50 (one per city) 

Property listing files downloaded from MagicBricks covering every major Indian city. Each file contains real estate listings with columns: `city_name`, `floors`, `bathrooms`, `carpet_area`, `price`, `price_per_sq_ft`.

**Example files:** `Delhi_magicbricks.csv`, `Mumbai_magicbricks.csv`, `Bengaluru_magicbricks.csv`

| City Sample | Price/sq ft (₹) |
|---|---|
| Delhi | ₹10,231 |
| Mumbai | ₹23,619 |
| Malappuram | ₹1,512 |

> **Coverage:** 50/50 cities (100%) | **Typical listings per city:** 100–500

---

### 2.2 Grocery Data — Blinkit
**Location:** `data/raw/grocery/blinkit_citywise/` 
**Format:** Excel (.xlsx) | **Files:** 41 

City-specific product price lists from Blinkit (online grocery delivery). Each file has two columns: product name and price (₹). Covers staples like rice, wheat, vegetables, dairy, and packaged goods.

**Example files:** `blinkit_delhi.xlsx`, `blinkit_mumbai.xlsx`, `blinkit_bangalore.xlsx`

| City | Median Grocery Price (₹) |
|---|---|
| Delhi | ₹42.00 |
| Mumbai | ₹49.50 |
| Bengaluru | ₹36.00 |

> **Coverage:** 41/50 cities (82%) — 9 missing cities filled with ₹42 median 
> **Products per city:** 50–200 items

---

### 2.3 Transport Data
**Location:** `data/raw/transport/` 
**Files:**
- `City Wise Uber Price Per km .xlsx` — Uber per-km pricing for 42 cities
- `Fuel Prices by city (1).csv` — Petrol, Diesel, CNG, LPG prices for 50 cities

Uber price is the primary transport metric used in the index. Fuel data is loaded but not directly weighted in the index.

| City | Uber ₹/km | Avg Fuel ₹/L |
|---|---|---|
| Delhi | ₹20.00 | ₹91.26 |
| Mumbai | ₹44.07 | ₹96.75 |
| Bengaluru | ₹43.26 | ₹96.94 |

> **Uber Coverage:** 42/50 cities — 8 missing filled with ₹18.91 median

---

### 2.4 Healthcare Data
**Location:** `data/raw/healthcare/General Physician Fee City wise.xlsx` 
**Format:** Excel | **Files:** 1 (wide format, multiple fee samples per row) 

Contains general physician consultation fees for all 50 cities. The wide format stores multiple doctor fee samples per city across columns.

| City | Median Doctor Fee (₹) |
|---|---|
| Delhi | ₹1,000 |
| Mumbai | ₹1,350 |
| Bengaluru | ₹750 |
| Salem | ₹150 |

> **Coverage:** 50/50 cities (100%) | **Samples per city:** 10–30

---

### 2.5 Education Data — Tutor Marketplace
**Location:** `data/raw/education/TutorData_Filtered.xlsx` 
**Format:** Excel | **Total Records:** 60,256 tutor listings 

A large dataset of online tutor listings with city, location, and fee range. Only per-hour fees are used for comparability. Fee ranges like "₹300–1,000/hour" are midpoint-averaged.

After filtering: **46,965 per-hour records** across all 50 cities.

| City | Avg Tutor Fee/hr (₹) |
|---|---|
| Delhi | ₹539 |
| Mumbai | ₹614 |
| Malappuram | ₹253 |

> **Coverage:** 50/50 cities | **Average listings per city:** ~940

---

### 2.6 Utilities Data — Electricity
**Location:** `data/raw/utilities/` 
**Files:**
- `Electricity Price.xlsx` (primary)
- `Electricity Price (1).xlsx` (backup)

Effective electricity tariff rates (₹/unit) sourced from state electricity boards.

| City | Rate (₹/unit) |
|---|---|
| Delhi | ₹4.00 |
| Mumbai | ₹8.50 |
| Visakhapatnam | ₹3.00 |

> **Coverage:** 50/50 cities (100%) | **Range:** ₹3.00–₹8.50/unit

---

### 2.7 Entertainment Data
**Location:** `data/raw/entertainment/` 
**Files:**
- `Movieticketprices.xlsx` — Ticket prices from 5–15 theaters per city
- `swiggy dataset.xlsx` — Restaurant meal prices for 55 cities (deduplicated to 50)

Movie prices had premium shows/IMAX filtered using IQR. Restaurant prices are per-person (raw "for two" values halved).

| City | Movie Ticket (₹) | Restaurant/person (₹) |
|---|---|---|
| Delhi | ₹390 | ₹125 |
| Mumbai | ₹600 | ₹150 |
| Salem | ₹60 | ₹125 |

---

## 3. Data Processing Methodology

### 3.1 Outlier Removal (IQR Method)
Applied to all multi-sample datasets (housing, grocery, healthcare, education, movies, restaurants):

```
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
Valid range: [Q1 1.5×IQR, Q3 + 1.5×IQR]
```

This removes luxury properties, IMAX tickets, specialist doctors, and premium tutors — preserving typical costs.

### 3.2 Index Calculation
Each component index is relative to Delhi (base = 100):

```
Component_Index = (City_Price / Delhi_Price) × 100
```

### 3.3 Weighted Overall Index

| Component | Raw Weight | Normalized Weight |
|-----------|-----------|-------------------|
| Grocery | 0.30 | **36.36%** |
| Housing | 0.25 | **30.30%** |
| Transport | 0.09 | **10.91%** |
| Healthcare | 0.053 | **6.42%** |
| Education | 0.05 | **6.06%** |
| Restaurant | 0.04 | **4.85%** |
| Electricity | 0.025 | **3.03%** |
| Movies | 0.0171 | **2.07%** |
| **Total** | **0.8251** | **100%** |

```
Cost_Index = (Grocery×36.36%) + (Housing×30.30%) + (Transport×10.91%) +
 (Healthcare×6.42%) + (Education×6.06%) + (Restaurant×4.85%) +
 (Electricity×3.03%) + (Movies×2.07%)
```

### 3.4 Missing Data Strategy
Missing values filled with median across all cities — robust to outliers and avoids under/overestimation.

---

## 4. Output Visualizations

The project generates **23 charts** in `outputs/visualizations/`. Key outputs are described below.

### 4.1 Overall Cost of Living — All 50 Cities

![All cities cost of living](/Users/mudit/.gemini/antigravity/brain/51f56e18-8f71-402f-823f-3fba7811cc7b/cost_of_living_all_cities.png)

*Horizontal bar chart ranking all 50 cities from most to least expensive. Mumbai stands clearly above the rest at index 162.79.*

---

### 4.2 City Rankings by Overall Index

![Overall index ranking](/Users/mudit/.gemini/antigravity/brain/51f56e18-8f71-402f-823f-3fba7811cc7b/overall_index_all_cities.png)

*Bar chart showing the cost of living index for all cities. The red dashed line at 100 represents Delhi's baseline.*

---

### 4.3 Component Heatmap — All 50 Cities

![Heatmap all cities](/Users/mudit/.gemini/antigravity/brain/51f56e18-8f71-402f-823f-3fba7811cc7b/heatmap_all_50_cities.png)

*Color-coded matrix showing each city's performance across all 8 cost components. Bright colors = expensive, dark colors = affordable. This reveals which component drives a city's high cost.*

---

### 4.4 Radar Chart — Multi-City Comparison

![Radar chart](/Users/mudit/.gemini/antigravity/brain/51f56e18-8f71-402f-823f-3fba7811cc7b/radar_chart_comparison.png)

*Radar / spider chart comparing selected cities across all 8 components simultaneously. Each axis represents a cost category — shows the "cost profile" of each city.*

---

### 4.5 Housing vs Overall Index

![Housing vs overall](/Users/mudit/.gemini/antigravity/brain/51f56e18-8f71-402f-823f-3fba7811cc7b/housing_vs_overall.png)

*Scatter plot showing the relationship between housing index and overall cost index. Demonstrates that housing is a strong predictor of overall cost of living.*

---

### 4.6 Top & Bottom Cities

![Top bottom cities](/Users/mudit/.gemini/antigravity/brain/51f56e18-8f71-402f-823f-3fba7811cc7b/top_bottom_cities.png)

*Side-by-side bar chart comparing the top 5 most expensive and bottom 5 most affordable cities for a quick summary.*

---

### 4.7 Component Distribution (Box Plot)

![Component boxplot](/Users/mudit/.gemini/antigravity/brain/51f56e18-8f71-402f-823f-3fba7811cc7b/component_distribution_boxplot.png)

*Box plots for all 8 cost components showing median, spread, and outliers across the 50 cities. Housing has the highest variance — grocery is most consistent.*

---

### 4.8 ML — Algorithm Comparison

![ML algorithm comparison](/Users/mudit/.gemini/antigravity/brain/51f56e18-8f71-402f-823f-3fba7811cc7b/ml_algorithm_comparison.png)

*Bar chart comparing accuracy/performance of multiple ML classification models (Random Forest, SVM, Decision Tree, Logistic Regression) used to classify cities into cost tiers.*

---

### 4.9 ML — Confusion Matrix

![ML confusion matrix](/Users/mudit/.gemini/antigravity/brain/51f56e18-8f71-402f-823f-3fba7811cc7b/ml_confusion_matrix.png)

*Confusion matrix for the best-performing ML classifier, showing how accurately the model predicted city tiers (Expensive / Moderate / Affordable).*

---

### 4.10 Weight Optimization Comparison

![Weight optimization](/Users/mudit/.gemini/antigravity/brain/51f56e18-8f71-402f-823f-3fba7811cc7b/weight_optimization_comparison.png)

*Comparison of city rankings under different weight schemes — original weights vs. optimized weights — showing how the ranking changes when emphasis shifts between components.*

---

### Full Visualization List

| # | File | Description |
|---|------|-------------|
| 1 | `all_50_cities_components.png` | Component breakdown for all 50 cities |
| 2 | `all_50_cities_ranking.png` | Overall ranking bar chart |
| 3 | `component_breakdown.png` | Weighted contribution breakdown |
| 4 | `component_distribution_boxplot.png` | Box plots per component |
| 5 | `components_all_cities.png` | Multi-line component chart |
| 6 | `cost_of_living_all_cities.png` | Horizontal bar, all cities |
| 7 | `cost_of_living_components_breakdown.png` | Stacked component chart |
| 8 | `dining_entertainment.png` | Restaurant & movie index |
| 9 | `distribution.png` | Index distribution histogram |
| 10 | `education_cost_comparison.png` | City-wise tutor fees |
| 11 | `electricity_index.png` | Electricity rate index |
| 12 | `heatmap.png` | Component heatmap (sample cities) |
| 13 | `heatmap_all_50_cities.png` | Full 50-city heatmap |
| 14 | `housing_vs_overall.png` | Housing vs. overall scatter |
| 15 | `ml_algorithm_comparison.png` | ML model comparison |
| 16 | `ml_confusion_matrix.png` | ML confusion matrix |
| 17 | `movie_ticket_index.png` | Movie ticket index |
| 18 | `overall_index_all_cities.png` | Overall index bar chart |
| 19 | `radar_chart_comparison.png` | Radar chart |
| 20 | `restaurant_index.png` | Restaurant price index |
| 21 | `top_bottom_cities.png` | Top/bottom 5 comparison |
| 22 | `weight_optimization_comparison.png` | Weight sensitivity analysis |
| 23 | `weighted_contribution_stacked.png` | Stacked weighted contribution |

---

## 5. Key Findings

### 5.1 Full City Rankings (All 50 Cities)

| Rank | City | Index | Category |
|------|------|-------|----------|
| 1 | Mumbai | 162.79 | Expensive |
| 2 | Bengaluru | 114.76 | Expensive |
| 3 | Kozhikode | 107.66 | Expensive |
| 4 | Hyderabad | 107.09 | Expensive |
| 5 | Patna | 100.72 | Baseline |
| 6 | Delhi | 100.00 | **Base** |
| 7 | Pune | 99.61 | Moderate |
| 8 | Kolkata | 98.57 | Moderate |
| 9 | Ahmedabad | 95.42 | Moderate |
| 10 | Coimbatore | 93.04 | Moderate |
| 11 | Chennai | 92.25 | Moderate |
| 12 | Raipur | 89.95 | Moderate |
| 13 | Bhubaneswar | 89.18 | Moderate |
| 14 | Jaipur | 88.38 | Moderate |
| 15 | Rajkot | 85.78 | Moderate |
| 16 | Bhopal | 85.25 | Moderate |
| 17 | Jabalpur | 84.32 | Moderate |
| 18 | Sangli | 83.17 | Moderate |
| 19 | Agra | 82.75 | Moderate |
| 20 | Thrissur | 82.52 | Moderate |
| 21 | Salem | 81.95 | Affordable |
| 22 | Mysuru | 81.08 | Affordable |
| 23 | Kollam | 81.05 | Affordable |
| 24 | Nagpur | 81.03 | Affordable |
| 25 | Kolhapur | 80.48 | Affordable |
| 26 | Lucknow | 80.41 | Affordable |
| 27 | Erode | 80.35 | Affordable |
| 28 | Chandigarh | 80.16 | Affordable |
| 29 | Aurangabad | 79.87 | Affordable |
| 30 | Visakhapatnam | 79.52 | Affordable |
| 31 | Kochi | 79.24 | Affordable |
| 32 | Kanpur | 79.21 | Affordable |
| 33 | Asansol | 78.39 | Affordable |
| 34 | Vadodara | 77.82 | Affordable |
| 35 | Madurai | 77.63 | Affordable |
| 36 | Meerut | 77.60 | Affordable |
| 37 | Kottayam | 77.11 | Affordable |
| 38 | Mangaluru | 76.59 | Affordable |
| 39 | Surat | 76.49 | Affordable |
| 40 | Thiruvananthapuram | 76.36 | Affordable |
| 41 | Indore | 76.10 | Affordable |
| 42 | Nashik | 75.71 | Affordable |
| 43 | Amaravati | 75.65 | Affordable |
| 44 | Hubli | 75.10 | Affordable |
| 45 | Kannur | 74.34 | Affordable |
| 46 | Jamnagar | 72.77 | Affordable |
| 47 | Ludhiana | 72.50 | Affordable |
| 48 | Tiruchirappalli | 71.41 | Affordable |
| 49 | Solapur | 68.20 | Very Affordable |
| 50 | Malappuram | 69.54 | Very Affordable |

### 5.2 Component-Level Insights

| Component | Highest City | Lowest City | Key Insight |
|-----------|-------------|-------------|-------------|
| Housing | Mumbai (230.86) | Malappuram (14.77) | **15× variation** — largest spread |
| Grocery | Kozhikode (151.21) | Nashik (90.94) | ~65% variation |
| Transport | Hyderabad (242.31) | Mangaluru (43.75) | Uber pricing varies widely |
| Healthcare | Mumbai (135.0) | Salem/Mangaluru (15.0) | 9× variation |
| Education | Rajkot (105.16) | Salem/Madurai (~15) | Online platform skew |
| Electricity | Mumbai (212.5) | Visakhapatnam (75.0) | State tariff differences |
| Restaurant | Mumbai/Mysuru (120–150) | Kolkata (80.0) | Moderate variation |
| Movies | Mumbai/Kozhikode (154) | Salem/Madurai (~15) | Theater concentration |

### 5.3 City Tiers

```
 Expensive (Index > 100): Mumbai, Bengaluru, Kozhikode, Hyderabad, Patna
 Moderate (Index 80–100): Delhi, Pune, Kolkata, Ahmedabad, Chennai, Jaipur...
 Affordable (Index < 80): Malappuram, Solapur, Tiruchirappalli, Ludhiana...
```

---

## 6. Machine Learning Applications

The project includes implemented ML models in `src/ml_classification.py` and `src/ml_demo.py`.

### 6.1 City Tier Classification
- **Goal:** Automatically classify cities as Expensive / Moderate / Affordable
- **Algorithms tested:** Random Forest, SVM, Decision Tree, Logistic Regression
- **Features:** All 8 component indices
- **Output:** See confusion matrix and algorithm comparison charts above

### 6.2 City Recommendation System
- **Goal:** Recommend cities matching user priorities (cheap housing, don't care about education, etc.)
- **Method:** Priority-based weighted scoring + cosine similarity
- **Interface:** Interactive Streamlit web app (`website/app.py`)

### 6.3 Weight Optimization
- **Goal:** Find the optimal component weights that best explain real cost patterns
- **Method:** Scipy optimization on index calculation weights
- **File:** `src/weight_optimizer.py`

### 6.4 Potential Future ML (from `docs/ML_APPLICATIONS.md`)
- **Predictive Modeling:** Forecast costs for new/uncharted cities (Random Forest, XGBoost)
- **Clustering:** K-Means city grouping by cost profiles
- **Anomaly Detection:** Isolation Forest to flag unusual pricing
- **Time Series:** ARIMA/Prophet to track cost changes over time
- **NLP:** Sentiment analysis on city reviews to complement quantitative data

---

## 7. Project Architecture

```
BMP Data Modelling/
 data/
 raw/
 Magic Bricks data/ 50 housing CSV files
 grocery/blinkit_citywise/ 41 grocery Excel files
 transport/ Uber + fuel prices
 healthcare/ Doctor consultation fees
 education/ 60K+ tutor listings
 utilities/ Electricity tariffs
 entertainment/ Movies + restaurants
 processed/ Intermediate outputs

 src/
 main.py Pipeline orchestrator
 data_loader.py Load & preprocess all sources
 cost_calculator.py Index formula & weighting
 visualizer.py 23 chart types
 ml_classification.py City tier ML models
 ml_demo.py ML demonstrations
 weight_optimizer.py Optimal weight search
 recommender.py City recommendation logic

 website/
 app.py Streamlit web interface
 recommender.py Priority-based matching

 outputs/
 reports/cost_index_results.csv Full results (50 cities)
 visualizations/ 23 PNG charts

 docs/ Full documentation
```

**Technology Stack:**
- **Language:** Python 3.8+
- **Data Processing:** `pandas`, `numpy`
- **Visualization:** `matplotlib`, `seaborn`
- **Web Interface:** `streamlit`
- **ML:** `scikit-learn`
- **File I/O:** `openpyxl` (Excel), native `csv`

---

## 8. Use Cases

### For Individuals
- **Relocation decisions:** Compare your target city's cost of living against your current city
- **Salary negotiation:** Quantify the cost premium of metros vs. Tier-2 cities
- **Budget planning:** Know the housing/grocery/transport breakdown before moving

### For Businesses
- **Location-based salaries:** Set fair compensation by city using indexed cost data
- **Office location strategy:** Balance talent availability vs. real estate cost
- **Market segmentation:** Understand cost profiles for pricing products/services

### For Policy Makers
- **Identify affordability gaps:** Spot where housing or groceries spike above the national norm
- **Infrastructure investment:** Prioritize cities with high transport costs
- **Monitor equity:** Track if lower-tier cities are convergening with metros over time

### For Researchers
- **Urban economics study:** Compare cost drivers across different city typologies
- **Regional analysis:** Kerala cities (Kochi, Kozhikode, Thiruvananthapuram) show high grocery costs vs. national median
- **Academic benchmark:** A reproducible index with transparent methodology

---

## 9. Running the Project

```bash
# Full analysis pipeline
./run.sh

# Or manually
cd src && python3 main.py

# Launch interactive city recommender
streamlit run website/app.py
```

**Output files generated:**
- `outputs/reports/cost_index_results.csv` — Full results
- `outputs/visualizations/*.png` — 23 charts

---

## 10. Limitations & Future Enhancements

### Current Limitations
1. **Point-in-time data** — Prices are not tracked over time
2. **Quality variations ignored** — A ₹5,000/sqft flat in City A quality of same in City B 
3. **Grocery coverage gap** — 9 cities rely on median imputation
4. **Small dataset for ML** — 50 cities limits complex model training
5. **No income data** — Cannot compute affordability ratio (cost vs. salary)

### Proposed Enhancements
1. Integrate monthly data collection for temporal tracking
2. Add income / average salary data for affordability index
3. Implement interactive web dashboard with filters and drill-downs
4. Add quality-of-life scores (pollution, infrastructure, greenery)
5. Regional clustering with geographic visualizations (choropleth maps)
6. Expand to 100+ cities

---

*Report generated: April 2026 | Project by BMP Data Modelling*
