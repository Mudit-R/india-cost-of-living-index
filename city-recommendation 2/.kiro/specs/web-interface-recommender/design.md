# Design Document: Web Interface Recommender

## Overview

This design specifies a Streamlit-based web interface for the existing city recommender CLI application. The web interface provides a browser-based form for collecting user preferences and displays city recommendations without requiring command-line interaction.

The design reuses the core recommendation logic from `recommender.py` (WeightCalculator, ScoringEngine, RecommendationFormatter) while replacing the CLI-based InputCollector with Streamlit UI components. The interface runs as a local development server on port 8501 and maintains full compatibility with the existing backend logic.

### Key Design Principles

1. **Reuse over Duplication**: Leverage existing recommender.py classes rather than reimplementing logic
2. **Separation of Concerns**: Keep UI layer (Streamlit) separate from business logic (recommender.py)
3. **Error Transparency**: Surface backend errors (missing CSV, invalid data) directly to users
4. **Simplicity**: Single-page application with minimal state management

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Web Interface                  │
│                          (app.py)                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           UI Layer (Streamlit Components)            │   │
│  │                                                       │   │
│  │  • Title & Instructions                              │   │
│  │  • 7 Category Sliders (1-5 scale)                    │   │
│  │  • "Get Recommendations" Button                      │   │
│  │  • Results Display Area                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Integration Layer (app.py logic)             │   │
│  │                                                       │   │
│  │  • Collect slider values → preferences dict          │   │
│  │  • Call WeightCalculator.compute_weights()           │   │
│  │  • Call ScoringEngine.score_cities()                 │   │
│  │  • Call RecommendationFormatter.format()             │   │
│  │  • Display results or errors                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
└──────────────────────────┼───────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend Logic (recommender.py)                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  • WeightCalculator: preferences → weights                   │
│  • ScoringEngine: weights → ranked DataFrame                 │
│  • RecommendationFormatter: DataFrame → formatted string     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                 cost_index_results.csv
```

### Component Interaction Flow

1. **Startup**: Streamlit loads app.py, displays UI components
2. **User Input**: User adjusts 7 sliders (Housing, Grocery, Transport, Healthcare, Electricity, Restaurant, Movies)
3. **Submission**: User clicks "Get Recommendations" button
4. **Processing**:
   - Collect slider values into preferences dictionary: `{category: value}`
   - Pass to WeightCalculator → get weights dictionary
   - Pass weights to ScoringEngine → get ranked DataFrame
   - Pass DataFrame to RecommendationFormatter → get formatted string
5. **Display**: Show formatted recommendations or error message

### State Management

Streamlit's reactive model handles state automatically:
- Slider values are stored in Streamlit's session state
- Button click triggers rerun with updated values
- No manual state management required

## Components and Interfaces

### app.py (New File)

The main Streamlit application file containing:

#### UI Components

1. **Title Section**
   - `st.title("City Cost of Living Recommender")`
   - Displays application name

2. **Instructions Section**
   - `st.write()` with explanation of 1-5 scale
   - Text: "Rate your spending comfort for each category (1 = prefer low cost, 5 = prefer high quality/cost)"

3. **Preference Form**
   - 7 `st.slider()` widgets, one per category
   - Configuration:
     - `min_value=1, max_value=5, value=3, step=1`
     - `label=f"{category} (1=low cost, 5=high quality)"`
   - Returns: Dictionary `{category: slider_value}`

4. **Submit Button**
   - `st.button("Get Recommendations")`
   - Triggers recommendation generation

5. **Results Display**
   - `st.subheader("Top 3 Recommendations")`
   - `st.text()` or `st.markdown()` for formatted output
   - Shows either recommendations or error messages

#### Integration Logic

```python
# Pseudo-code structure
import streamlit as st
from recommender import (
    CATEGORIES,
    WeightCalculator,
    ScoringEngine,
    RecommendationFormatter
)

# Title and instructions
st.title("City Cost of Living Recommender")
st.write("Rate your spending comfort...")

# Collect preferences via sliders
preferences = {}
for category in CATEGORIES:
    preferences[category] = st.slider(
        f"{category} (1=low cost, 5=high quality)",
        min_value=1,
        max_value=5,
        value=3,
        step=1
    )

# Generate recommendations on button click
if st.button("Get Recommendations"):
    try:
        # Use existing backend classes
        calculator = WeightCalculator()
        weights = calculator.compute_weights(preferences)
        
        engine = ScoringEngine()
        ranked_df = engine.score_cities(weights)
        
        formatter = RecommendationFormatter()
        output = formatter.format(ranked_df, weights, preferences)
        
        # Display results
        st.subheader("Top 3 Recommendations")
        st.text(output)
        
    except (FileNotFoundError, KeyError) as e:
        st.error(str(e))
```

### Integration with recommender.py

The web interface imports and uses these existing classes:

1. **CATEGORIES** (list)
   - Used to generate slider labels dynamically
   - Ensures consistency with backend

2. **WeightCalculator**
   - Input: `preferences: dict[str, int]`
   - Output: `weights: dict[str, float]`
   - No modifications needed

3. **ScoringEngine**
   - Input: `weights: dict[str, float]`
   - Output: `ranked_df: pd.DataFrame`
   - Uses existing CSV loading and error handling
   - No modifications needed

4. **RecommendationFormatter**
   - Input: `ranked_df, weights, preferences, top_n=3`
   - Output: `formatted_string: str`
   - No modifications needed

### Classes NOT Used

- **InputCollector**: Replaced by Streamlit sliders
- **CityRecommender**: Orchestration logic replaced by app.py button handler

## Data Models

### Preferences Dictionary

```python
{
    "Housing": int,      # 1-5
    "Grocery": int,      # 1-5
    "Transport": int,    # 1-5
    "Healthcare": int,   # 1-5
    "Electricity": int,  # 1-5
    "Restaurant": int,   # 1-5
    "Movies": int        # 1-5
}
```

- Keys: Category names from CATEGORIES list
- Values: Integer slider values (1-5 inclusive)
- Same format as InputCollector output

### Weights Dictionary

```python
{
    "Housing": float,      # -2 to 2
    "Grocery": float,      # -2 to 2
    "Transport": float,    # -2 to 2
    "Healthcare": float,   # -2 to 2
    "Electricity": float,  # -2 to 2
    "Restaurant": float,   # -2 to 2
    "Movies": float        # -2 to 2
}
```

- Computed by WeightCalculator
- Negative values: prefer low cost
- Positive values: prefer high quality/cost
- Zero: neutral

### Ranked DataFrame

Pandas DataFrame with columns:
- `City`: string
- `cost_of_living_index`: float
- `housing_index`, `grocery_index`, etc.: float
- `preference_score`: float (lower = better match)

Sorted by `preference_score` ascending.

### Formatted Output

Multi-line string:
```
Rank 1: {City} — {explanation}
Rank 2: {City} — {explanation}
Rank 3: {City} — {explanation}
```

## Error Handling

### Error Sources and Handling

1. **Missing CSV File**
   - Source: `ScoringEngine.__init__()` or `score_cities()`
   - Exception: `FileNotFoundError`
   - Message: "Data file 'cost_index_results.csv' not found. Please run `python main.py` first..."
   - Display: `st.error(str(e))`

2. **Missing CSV Columns**
   - Source: `ScoringEngine.score_cities()`
   - Exception: `KeyError`
   - Message: "Required column '{col}' (for category '{category}') is missing..."
   - Display: `st.error(str(e))`

3. **Invalid Slider Values**
   - Prevention: Streamlit slider constraints (`min_value=1, max_value=5, step=1`)
   - No runtime validation needed

### Error Display Strategy

```python
try:
    # Recommendation generation logic
    ...
except (FileNotFoundError, KeyError) as e:
    st.error(str(e))
except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")
```

- Use `st.error()` for error messages (red background)
- Display in the results area (below button)
- Preserve error messages from backend (don't modify)

## Testing Strategy

### Unit Tests

Since this feature is primarily UI integration with existing tested backend logic, testing focuses on:

1. **Import Verification**
   - Test: Verify app.py can import CATEGORIES, WeightCalculator, ScoringEngine, RecommendationFormatter
   - Purpose: Ensure integration layer is correctly wired

2. **Preferences Dictionary Construction**
   - Test: Given slider values, verify preferences dict has correct structure
   - Example: `{"Housing": 3, "Grocery": 2, ...}` with all 7 categories

3. **Error Handling**
   - Test: Verify FileNotFoundError is caught when CSV missing
   - Test: Verify KeyError is caught when CSV columns missing
   - Mock ScoringEngine to raise exceptions

4. **End-to-End Flow**
   - Test: Given valid preferences, verify WeightCalculator → ScoringEngine → RecommendationFormatter chain produces output
   - Use existing CSV file
   - Verify output is non-empty string with 3 ranks

### Manual Testing

1. **UI Rendering**
   - Verify title displays correctly
   - Verify 7 sliders appear with correct labels
   - Verify button is clickable
   - Verify results area updates after button click

2. **Slider Interaction**
   - Adjust each slider, verify value changes
   - Verify default value is 3
   - Verify min/max constraints (1-5)

3. **Recommendation Generation**
   - Set all sliders to 1 (prefer low cost), verify results
   - Set all sliders to 5 (prefer high quality), verify results
   - Set mixed values, verify results change

4. **Error Scenarios**
   - Rename CSV file, verify error message displays
   - Modify CSV to remove column, verify error message displays

### Testing Tools

- **pytest**: For unit tests
- **streamlit run**: For manual UI testing
- **Mock/patch**: For simulating errors in unit tests

No property-based testing is applicable for this feature because:
- The feature is primarily UI integration code
- The core logic (WeightCalculator, ScoringEngine, RecommendationFormatter) is already implemented and tested
- UI rendering and Streamlit component behavior cannot be meaningfully tested with property-based approaches
- Manual testing and example-based unit tests are more appropriate for verifying UI integration

