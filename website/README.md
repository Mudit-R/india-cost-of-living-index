# Cost of Living City Recommender - Web Interface

An interactive Streamlit web application that helps users find the best Indian city based on their spending preferences across 8 categories.

## Features

- **8 Category Analysis**: Housing, Grocery, Transport, Healthcare, Education, Electricity, Restaurant, Movies
- **Interactive Sliders**: Rate your comfort level for spending in each category (1-5 scale)
- **Smart Recommendations**: Get top 3 city matches based on your preferences
- **Detailed Metrics**: View cost indices and match scores for all 50 cities
- **Beautiful UI**: Modern, responsive design with custom styling

## Prerequisites

Make sure you have generated the cost index data first:

```bash
cd src
python main.py
```

This will create `outputs/reports/cost_index_results.csv` which the website uses.

## Installation

Install Streamlit if you haven't already:

```bash
pip install streamlit
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Running the Website

From the project root directory:

```bash
streamlit run website/app.py
```

Or from the website directory:

```bash
cd website
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## How to Use

1. **Rate Your Preferences**: Use the sliders to rate each category from 1 to 5:
   - **1-2**: You prefer LOW cost (budget-friendly)
   - **3**: Neutral (balanced)
   - **4-5**: You prefer HIGH quality (willing to pay more)

2. **Get Recommendations**: Click the "Get Recommendations" button

3. **View Results**: 
   - See your top 3 city matches with detailed explanations
   - View overall cost index (Delhi = 100 baseline)
   - Check match scores (lower = better fit)
   - Expand to see all 50 cities ranked

## Understanding the Results

### Cost Index
- **Base City**: Delhi = 100
- **Higher Index**: More expensive than Delhi
- **Lower Index**: More affordable than Delhi

### Match Score
- Lower scores indicate better matches to your preferences
- The algorithm considers both your budget preferences and quality expectations

### Categories Explained

- **Housing**: Property prices and rent (based on MagicBricks data)
- **Grocery**: Daily food and grocery costs (based on Blinkit product prices)
- **Transport**: Uber/taxi fares and fuel costs
- **Healthcare**: General physician consultation fees
- **Education**: Tutor and coaching fees (per-hour rates)
- **Electricity**: Utility and electricity rates
- **Restaurant**: Dining out costs (Swiggy data)
- **Movies**: Entertainment and movie ticket prices

## Data Source

The application uses real data from 50 Indian cities:
- 50 cities across India
- 8 cost categories
- Data collected from multiple sources (MagicBricks, Blinkit, Swiggy, etc.)
- Processed with outlier removal and normalization

## Troubleshooting

### "Data file not found" Error
Run the data processing pipeline first:
```bash
cd src
python main.py
```

### "Required column missing" Error
The CSV file may be outdated. Regenerate it:
```bash
cd src
python main.py
```

### Port Already in Use
If port 8501 is busy, specify a different port:
```bash
streamlit run website/app.py --server.port 8502
```

## File Structure

```
website/
├── app.py              # Main Streamlit application
├── recommender.py      # Recommendation engine and logic
└── README.md          # This file
```

## Command Line Version

For a command-line interface version, you can also use:

```bash
cd website
python recommender.py
```

This will prompt you for preferences in the terminal and output recommendations.
