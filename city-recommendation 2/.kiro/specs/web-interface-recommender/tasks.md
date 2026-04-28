# Implementation Plan: Web Interface Recommender

## Overview

This plan implements a Streamlit-based web interface (app.py) that provides browser access to the existing city recommender CLI application. The interface reuses backend classes from recommender.py (WeightCalculator, ScoringEngine, RecommendationFormatter) and replaces the CLI-based InputCollector with Streamlit UI components.

## Tasks

- [x] 1. Create app.py with basic Streamlit structure
  - Create new file app.py in project root
  - Import streamlit and required classes from recommender.py (CATEGORIES, WeightCalculator, ScoringEngine, RecommendationFormatter)
  - Add title and instructions section using st.title() and st.write()
  - _Requirements: 1.2, 7.1, 7.2_

- [ ] 2. Implement preference input collection with sliders
  - [x] 2.1 Create 7 category sliders for user input
    - Loop through CATEGORIES list to create st.slider() for each category
    - Configure sliders: min_value=1, max_value=5, value=3, step=1
    - Set labels to "{category} (1=low cost, 5=high quality)"
    - Store slider values in preferences dictionary
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 7.3_

- [ ] 3. Implement recommendation generation logic
  - [x] 3.1 Add "Get Recommendations" button
    - Create st.button("Get Recommendations")
    - _Requirements: 3.1, 7.4_
  
  - [x] 3.2 Wire backend classes on button click
    - Inside button click handler, instantiate WeightCalculator
    - Call compute_weights() with preferences dictionary
    - Instantiate ScoringEngine with default CSV path
    - Call score_cities() with weights
    - Instantiate RecommendationFormatter
    - Call format() with ranked DataFrame, weights, preferences, and top_n=3
    - _Requirements: 3.2, 3.3, 3.4, 3.5, 5.1, 5.2, 5.4_

- [ ] 4. Implement results display
  - [x] 4.1 Display formatted recommendations
    - Add st.subheader("Top 3 Recommendations")
    - Display formatted output string using st.text()
    - _Requirements: 3.6, 4.1, 4.2, 4.3, 7.4, 7.5_
  
  - [x] 4.2 Add error handling for CSV and data issues
    - Wrap recommendation logic in try-except block
    - Catch FileNotFoundError and KeyError exceptions
    - Display error messages using st.error()
    - _Requirements: 1.4, 6.1, 6.2, 6.3_

- [ ]* 5. Write unit tests for app.py integration
  - Test import verification (CATEGORIES, WeightCalculator, ScoringEngine, RecommendationFormatter)
  - Test preferences dictionary construction from slider values
  - Test error handling with mocked exceptions (FileNotFoundError, KeyError)
  - Test end-to-end flow with valid preferences and existing CSV
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 6. Checkpoint - Verify web interface functionality
  - Run streamlit run app.py manually to test the interface
  - Verify all 7 sliders display correctly with proper labels
  - Test recommendation generation with various preference combinations
  - Test error scenarios (missing CSV, missing columns)
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- The web interface runs on localhost:8501 by default (Streamlit's default port)
- No modifications to recommender.py are required
- Manual testing via `streamlit run app.py` is recommended after implementation
- Each task references specific requirements for traceability
