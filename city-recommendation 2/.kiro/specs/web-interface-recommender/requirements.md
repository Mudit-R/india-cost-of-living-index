# Requirements Document

## Introduction

This feature adds a local web interface to the existing city recommender CLI application. The web interface will allow users to input their spending preferences through a browser-based form and view city recommendations without using the command line. The interface will be built using Streamlit and will integrate with the existing recommender.py logic.

## Glossary

- **Web_Interface**: The Streamlit-based web application that provides browser access to the recommender
- **Preference_Form**: The input component containing 7 category sliders (Housing, Grocery, Transport, Healthcare, Electricity, Restaurant, Movies)
- **Recommendation_Display**: The output component showing the top 3 ranked city recommendations
- **Recommender_Engine**: The existing backend logic in recommender.py (InputCollector, WeightCalculator, ScoringEngine, RecommendationFormatter)
- **Category_Preference**: An integer value from 1 to 5 indicating user spending comfort level for a specific category
- **Local_Server**: The Streamlit development server running on localhost

## Requirements

### Requirement 1: Web Interface Initialization

**User Story:** As a user, I want to start a local web server, so that I can access the recommender through my browser

#### Acceptance Criteria

1. THE Web_Interface SHALL start a Local_Server on localhost port 8501
2. WHEN the Local_Server starts, THE Web_Interface SHALL display the Preference_Form
3. THE Web_Interface SHALL load cost_index_results.csv at startup
4. IF cost_index_results.csv is missing, THEN THE Web_Interface SHALL display an error message instructing the user to generate the CSV file

### Requirement 2: Preference Input Collection

**User Story:** As a user, I want to input my spending preferences through sliders, so that I can easily specify my comfort level for each category

#### Acceptance Criteria

1. THE Preference_Form SHALL display 7 sliders for Housing, Grocery, Transport, Healthcare, Electricity, Restaurant, and Movies
2. THE Preference_Form SHALL constrain each slider to integer values between 1 and 5 inclusive
3. THE Preference_Form SHALL set the default value of each slider to 3
4. THE Preference_Form SHALL display labels indicating that 1 means low spending comfort and 5 means high spending comfort
5. WHEN a user adjusts any slider, THE Web_Interface SHALL store the Category_Preference value

### Requirement 3: Recommendation Generation

**User Story:** As a user, I want to generate city recommendations based on my preferences, so that I can see which cities match my spending profile

#### Acceptance Criteria

1. THE Web_Interface SHALL display a "Get Recommendations" button below the Preference_Form
2. WHEN the user clicks "Get Recommendations", THE Web_Interface SHALL pass all Category_Preference values to the Recommender_Engine
3. THE Recommender_Engine SHALL compute weights using WeightCalculator
4. THE Recommender_Engine SHALL score cities using ScoringEngine
5. THE Recommender_Engine SHALL format results using RecommendationFormatter
6. THE Web_Interface SHALL display the formatted recommendations in the Recommendation_Display

### Requirement 4: Results Display

**User Story:** As a user, I want to see my top 3 city recommendations with explanations, so that I understand why each city was recommended

#### Acceptance Criteria

1. THE Recommendation_Display SHALL show exactly 3 ranked cities
2. THE Recommendation_Display SHALL show each city's rank number, name, and explanation
3. THE Recommendation_Display SHALL format each recommendation as "Rank {n}: {City} — {explanation}"
4. WHEN no recommendations have been generated yet, THE Recommendation_Display SHALL display a message prompting the user to click "Get Recommendations"

### Requirement 5: Code Integration

**User Story:** As a developer, I want to reuse existing recommender.py logic, so that I maintain consistency between CLI and web interfaces

#### Acceptance Criteria

1. THE Web_Interface SHALL import WeightCalculator, ScoringEngine, and RecommendationFormatter from recommender.py
2. THE Web_Interface SHALL NOT duplicate the scoring or formatting logic
3. THE Web_Interface SHALL use the same CATEGORIES list from recommender.py
4. THE Web_Interface SHALL pass preferences in the same dictionary format as InputCollector

### Requirement 6: Error Handling

**User Story:** As a user, I want clear error messages when something goes wrong, so that I know how to fix the problem

#### Acceptance Criteria

1. IF the CSV file is missing, THEN THE Web_Interface SHALL display the FileNotFoundError message from ScoringEngine
2. IF a required column is missing from the CSV, THEN THE Web_Interface SHALL display the KeyError message from ScoringEngine
3. WHEN an error occurs during recommendation generation, THE Web_Interface SHALL display the error message in the Recommendation_Display area

### Requirement 7: User Experience

**User Story:** As a user, I want a clean and intuitive interface, so that I can quickly get recommendations without confusion

#### Acceptance Criteria

1. THE Web_Interface SHALL display a title "City Cost of Living Recommender"
2. THE Web_Interface SHALL display instructions explaining the 1-5 scale before the sliders
3. THE Web_Interface SHALL group all 7 sliders together in the Preference_Form
4. THE Web_Interface SHALL display the Recommendation_Display below the "Get Recommendations" button
5. THE Web_Interface SHALL use clear visual separation between input and output sections
