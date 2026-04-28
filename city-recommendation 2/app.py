import streamlit as st
from recommender import (
    CATEGORIES,
    WeightCalculator,
    ScoringEngine,
    RecommendationFormatter,
)

# Title section (Requirement 7.1)
st.title("City Recommender")

# Instructions section (Requirement 7.2)
st.write(
    "Rate your spending comfort for each category on a scale of 1 to 5, "
    "where 1 means you prefer low cost and 5 means you prefer high quality/cost."
)

# Preference collection via sliders (Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 7.3)
preferences = {}
for category in CATEGORIES:
    preferences[category] = st.slider(
        f"{category} (1=low cost, 5=high quality)",
        min_value=1,
        max_value=5,
        value=3,
        step=1,
    )

# Get Recommendations button (Requirements 3.1, 7.4)
if st.button("Get Recommendations"):
    try:
        # Requirement 3.2: Instantiate WeightCalculator and compute weights
        calculator = WeightCalculator()
        weights = calculator.compute_weights(preferences)
        
        # Requirement 3.3: Instantiate ScoringEngine with default CSV path
        engine = ScoringEngine()
        
        # Requirement 3.4: Call score_cities() with weights
        ranked_df = engine.score_cities(weights)
        
        # Requirement 3.5: Instantiate RecommendationFormatter
        formatter = RecommendationFormatter()
        
        # Requirements 5.1, 5.2, 5.4: Call format() with parameters
        output = formatter.format(ranked_df, weights, preferences, top_n=3)
        
        # Display results
        st.subheader("Top 3 Recommendations")
        st.text(output)
        
    except (FileNotFoundError, KeyError) as e:
        st.error(str(e))