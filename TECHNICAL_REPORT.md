---
title: "Cost of Living Index for Indian Cities: A Data-Driven Analysis"
subtitle: "Technical Report — BMP Data Modelling"
date: "April 2026"
---

# 1. Introduction

Comparing the cost of living across cities is rarely straightforward. Prices vary not just between metros and smaller towns but also within the same tier of cities, driven by differences in local supply chains, regulatory environments, and consumer habits. Most existing indices either cover too few cities, rely on outdated survey data, or collapse all expenses into a single number without exposing what is driving costs in any particular place.

This report documents the design, data pipeline, and results of a cost of living index built for 50 Indian cities. The index is constructed entirely from raw transactional data pulled from live platforms — property listings, grocery delivery apps, ride-hailing services, tutor marketplaces, and restaurant aggregators. Every step of the pipeline, from how data is cleaned to how missing values are handled, is described here so the work can be reproduced or extended.

Delhi is used as the base city, assigned an index of 100. All other cities are expressed relative to that baseline. A city with an index of 130 costs 30% more than Delhi in aggregate; a city at 80 costs 20% less.

---

# 2. Scope and Objectives

The primary goals of this project were:

- Build a reproducible, city-level cost of living index covering at least 50 cities across different tiers of Indian urban settlement.
- Use real transactional data rather than consumer surveys, which are expensive to run and easy to date.
- Weight each expense category according to how much of a typical urban household budget it actually consumes.
- Generate visualisations that allow comparisons across individual categories, not just at the aggregate level.
- Identify where the largest cost gaps between cities occur and which components drive them.

A secondary objective was to connect the index to a practical tool — a city recommendation engine — that lets individuals explore trade-offs when considering relocation.

---

# 3. Data Sources

Data was collected from seven categories, each representing a distinct slice of household spending. The sections below describe each source, the format of the raw files, and the volume of records processed.

## 3.1 Housing — MagicBricks

Property listing data was collected from MagicBricks for 50 cities. Each city has its own CSV file named in the format `{CityName}_magicbricks.csv`. The files contain individual property listings with the following fields: city name, number of floors, number of bathrooms, carpet area in square feet, listed price, and derived price per square foot.

The metric used in the index is the price per square foot rather than the absolute price of a flat. This makes comparisons between cities more consistent, since the size distribution of properties varies considerably — Mumbai listings skew towards smaller flats compared to cities like Jaipur or Nagpur.

| City | Median Price/sq ft (INR) |
|---|---|
| Delhi | 10,231 |
| Mumbai | 23,619 |
| Bengaluru | 11,029 |
| Jaipur | 3,579 |
| Malappuram | 1,512 |

A total of 50 files were processed, covering the full city list with no gaps in housing coverage.

## 3.2 Grocery — Blinkit

Grocery price data was sourced from Blinkit, an online grocery delivery platform with strong city-level penetration across tier-1 and tier-2 markets. Files are in Excel format, one per city, and contain product names alongside current listed prices.

The raw product lists are heterogeneous — different cities stock different SKUs, and price points span a wide range from a few rupees for spices to several hundred for packaged goods. Rather than trying to build a fixed basket comparison, we calculate the IQR-cleaned median price across all products in each city. This is a reasonable proxy for the general level of grocery prices, though it implicitly assumes that the product mix tracked by Blinkit is broadly comparable across cities.

Coverage is 41 out of 50 cities. The nine cities without Blinkit data — mostly smaller metros — are filled with the national median.

## 3.3 Transport — Uber and Fuel Prices

Transport costs are captured through two separate files. The first is an Excel sheet containing Uber's per-kilometre rate for each city. The second is a CSV with city-wise petrol, diesel, CNG, and LPG prices.

Uber pricing is used as the index metric because it represents the cost of on-demand urban transport, which is how a large proportion of working urban residents commute. Fuel prices were loaded and are available in the dataset but are not directly included in the weighted index, since they are more relevant to car owners and the price variation across cities is substantially lower (driven mainly by state-level taxes rather than local market conditions).

## 3.4 Healthcare — General Physician Fees

Doctor consultation fees were compiled in a wide-format Excel file where each row corresponds to a city and each subsequent column contains a fee observation from a different clinic or practitioner. This format is somewhat unusual but preserves the full sample for each city rather than pre-aggregating it, which is useful for further analysis.

Only general physician fees are included. Specialist fees, which can be an order of magnitude higher, were excluded from the comparison because they do not represent routine household spending in the same way.

## 3.5 Education — Tutor Marketplace

Education cost data comes from a tutor listing platform. The raw file contains 60,256 listings with fields for tutor ID, city, location description, and a fee range string in the format "INR 300–1,000/hour (USD …)". Monthly fee listings are excluded — only per-hour rates are retained, which leaves 46,965 records.

Fee extraction uses a regular expression to pull numeric values following the INR symbol. Where a range is given (e.g., INR 300–1,000), the midpoint is used. The per-city metric is the mean of IQR-cleaned hourly rates.

This data source is one of the richer ones in terms of volume — cities average around 940 listings each, giving a stable estimate of local tutoring costs.

## 3.6 Utilities — Electricity Tariffs

Electricity rates come from a single Excel file with one row per city, containing the effective tariff rate in rupees per kilowatt-hour. These figures were sourced from state electricity board schedules. No outlier removal is applied since there is a single figure per city.

The range across the 50 cities is INR 3.00 to 8.50 per unit, with the variation explained entirely by differences in state tariff structures. Delhi's rate of INR 4.00 per unit sits towards the lower end of the national range.

## 3.7 Entertainment — Movie Tickets and Restaurants

Two entertainment files are included. Movie ticket prices were gathered for 5 to 15 cinemas per city and stored in an Excel file with a merged header row. Restaurant prices come from a Swiggy dataset containing average meal prices alongside location tags. Swiggy lists prices "for two", so all values are halved before analysis to get a per-person cost.

City name aliases require handling for this dataset — Bangalore is mapped to Bengaluru, Mysore to Mysuru, Trichy to Tiruchirappalli, and so on. Without this normalisation, city-level joins between datasets fail silently, which is one of the more common but hard-to-spot data quality issues in multi-source pipelines.

---

# 4. Methodology

## 4.1 Outlier Removal

Before any aggregation, each multi-observation dataset goes through IQR-based outlier removal applied at the city level:

$$Q_1 = 25\text{th percentile}, \quad Q_3 = 75\text{th percentile}$$

$$\text{IQR} = Q_3 - Q_1$$

$$\text{Valid range} = [Q_1 - 1.5 \times \text{IQR},\; Q_3 + 1.5 \times \text{IQR}]$$

This removes extreme observations — luxury penthouses from the housing data, IMAX ticket prices from the movie data, premium specialist tutors from the education data — without requiring manual curation of the dataset. The assumption is that what matters for a cost of living index is what a typical resident actually pays, not what the most expensive option in the city charges.

## 4.2 City Name Normalisation

A consistent city name is essential when merging datasets sourced from different platforms. A mapping dictionary handles known aliases and spelling variations:

| Alias Used in Raw Data | Canonical Name |
|---|---|
| Bangalore | Bengaluru |
| Bombay | Mumbai |
| Calcutta | Kolkata |
| Mysore | Mysuru |
| Trichy | Tiruchirappalli |
| Trivandrum | Thiruvananthapuram |
| Merrut | Meerut |

After normalisation, all datasets are joined on the canonical city name using outer joins to preserve all available data before filtering to the official 50-city list.

## 4.3 Index Calculation

Each component index is expressed as a ratio relative to Delhi:

$$\text{Component Index}_{\text{city}} = \frac{\text{City Price}}{\text{Delhi Price}} \times 100$$

The overall cost of living index is a weighted average of the eight component indices:

$$\text{Cost Index} = \sum_{i=1}^{8} w_i \times \text{Component Index}_i$$

## 4.4 Weight Derivation

Raw weights are assigned based on typical urban household expenditure patterns in India. They are then re-normalised to sum to 100% at runtime:

| Component | Raw Weight | Normalised Weight | Basis |
|---|---|---|---|
| Grocery | 0.30 | 36.36% | Daily consumption — largest recurring expense |
| Housing | 0.25 | 30.30% | Rent or EMI — largest fixed monthly outflow |
| Transport | 0.09 | 10.91% | Daily commute via ride-hailing |
| Healthcare | 0.053 | 6.42% | Routine doctor visits |
| Education | 0.050 | 6.06% | Private tutoring, which is widespread in urban India |
| Restaurant | 0.040 | 4.85% | Meals out and food delivery |
| Electricity | 0.025 | 3.03% | Monthly utility billing |
| Movies | 0.0171 | 2.07% | Discretionary entertainment proxy |
| **Total** | **0.8251** | **100%** | |

The raw weights sum to 0.8251, which reflects the fact that not all household expenses are captured here — clothing, personal care, savings, and others are excluded. By re-normalising, we ensure the index reflects the relative importance of the included categories.

## 4.5 Missing Value Handling

When a city has no data for a given component, the gap is filled with the median value across all cities that do have data. Median rather than mean is used because the distribution of component values across cities tends to be right-skewed — a few cities like Mumbai pull the mean upward in ways that would overestimate the typical national value.

---

# 5. Results

## 5.1 Full City Rankings

The table below gives the complete cost of living index for all 50 cities, sorted from most to least expensive.

| Rank | City | Index | Category |
|------|------|-------|----------|
| 1 | Mumbai | 162.79 | Expensive |
| 2 | Bengaluru | 114.76 | Expensive |
| 3 | Kozhikode | 107.66 | Expensive |
| 4 | Hyderabad | 107.09 | Expensive |
| 5 | Patna | 100.72 | Near Baseline |
| 6 | Delhi | 100.00 | Base City |
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
| 49 | Malappuram | 69.54 | Very Affordable |
| 50 | Solapur | 68.20 | Very Affordable |

## 5.2 Component-Level Variation

The aggregate index can mask substantial differences at the component level. Housing is the most volatile component — Mumbai's housing index of 230.86 is 15 times that of Malappuram (14.77), a spread far larger than any other category. This means that housing is the primary driver of Mumbai's exceptional overall score, rather than a uniform increase across all categories.

Grocery variation is narrower (roughly 65%), partly because Blinkit operates on standardised national pricing for many SKUs. Transport shows the widest variation in relative terms because Uber's pricing strategy differs significantly by city — Hyderabad (242.31) and Mumbai (220.37) are more than five times as expensive per kilometre as Mangaluru (43.75).

Healthcare varies approximately ninefold from Salem and Mangaluru at index 15 up to Mumbai at 135. This likely reflects both market concentration — fewer clinics in smaller cities tend to charge less — and the higher cost base of medical services in larger urban markets.

Education shows an interesting pattern. The cities with the highest tutor rates tend to be large metros with competitive exam coaching cultures (Mumbai at 113.87, Rajkot at 105.16), while smaller south Indian cities come in considerably lower.

| Component | Highest (Index) | Lowest (Index) |
|---|---|---|
| Housing | Mumbai (230.86) | Malappuram (14.77) |
| Grocery | Kozhikode (151.21) | Nashik (90.94) |
| Transport | Hyderabad (242.31) | Mangaluru (43.75) |
| Healthcare | Mumbai (135.0) | Salem (15.0) |
| Education | Mumbai (113.87) | Salem (15.38) |
| Electricity | Mumbai (212.5) | Visakhapatnam (75.0) |
| Restaurant | Mumbai / Mysuru (120) | Kolkata (80.0) |
| Movies | Kozhikode (153.85) | Salem / Madurai (15.38) |

## 5.3 Regional Patterns

Kerala cities — Kozhikode, Thrissur, Kochi, Kollam, Kottayam, Thiruvananthapuram, Kannur, Malappuram — present an unusual picture. Despite being relatively affordable in housing, some of them (particularly Kozhikode) register very high grocery index scores. This is plausible given Kerala's higher-than-average food prices, which are partly a function of the state's limited agricultural hinterland and its dependence on imports from other states.

Gujarat cities — Rajkot, Surat, Ahmedabad, Vadodara, Jamnagar — cluster in the moderate-to-affordable range across most components, with the exception of education in some cities. This is consistent with Gujarat's reputation for cost-effective urban living despite strong economic activity.

Maharashtra presents a split picture: Mumbai is in a class of its own, while Pune, Nagpur, Nashik, Aurangabad, Kolhapur, and Sangli all sit comfortably in the affordable to moderate band. Proximity to Mumbai does not appear to push costs significantly higher in these cities.

---

# 6. Implementation

## 6.1 Code Structure

The pipeline is written in Python and broken into discrete modules:

| Module | Responsibility |
|---|---|
| `data_loader.py` | Load and clean each data source; return standardised DataFrames |
| `cost_calculator.py` | Apply weights, normalise, and compute the index |
| `visualizer.py` | Generate all output charts |
| `ml_classification.py` | Classify cities into cost tiers using ML models |
| `weight_optimizer.py` | Search for weight combinations that minimise a specified cost function |
| `recommender.py` | Priority-based city recommendation logic |
| `main.py` | Top-level orchestration; runs the full pipeline end to end |

## 6.2 Running the Pipeline

```bash
# Full pipeline from the project root
./run.sh

# Equivalent manual run
cd src && python3 main.py

# Interactive city recommender
streamlit run website/app.py
```

Output is written to two locations: `outputs/reports/cost_index_results.csv` for the full numerical results, and `outputs/visualizations/` for the chart set (23 PNG files).

## 6.3 Dependencies

| Library | Purpose |
|---|---|
| pandas | Data loading, merging, and transformation |
| numpy | Array operations and IQR calculations |
| matplotlib | All chart rendering |
| seaborn | Heatmap and styled statistical charts |
| openpyxl | Reading Excel files (.xlsx) |
| streamlit | Web interface for city recommender |
| scikit-learn | ML classification models |

---

# 7. Machine Learning Component

## 7.1 City Tier Classification

A classification model is trained to assign cities to one of three tiers — Expensive, Moderate, and Affordable — using the eight component indices as features. Four algorithms are compared: Random Forest, Support Vector Machine, Decision Tree, and Logistic Regression. Random Forest and SVM generally outperform the simpler classifiers on this dataset given the relatively small sample size and the non-linear relationships between components.

Training on 50 data points is a known limitation. The models are useful for demonstrating the classification approach and for flagging which components are most predictive of tier assignment, rather than for deployment in a production system without additional data.

## 7.2 Recommendation Engine

The city recommender takes user-defined priorities for each cost category — the user specifies whether they want a city to be cheap, expensive, or neutral for housing, grocery, transport, and so on — and scores all 50 cities against those preferences. Cities where the actual component index aligns with the stated preference score higher.

This is implemented in `website/recommender.py` and surfaced through a Streamlit interface. A user might, for example, specify that affordable housing is a hard requirement while transport costs are not a concern — the system will rank cities accordingly and show the component breakdown for each result.

## 7.3 Weight Optimisation

`weight_optimizer.py` uses Scipy's optimisation routines to find component weights that minimise a specified objective. The primary use case explored here is finding the weight set that produces the smallest variance in city rankings when individual components are perturbed — a measure of index robustness. The optimised weights are compared to the original expenditure-based weights to see how sensitive the rankings are to the weighting scheme.

---

# 8. Limitations

A few limitations are worth being explicit about before drawing conclusions from this data.

**Data is not contemporaneous.** The various datasets were collected at different points in time. Grocery prices from Blinkit may be from a different quarter than the MagicBricks listings, and both may have shifted by the time this report was written. The index is a snapshot, not a continuous tracker.

**Quality differences are not captured.** An average apartment in Bengaluru at INR 11,000 per square foot is almost certainly better built and better located than an average apartment at the same price in a smaller city. The index makes no adjustment for quality, which means it may understate the real effective cost of living in cities where the quality-to-price ratio is lower.

**Grocery imputation affects nine cities.** The nine cities without Blinkit coverage are assigned the national median grocery value, which means their grocery index is fixed at exactly 100. This is known and documented, but it means that comparisons involving those cities should be treated with some caution on the grocery dimension specifically.

**Small sample for ML.** Fifty cities is not a large training corpus for machine learning. The classification models are illustrative rather than production-grade, and the accuracy figures should be taken in that context.

**Income data is absent.** Without income data, the index cannot produce an affordability measure — a ratio of cost to local salary that would be more useful for relocation decisions than the cost index alone.

---

# 9. Conclusions

The cost of living gap between Indian cities is real and large. Mumbai's index of 162.79 is more than twice that of Solapur at 68.20, and that ratio holds even after removing the most extreme values. Housing is the primary driver — it accounts for 30% of the index weight and shows the widest variation of any component.

Tier-2 cities are not uniformly affordable. Some, like Coimbatore, Bhubaneswar, and Jaipur, sit only modestly below Delhi. Others, like Malappuram, Jamnagar, and Tiruchirappalli, are genuinely low-cost environments. The index makes it easier to distinguish between these two groups than headline city-tier labels do.

The pipeline built here is modular and extensible. Adding a new data source requires writing a new loader function in `data_loader.py`, adding the corresponding weight and label in the configuration, and re-running. The architecture does not need to change.

The next logical step would be to put this on a time series footing — running the pipeline quarterly and storing the results — so that cost trends can be tracked over time rather than read as a single snapshot.

---

# Appendix A: Output Files

| File | Description |
|---|---|
| `outputs/reports/cost_index_results.csv` | Full results: raw prices, component indices, overall index for all 50 cities |
| `outputs/visualizations/cost_of_living_all_cities.png` | Horizontal bar chart, all 50 cities ranked |
| `outputs/visualizations/heatmap_all_50_cities.png` | Component heatmap across all cities |
| `outputs/visualizations/radar_chart_comparison.png` | Multi-city radar comparison |
| `outputs/visualizations/component_distribution_boxplot.png` | Box plot distribution per component |
| `outputs/visualizations/housing_vs_overall.png` | Housing vs. overall index scatter |
| `outputs/visualizations/ml_algorithm_comparison.png` | ML classifier accuracy comparison |
| `outputs/visualizations/ml_confusion_matrix.png` | ML confusion matrix |
| `outputs/visualizations/weight_optimization_comparison.png` | Weight sensitivity analysis |
| `outputs/visualizations/top_bottom_cities.png` | Top/bottom 5 cities comparison |

# Appendix B: City Name Canonical List

The following 50 cities form the official dataset: Agra, Ahmedabad, Amaravati, Asansol, Aurangabad, Bengaluru, Bhopal, Bhubaneswar, Chandigarh, Chennai, Coimbatore, Delhi, Erode, Hubli, Hyderabad, Indore, Jabalpur, Jaipur, Jamnagar, Kannur, Kanpur, Kochi, Kolhapur, Kolkata, Kollam, Kottayam, Kozhikode, Lucknow, Ludhiana, Madurai, Malappuram, Mangaluru, Meerut, Mumbai, Mysuru, Nagpur, Nashik, Patna, Pune, Raipur, Rajkot, Salem, Sangli, Solapur, Surat, Thiruvananthapuram, Thrissur, Tiruchirappalli, Vadodara, Visakhapatnam.
