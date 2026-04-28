import streamlit as st
import pandas as pd
import sys
import os
import folium
from streamlit_folium import st_folium

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from website.recommender import CityRecommender, CATEGORIES
from website.city_coordinates import get_coordinates, get_all_cities_with_coords

# Determine correct data path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
data_path = os.path.join(parent_dir, 'outputs', 'reports', 'cost_index_results.csv')

# Page configuration
st.set_page_config(
    page_title="City Cost Recommender",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Import Next Chapter fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Helvetica+Neue:wght@400;500;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Streamlit app background overrides */
    .stApp {
        background-color: #F9F3EA;
    }
    
    /* Main container */
    .main {
        background: transparent;
        padding: 2rem 1rem;
    }
    
    /* Header section */
    .header-container {
        background: transparent;
        padding: 2rem 0;
        border-radius: 0;
        margin-bottom: 2rem;
        border: none;
    }
    
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
    
    /* Info box */
    .info-box {
        background: #F4EBE0;
        border: 1px solid #E5DBCD;
        border-radius: 8px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    
    .info-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: #726E68;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .info-text {
        font-size: 1.05rem;
        color: #4A4845;
        line-height: 1.6;
    }
    
    /* Section headers */
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
    
    /* Priority cards */
    .priority-card {
        background: transparent;
        padding: 1.5rem 0;
        border-radius: 0;
        border: none;
        border-top: 1px solid #E5DBCD;
        margin-bottom: 1rem;
    }
    
    /* City result cards */
    .city-card {
        background: transparent;
        padding: 3rem 0;
        border-radius: 0;
        border: none;
        border-top: 1px solid #1E1B18;
        margin-bottom: 1rem;
        transition: none;
    }
    
    .city-card:hover {
        /* No hover transform */
    }
    
    .rank-badge {
        display: inline-block;
        background: transparent;
        color: #726E68;
        padding: 0;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .city-name {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 500;
        color: #1E1B18;
        margin: 0.5rem 0;
        letter-spacing: -1px;
    }
    
    .city-explanation {
        font-size: 1.05rem;
        color: #4A4845;
        line-height: 1.6;
        margin: 1rem 0;
    }
    
    /* Metric boxes */
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
    
    .metric-delta {
        font-size: 0.9rem;
        color: #726E68;
        margin-top: 1rem;
        font-weight: 400;
    }
    
    /* Button styling */
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
        transition: background-color 0.2s !important;
    }
    
    .stButton>button:hover {
        background: #3A3835 !important;
        color: #FAF4EB !important;
    }
    
    /* Slider styling */
    .stSlider label {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 600;
        color: #1E1B18;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #F4EBE0;
        border-radius: 8px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 600;
        color: #1E1B18;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 0.9rem;
        border: 1px solid #E5DBCD;
    }
    
    /* Table styling */
    .dataframe {
        font-size: 1rem;
        border-collapse: collapse;
    }
    
    /* Priority summary boxes */
    .priority-summary {
        background: #F4EBE0;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E5DBCD;
    }
    
    .priority-summary h4 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #726E68;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #E5DBCD;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .priority-item {
        color: #1E1B18;
        font-size: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: left;
        color: #1E1B18;
        padding: 3rem 0;
        margin-top: 5rem;
        font-size: 1rem;
        background: transparent;
        border-top: 1px solid #1E1B18;
    }
    
    .footer-title {
        font-family: 'Playfair Display', serif;
        font-weight: 500;
        color: #1E1B18;
        margin-bottom: 1rem;
        font-size: 1.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 class="main-title">City Cost Recommender</h1>
    <p class="subtitle">Find Indian cities that match your custom priorities by shaping your own Cost of Living Index.</p>
</div>
""", unsafe_allow_html=True)

# Information section
with st.expander("How This Tool Works"):
    st.markdown("""
    <div class="info-box">
        <div class="info-title">About the Custom Weights</div>
        <div class="info-text">
            This tool scales the standard household component weights based on your preferences to create a personalized Index.
            <br><br>
            <strong>For each category, use the slider to set its weight multiplier (1 to 10):</strong>
            <ul>
                <li><strong>1 : </strong> 0.1x weight (unimportant)</li>
                <li><strong>5 : </strong> 1.0x weight (normal, baseline weights)</li>
                <li><strong>10 : </strong> 2.0x weight (very important)</li>
            </ul>
            <br>
            <strong>Categories analyzed:</strong> Housing, Grocery, Transport, Healthcare, Education, 
            Electricity, Restaurant, Movies.
            <br><br>
            <strong>Index scale:</strong> Delhi = 100 (baseline). Lower values = more affordable.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-header">Set Component Weights</div>', unsafe_allow_html=True)

# Create columns for better slider layout
col1, col2 = st.columns(2)

sliders = {}

with col1:
    sliders["Housing"] = st.slider("Housing Weight", min_value=1, max_value=10, value=5, help="Property prices and rent costs")
    sliders["Grocery"] = st.slider("Grocery Weight", min_value=1, max_value=10, value=5, help="Daily food and grocery shopping")
    sliders["Transport"] = st.slider("Transport Weight", min_value=1, max_value=10, value=5, help="Uber/taxi and fuel costs")
    sliders["Healthcare"] = st.slider("Healthcare Weight", min_value=1, max_value=10, value=5, help="Doctor consultation fees")

with col2:
    sliders["Education"] = st.slider("Education Weight", min_value=1, max_value=10, value=5, help="Tutor and coaching fees")
    sliders["Electricity"] = st.slider("Electricity Weight", min_value=1, max_value=10, value=5, help="Utility and electricity costs")
    sliders["Restaurant"] = st.slider("Restaurant Weight", min_value=1, max_value=10, value=5, help="Dining out costs")
    sliders["Movies"] = st.slider("Movies Weight", min_value=1, max_value=10, value=5, help="Entertainment and movie tickets")

# Number of results
st.markdown("<br>", unsafe_allow_html=True)
top_n = st.slider("Number of recommendations:", min_value=3, max_value=20, value=10, step=1)

st.markdown("<br>", unsafe_allow_html=True)

# Get Recommendations button
cola, colb, colc = st.columns([1, 1, 1])
with colb:
    get_recommendations = st.button("Calculate My Index", use_container_width=True, type="primary")

if get_recommendations:
    try:
        with st.spinner("Analyzing cities with your custom index..."):
            recommender = CityRecommender(data_path=data_path)
            recommendations, norm_weights = recommender.get_recommendations(sliders, top_n=top_n)
        
        # Display priority summary
        st.markdown('<div class="section-header">Your Custom Index Weights</div>', unsafe_allow_html=True)
        
        # Format weights nicely in a table
        weight_df = pd.DataFrame([
            {"Category": cat, "New Weight": f"{w*100:.1f}%"}
            for cat, w in norm_weights.items()
        ]).sort_values(by="New Weight", ascending=False)
        
        st.dataframe(weight_df, use_container_width=True, hide_index=True)
        
        # CREATE INTERACTIVE MAP
        st.markdown('<div class="section-header">Top 5 Cities on Map</div>', unsafe_allow_html=True)
        
        try:
            # Create map centered on India
            m = folium.Map(
                location=[20.5937, 78.9629],  # Center of India
                zoom_start=5,
                tiles='OpenStreetMap'
            )
            
            # Add top 5 cities to map
            cities_added = 0
            for i, rec in enumerate(recommendations[:5], 1):
                city_name = rec['city']
                coords = get_coordinates(city_name)
                
                if coords:
                    cities_added += 1
                    # Color based on rank - using valid folium colors
                    colors = ['darkgreen', 'green', 'lightgreen', 'orange', 'red']
                    color = colors[i-1] if i <= 5 else 'gray'
                    
                    # Create popup with city info
                    popup_html = f"""
                    <div style="font-family: Arial; width: 200px;">
                        <h4 style="margin: 0; color: #1E1B18;">#{i} {city_name}</h4>
                        <hr style="margin: 5px 0;">
                        <p style="margin: 5px 0;"><b>Custom Index:</b> {rec['custom_index']:.1f}</p>
                        <p style="margin: 5px 0;"><b>Baseline Index:</b> {rec['overall_index']:.1f}</p>
                    </div>
                    """
                    
                    # Add marker
                    folium.Marker(
                        location=[coords['lat'], coords['lon']],
                        popup=folium.Popup(popup_html, max_width=250),
                        tooltip=f"#{i} {city_name}",
                        icon=folium.Icon(color=color, icon='info-sign')
                    ).add_to(m)
                    
                    # Add circle marker for emphasis
                    folium.CircleMarker(
                        location=[coords['lat'], coords['lon']],
                        radius=15 - (i * 2),  # Larger for top ranks
                        color=color,
                        fill=True,
                        fillColor=color,
                        fillOpacity=0.3,
                        weight=2
                    ).add_to(m)
            
            # Display map
            if cities_added > 0:
                st_folium(m, width=1200, height=500, key="city_map", returned_objects=[])
            else:
                st.warning("No city coordinates found for mapping")
                
        except Exception as e:
            st.error(f"Map error: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display results
        st.markdown(f'<div class="section-header">Top {len(recommendations)} Recommended Cities</div>', unsafe_allow_html=True)
        
        for rec in recommendations:
            st.markdown('<div class="city-card">', unsafe_allow_html=True)
            
            # Rank badge and city name
            st.markdown(f'<span class="rank-badge">Rank {rec["rank"]}</span>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="city-name">{rec["city"]}</h2>', unsafe_allow_html=True)
            
            # Metrics row
            rc1, rc2, rc3 = st.columns([2, 1, 1])
            
            with rc1:
                # Convert explanation safely (split lines and bullet points)
                exp_text = "<br>".join(rec["explanation"].split("\n"))
                st.markdown(f'<div class="city-explanation">{exp_text}</div>', unsafe_allow_html=True)
            
            with rc2:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Custom Index</div>
                    <div class="metric-value">{rec['custom_index']:.1f}</div>
                    <div class="metric-delta">Your Personal Weighting</div>
                </div>
                """, unsafe_allow_html=True)
            
            with rc3:
                delta_val = rec['overall_index'] - 100
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Baseline Index</div>
                    <div class="metric-value">{rec['overall_index']:.1f}</div>
                    <div class="metric-delta">Default National Weights</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Show detailed breakdown
            with st.expander(f"View raw indices for {rec['city']}"):
                indices_df = pd.DataFrame([
                    {"Category": cat, "Cost Index vs Delhi": f"{rec['all_indices'][cat]:.1f}"}
                    for cat in CATEGORIES
                ])
                st.dataframe(indices_df, use_container_width=True, hide_index=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show all cities option
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("View complete ranking of all 50 cities"):
            all_cities, _ = recommender.find_cities(sliders)
            display_df = all_cities[['City', 'custom_index', 'cost_of_living_index']].copy()
            display_df.columns = ['City', 'Custom Index', 'Baseline Index']
            display_df['Rank'] = range(1, len(display_df) + 1)
            display_df = display_df[['Rank', 'City', 'Custom Index', 'Baseline Index']]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        
    except FileNotFoundError as e:
        st.error("Data file not found. Please run the analysis first.")
        st.code("cd src && python main.py", language="bash")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check that the data file exists and is properly formatted.")

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-title">Cost of Living Index Analysis</div>
    <p>50 Indian Cities | 8 Cost Categories | Delhi Baseline = 100</p>
    <p style="margin-top: 0.5rem; font-size: 0.85rem;">
        Data includes: Housing, Grocery, Transport, Healthcare, Education, Electricity, Restaurant, Movies.
    </p>
</div>
""", unsafe_allow_html=True)
