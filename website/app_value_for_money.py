import streamlit as st
import pandas as pd
import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Determine correct data path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
data_path = os.path.join(parent_dir, 'outputs', 'reports', 'cost_index_results.csv')

# Page configuration
st.set_page_config(
    page_title="Value-for-Money City Recommender",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Helvetica+Neue:wght@400;500;700&display=swap');
    
    * { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #F9F3EA; }
    .main { background: transparent; padding: 2rem 1rem; }
    
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 5rem;
        font-weight: 500;
        color: #1E1B18;
        margin: 0;
        letter-spacing: -1.5px;
    }
    
    .subtitle {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 0.9rem;
        color: #726E68;
        margin-top: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 500;
        color: #1E1B18;
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 1rem;
        border-bottom: 1px solid #1E1B18;
        letter-spacing: -1px;
    }
    
    .city-card {
        background: transparent;
        padding: 3rem 0;
        border-radius: 0;
        border: none;
        border-top: 1px solid #1E1B18;
        margin-bottom: 1rem;
    }
    
    .city-name {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 500;
        color: #1E1B18;
        margin: 0.5rem 0;
        letter-spacing: -1px;
    }
    
    .metric-container {
        background: transparent;
        padding: 1rem 1.5rem;
        border-radius: 0;
        text-align: left;
        border: none;
        height: 100%;
        border-left: 1px solid #1E1B18;
    }
    
    .metric-label {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 0.85rem;
        color: #726E68;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 500;
        color: #1E1B18;
        letter-spacing: -1.5px;
        line-height: 1;
    }
    
    .value-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 1rem;
    }
    
    .excellent-value {
        background: #D4EDDA;
        color: #155724;
        border: 1px solid #C3E6CB;
    }
    
    .good-value {
        background: #D1ECF1;
        color: #0C5460;
        border: 1px solid #BEE5EB;
    }
    
    .fair-value {
        background: #FFF3CD;
        color: #856404;
        border: 1px solid #FFEAA7;
    }
    
    .poor-value {
        background: #F8D7DA;
        color: #721C24;
        border: 1px solid #F5C6CB;
    }
    
    .stButton>button {
        background: #21201D !important;
        color: #FAF4EB !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        border-radius: 2px !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .info-box {
        background: #F4EBE0;
        border: 1px solid #E5DBCD;
        border-radius: 8px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 class="main-title">Value-for-Money City Recommender</h1>
    <p class="subtitle">Find cities where quality of life exceeds the cost of living</p>
</div>
""", unsafe_allow_html=True)

# Information section
with st.expander("📖 How This Tool Works"):
    st.markdown("""
    <div class="info-box">
        <h3>Value-for-Money Analysis</h3>
        <p>This tool compares <strong>Cost of Living</strong> against your personal <strong>Quality of Life preferences</strong> to find cities that offer the best value.</p>
        
        <h4>How it works:</h4>
        <ol>
            <li><strong>Cost Index (Calculated):</strong> Based on actual prices - Delhi = 100</li>
            <li><strong>Quality of Life Index (Your Input):</strong> Rate each city based on your preferences - Delhi = 100</li>
            <li><strong>Value Score:</strong> Quality / Cost ratio - Higher is better!</li>
        </ol>
        
        <h4>Example:</h4>
        <ul>
            <li>Mumbai: Cost = 162.79, Quality = 180 → Value = 1.11 (Good value despite high cost!)</li>
            <li>Delhi: Cost = 100, Quality = 100 → Value = 1.00 (Baseline)</li>
            <li>Solapur: Cost = 68.20, Quality = 50 → Value = 0.73 (Cheap but lower quality)</li>
        </ul>
        
        <p><strong>Tip:</strong> You can upload a CSV file with your quality ratings, or use our quick rating tool below.</p>
    </div>
    """, unsafe_allow_html=True)

# Load cost data
@st.cache_data
def load_cost_data():
    df = pd.read_csv(data_path)
    return df.sort_values('cost_of_living_index')

try:
    cost_df = load_cost_data()
    cities = cost_df['City'].tolist()
    
    st.markdown('<div class="section-header">Step 1: Input Quality of Life Ratings</div>', unsafe_allow_html=True)
    
    # Option to upload CSV or manual input
    input_method = st.radio(
        "Choose input method:",
        ["Upload CSV File", "Quick Rating Tool", "Manual Entry for All Cities"],
        horizontal=True
    )
    
    quality_ratings = {}
    
    if input_method == "Upload CSV File":
        st.info("Upload a CSV file with columns: City, Quality_Index (Delhi should be 100)")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            quality_df = pd.read_csv(uploaded_file)
            if 'City' in quality_df.columns and 'Quality_Index' in quality_df.columns:
                quality_ratings = dict(zip(quality_df['City'], quality_df['Quality_Index']))
                st.success(f"✓ Loaded quality ratings for {len(quality_ratings)} cities")
                
                # Show preview
                with st.expander("Preview uploaded data"):
                    st.dataframe(quality_df.head(10))
            else:
                st.error("CSV must have 'City' and 'Quality_Index' columns")
        else:
            # Provide download template
            template_df = pd.DataFrame({
                'City': cities,
                'Quality_Index': [100] * len(cities)  # Default all to 100
            })
            csv = template_df.to_csv(index=False)
            st.download_button(
                label="Download Template CSV",
                data=csv,
                file_name="quality_of_life_template.csv",
                mime="text/csv"
            )
    
    elif input_method == "Quick Rating Tool":
        st.info("Rate cities in tiers. Delhi = 100 (baseline)")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.subheader("Premium (120-150)")
            premium_rating = st.number_input("Rating", 120, 150, 130, key="premium")
            premium_cities = st.multiselect("Select cities", cities, key="premium_cities")
        
        with col2:
            st.subheader("Above Average (100-120)")
            above_avg_rating = st.number_input("Rating", 100, 120, 110, key="above")
            above_avg_cities = st.multiselect("Select cities", cities, key="above_cities")
        
        with col3:
            st.subheader("Average (80-100)")
            avg_rating = st.number_input("Rating", 80, 100, 90, key="avg")
            avg_cities = st.multiselect("Select cities", cities, key="avg_cities")
        
        with col4:
            st.subheader("Below Average (50-80)")
            below_avg_rating = st.number_input("Rating", 50, 80, 70, key="below")
            below_avg_cities = st.multiselect("Select cities", cities, key="below_cities")
        
        # Assign ratings
        for city in premium_cities:
            quality_ratings[city] = premium_rating
        for city in above_avg_cities:
            quality_ratings[city] = above_avg_rating
        for city in avg_cities:
            quality_ratings[city] = avg_rating
        for city in below_avg_cities:
            quality_ratings[city] = below_avg_rating
        
        # Default unrated cities to 100
        for city in cities:
            if city not in quality_ratings:
                quality_ratings[city] = 100
        
        st.info(f"Rated {len([c for c in quality_ratings.values() if c != 100])} cities explicitly, {len([c for c in quality_ratings.values() if c == 100])} cities defaulted to 100")
    
    else:  # Manual Entry for All Cities
        st.info("Enter quality of life index for each city (Delhi = 100 baseline)")
        
        # Create columns for better layout
        num_cols = 3
        cols = st.columns(num_cols)
        
        for idx, city in enumerate(cities):
            with cols[idx % num_cols]:
                default_val = 100 if city == 'Delhi' else 100
                quality_ratings[city] = st.number_input(
                    city,
                    min_value=0,
                    max_value=200,
                    value=default_val,
                    step=5,
                    key=f"quality_{city}"
                )
    
    # Calculate button
    st.markdown("<br>", unsafe_allow_html=True)
    top_n = st.slider("Number of recommendations:", 5, 30, 15, step=1)
    
    cola, colb, colc = st.columns([1, 1, 1])
    with colb:
        calculate = st.button("Calculate Value-for-Money Rankings", use_container_width=True, type="primary")
    
    if calculate and quality_ratings:
        # Merge cost and quality data
        results = []
        for _, row in cost_df.iterrows():
            city = row['City']
            cost_index = row['cost_of_living_index']
            quality_index = quality_ratings.get(city, 100)
            
            # Calculate value score (Quality / Cost)
            # Normalize so Delhi (100/100) = 1.00
            value_score = quality_index / cost_index
            
            # Calculate surplus/deficit
            surplus = quality_index - cost_index
            
            results.append({
                'City': city,
                'Cost_Index': cost_index,
                'Quality_Index': quality_index,
                'Value_Score': value_score,
                'Surplus': surplus,
                'housing_index': row['housing_index'],
                'grocery_index': row['grocery_index'],
                'transport_index': row['transport_index']
            })
        
        results_df = pd.DataFrame(results).sort_values('Value_Score', ascending=False)
        
        # Display results
        st.markdown(f'<div class="section-header">Top {top_n} Best Value Cities</div>', unsafe_allow_html=True)
        
        for idx, row in results_df.head(top_n).iterrows():
            st.markdown('<div class="city-card">', unsafe_allow_html=True)
            
            # City name and rank
            rank = list(results_df.index).index(idx) + 1
            st.markdown(f'<h2 class="city-name">#{rank} {row["City"]}</h2>', unsafe_allow_html=True)
            
            # Determine value category
            value_score = row['Value_Score']
            if value_score >= 1.2:
                value_class = "excellent-value"
                value_text = "Excellent Value"
            elif value_score >= 1.05:
                value_class = "good-value"
                value_text = "Good Value"
            elif value_score >= 0.95:
                value_class = "fair-value"
                value_text = "Fair Value"
            else:
                value_class = "poor-value"
                value_text = "Poor Value"
            
            st.markdown(f'<span class="value-badge {value_class}">{value_text}</span>', unsafe_allow_html=True)
            
            # Metrics
            rc1, rc2, rc3, rc4 = st.columns(4)
            
            with rc1:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Value Score</div>
                    <div class="metric-value">{value_score:.2f}</div>
                    <div class="metric-delta">Quality / Cost Ratio</div>
                </div>
                """, unsafe_allow_html=True)
            
            with rc2:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Quality Index</div>
                    <div class="metric-value">{row['Quality_Index']:.0f}</div>
                    <div class="metric-delta">Your Rating</div>
                </div>
                """, unsafe_allow_html=True)
            
            with rc3:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Cost Index</div>
                    <div class="metric-value">{row['Cost_Index']:.1f}</div>
                    <div class="metric-delta">Actual Cost Data</div>
                </div>
                """, unsafe_allow_html=True)
            
            with rc4:
                surplus_color = "#155724" if row['Surplus'] > 0 else "#721C24"
                surplus_sign = "+" if row['Surplus'] > 0 else ""
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Surplus/Deficit</div>
                    <div class="metric-value" style="color: {surplus_color};">{surplus_sign}{row['Surplus']:.1f}</div>
                    <div class="metric-delta">Quality - Cost</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Explanation
            if value_score >= 1.1:
                explanation = f"🌟 {row['City']} offers excellent value! Your quality rating ({row['Quality_Index']:.0f}) significantly exceeds the cost ({row['Cost_Index']:.1f}), making it a smart choice."
            elif value_score >= 1.0:
                explanation = f"✓ {row['City']} provides good value. The quality of life matches or slightly exceeds the cost of living."
            else:
                explanation = f"⚠️ {row['City']} may be overpriced for your preferences. The cost ({row['Cost_Index']:.1f}) exceeds your quality rating ({row['Quality_Index']:.0f})."
            
            st.info(explanation)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show complete ranking
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("View Complete Rankings (All 50 Cities)"):
            display_df = results_df[['City', 'Value_Score', 'Quality_Index', 'Cost_Index', 'Surplus']].copy()
            display_df['Rank'] = range(1, len(display_df) + 1)
            display_df = display_df[['Rank', 'City', 'Value_Score', 'Quality_Index', 'Cost_Index', 'Surplus']]
            display_df.columns = ['Rank', 'City', 'Value Score', 'Quality Index', 'Cost Index', 'Surplus/Deficit']
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Download option
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="Download Complete Rankings (CSV)",
                data=csv,
                file_name="value_for_money_rankings.csv",
                mime="text/csv"
            )

except FileNotFoundError:
    st.error("Data file not found. Please run the analysis first.")
    st.code("cd src && python main.py", language="bash")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
