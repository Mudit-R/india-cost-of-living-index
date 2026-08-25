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
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Helvetica+Neue:wght@400;500;700&display=swap');
    
    /* Global CSS variables to override Streamlit internal themes */
    :root {
        --text-color: #1E1B18 !important;
        --background-color: #F9F3EA !important;
        --secondary-background-color: #F4EBE0 !important;
        --primary-color: #21201D !important;
    }
    
    /* Universal typography and color overrides */
    html, body, [class*="css"], .stApp, .main, p, span, label, li, h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #1E1B18 !important;
        -webkit-font-smoothing: antialiased;
    }
    
    /* Hide Streamlit default header, deploy button & footer */
    #MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* App background */
    .stApp {
        background-color: #F9F3EA !important;
    }
    
    .main {
        background: transparent !important;
        padding: 2rem 1rem !important;
    }
    
    /* Header section */
    .header-container {
        background: transparent;
        padding: 2rem 0 1.5rem 0;
        margin-bottom: 1.5rem;
    }
    
    .main-title {
        font-family: 'Playfair Display', Georgia, serif !important;
        font-size: 4.2rem !important;
        font-weight: 600 !important;
        color: #1E1B18 !important;
        margin: 0 !important;
        line-height: 1.1 !important;
        letter-spacing: -1.5px !important;
    }
    
    .subtitle {
        font-size: 0.95rem !important;
        color: #726E68 !important;
        margin-top: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Playfair Display', Georgia, serif !important;
        font-size: 2.2rem !important;
        font-weight: 600 !important;
        color: #1E1B18 !important;
        margin: 2.5rem 0 1.5rem 0 !important;
        padding-bottom: 0.8rem !important;
        border-bottom: 2px solid #1E1B18 !important;
        letter-spacing: -0.5px !important;
    }
    
    /* Info box */
    .info-box {
        background: #F4EBE0 !important;
        border: 1px solid #E5DBCD !important;
        border-radius: 8px !important;
        padding: 1.8rem !important;
        margin: 0.5rem 0 !important;
    }
    
    .info-title {
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        color: #726E68 !important;
        margin-bottom: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }
    
    .info-text {
        font-size: 1rem !important;
        color: #2C2926 !important;
        line-height: 1.6 !important;
    }
    
    /* Streamlit Expander styling */
    [data-testid="stExpander"] {
        background-color: #F4EBE0 !important;
        border: 1px solid #E5DBCD !important;
        border-radius: 8px !important;
        margin: 1rem 0 !important;
        box-shadow: none !important;
    }
    
    [data-testid="stExpander"] details {
        background-color: #F4EBE0 !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stExpander"] summary {
        background-color: #F4EBE0 !important;
        border-radius: 8px !important;
        color: #1E1B18 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.8rem 1.2rem !important;
    }
    
    [data-testid="stExpander"] summary:hover {
        background-color: #EFE4D6 !important;
        color: #1E1B18 !important;
    }
    
    [data-testid="stExpander"] summary svg, [data-testid="stExpanderToggleIcon"] {
        color: #1E1B18 !important;
        fill: #1E1B18 !important;
    }
    
    [data-testid="stExpanderDetails"] {
        background-color: #F4EBE0 !important;
        border-top: 1px solid #E5DBCD !important;
        padding: 1.2rem !important;
    }
    
    /* Streamlit Sliders */
    [data-testid="stSlider"] {
        padding: 0.5rem 0 !important;
    }
    
    [data-testid="stSlider"] label, [data-testid="stWidgetLabel"] p {
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        color: #1E1B18 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    /* Slider Track & Thumb */
    [data-testid="stSlider"] [data-baseweb="slider"] {
        background: transparent !important;
    }
    
    /* Track highlight */
    div[data-testid="stSlider"] div[data-testid="stSliderTickBar"] {
        background: #E5DBCD !important;
    }
    
    /* Slider value label */
    [data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: #1E1B18 !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #1E1B18 !important;
        color: #FAF4EB !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.9rem 2.2rem !important;
        border-radius: 4px !important;
        font-size: 0.95rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        box-shadow: 0 4px 12px rgba(30, 27, 24, 0.15) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #3A3835 !important;
        color: #FFFFFF !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(30, 27, 24, 0.25) !important;
    }
    
    /* City result cards */
    .city-card {
        background: #FFFFFF !important;
        border: 1px solid #E5DBCD !important;
        border-radius: 12px !important;
        padding: 2.2rem 2.5rem !important;
        margin-bottom: 2rem !important;
        box-shadow: 0 4px 16px rgba(30, 27, 24, 0.04) !important;
    }
    
    .rank-badge {
        display: inline-block;
        background: #F4EBE0 !important;
        color: #726E68 !important;
        padding: 0.3rem 0.8rem !important;
        border-radius: 4px !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
        margin-bottom: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        border: 1px solid #E5DBCD !important;
    }
    
    .city-name {
        font-family: 'Playfair Display', Georgia, serif !important;
        font-size: 3.2rem !important;
        font-weight: 600 !important;
        color: #1E1B18 !important;
        margin: 0.2rem 0 1rem 0 !important;
        letter-spacing: -1px !important;
    }
    
    .city-explanation {
        font-size: 1.05rem !important;
        color: #383431 !important;
        line-height: 1.65 !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Metric boxes inside cards */
    .metric-container {
        background: #F9F3EA !important;
        padding: 1.4rem 1.8rem !important;
        border-radius: 8px !important;
        text-align: left !important;
        border: 1px solid #E5DBCD !important;
        height: 100% !important;
    }
    
    .metric-label {
        font-size: 0.8rem !important;
        color: #726E68 !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        margin-bottom: 0.5rem !important;
    }
    
    .metric-value {
        font-family: 'Playfair Display', Georgia, serif !important;
        font-size: 3.2rem !important;
        font-weight: 600 !important;
        color: #1E1B18 !important;
        letter-spacing: -1.5px !important;
        line-height: 1 !important;
    }
    
    .metric-delta {
        font-size: 0.85rem !important;
        color: #726E68 !important;
        margin-top: 0.6rem !important;
        font-weight: 500 !important;
    }
    
    /* Streamlit DataFrame & Table styling overrides */
    [data-testid="stDataFrame"], [data-testid="stTable"], .dataframe {
        background-color: #FFFFFF !important;
        border: 1px solid #E5DBCD !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        color: #1E1B18 !important;
    }
    
    /* Table headers and cells */
    table, th, td {
        color: #1E1B18 !important;
        border-color: #E5DBCD !important;
    }
    
    th {
        background-color: #F4EBE0 !important;
        font-weight: 700 !important;
    }
    
    /* Slider numbers and tick labels */
    div[data-testid="stSlider"] span {
        color: #1E1B18 !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="stSlider"] p {
        color: #1E1B18 !important;
    }
    
    /* Tooltip icons */
    [data-testid="stTooltipIcon"] svg {
        fill: #726E68 !important;
        color: #726E68 !important;
    }
    
    /* Help tooltips */
    div[data-baseweb="tooltip"] {
        background-color: #1E1B18 !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
    }
    
    /* Map Container */
    .element-container:has(iframe) {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #E5DBCD !important;
        box-shadow: 0 4px 16px rgba(30, 27, 24, 0.04) !important;
    }
    
    /* Footer */
    .footer {
        text-align: left;
        color: #1E1B18 !important;
        padding: 3rem 0 2rem 0;
        margin-top: 4rem;
        font-size: 0.95rem;
        background: transparent;
        border-top: 2px solid #1E1B18;
    }
    
    .footer-title {
        font-family: 'Playfair Display', Georgia, serif !important;
        font-weight: 600 !important;
        color: #1E1B18 !important;
        margin-bottom: 0.8rem;
        font-size: 1.6rem;
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
