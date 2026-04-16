import pandas as pd
import numpy as np

CATEGORIES = [
    "Housing",
    "Grocery",
    "Transport",
    "Healthcare",
    "Electricity",
    "Restaurant",
    "Movies",
]

CATEGORY_TO_COLUMN = {
    "Housing":     "housing_index",
    "Grocery":     "grocery_index",
    "Transport":   "transport_index",
    "Healthcare":  "healthcare_index",
    "Electricity": "electricity_index",
    "Restaurant":  "restaurant_index",
    "Movies":      "movie_index",
}


class InputCollector:
    def collect(self) -> dict[str, int]:
        preferences: dict[str, int] = {}
        for category in CATEGORIES:
            while True:
                raw = input(f"On a scale of 1 to 5, how much are you comfortable spending on {category}?")
                try:
                    value = int(raw)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                if value < 1 or value > 5:
                    print("Please enter a value between 1 and 5.")
                    continue
                preferences[category] = value
                break
        return preferences


class WeightCalculator:
    def compute_weights(self, preferences: dict[str, int]) -> dict[str, float]:
        """
        Converts preferences to weights based on deviation from neutral (3).
        - Preference 1-2: User wants LOW cost (negative weight for minimization)
        - Preference 3: Neutral (weight = 0)
        - Preference 4-5: User wants HIGH quality/cost (positive weight for maximization)
        
        Returns: {category_name: weight} where negative = minimize, positive = maximize
        """
        # Map preference to weight: 1→-2, 2→-1, 3→0, 4→1, 5→2
        weights = {c: preferences[c] - 3 for c in preferences}
        return weights


class ScoringEngine:
    CATEGORY_TO_COLUMN: dict[str, str] = CATEGORY_TO_COLUMN

    def __init__(self, data_path: str = "cost_index_results.csv"):
        self.data_path = data_path

    def score_cities(self, weights: dict[str, float]) -> pd.DataFrame:
        """
        Loads city index data, fills NaN with column medians, computes
        a preference-based score for each city where:
        - Negative weights (pref 1-2) favor LOW index values (cheap)
        - Positive weights (pref 4-5) favor HIGH index values (quality/expensive)
        - Zero weights (pref 3) are neutral
        
        Returns DataFrame sorted by best match (lowest score = best fit).
        """
        # --- Task 5.1: CSV loading with error handling ---
        try:
            df = pd.read_csv(self.data_path)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Data file '{self.data_path}' not found. "
                "Please run `python main.py` first to generate the cost index CSV."
            )

        for category, col in self.CATEGORY_TO_COLUMN.items():
            if col not in df.columns:
                raise KeyError(
                    f"Required column '{col}' (for category '{category}') is missing "
                    f"from '{self.data_path}'. The CSV may be outdated — "
                    "please run `python main.py` to regenerate it."
                )

        # --- Task 5.2: NaN fill, scoring, and sorting ---
        index_cols = list(self.CATEGORY_TO_COLUMN.values())

        # Fill NaN values with column median before scoring
        for col in index_cols:
            median = df[col].median()
            df[col] = df[col].fillna(median)

        # Normalize each index column to [0, 1] range for fair comparison
        normalized_df = df.copy()
        for col in index_cols:
            min_val = df[col].min()
            max_val = df[col].max()
            if max_val > min_val:
                normalized_df[col] = (df[col] - min_val) / (max_val - min_val)
            else:
                normalized_df[col] = 0.5  # All same value

        # Compute preference score
        # For each category:
        #   - If weight < 0 (pref 1-2): penalty increases with higher index (want cheap)
        #   - If weight > 0 (pref 4-5): penalty increases with lower index (want quality)
        #   - If weight = 0 (pref 3): no penalty
        df["preference_score"] = 0.0
        for cat, weight in weights.items():
            col = self.CATEGORY_TO_COLUMN[cat]
            normalized_index = normalized_df[col]
            
            if weight < 0:
                # Want cheap: penalize high index values
                df["preference_score"] += abs(weight) * normalized_index
            elif weight > 0:
                # Want quality: penalize low index values
                df["preference_score"] += weight * (1 - normalized_index)
            # weight == 0: no contribution

        # Sort ascending by preference_score (lower = better match)
        df = df.sort_values(
            by=["preference_score", "cost_of_living_index"],
            ascending=[True, True],
        ).reset_index(drop=True)

        return df


class RecommendationFormatter:
    def format(
        self,
        ranked_df: pd.DataFrame,
        weights: dict[str, float],
        preferences: dict[str, int],
        top_n: int = 3,
    ) -> str:
        """
        Generates ranked output string for the top `top_n` cities.
        Returns a multi-line string with exactly `top_n` rank lines, each in the form:
            "Rank {n}: {City} — {explanation}"
        The explanation references what the user prioritizes (low cost vs quality).
        """
        # Categorize preferences
        minimize_cats = [c for c in preferences if preferences[c] <= 2]  # Want cheap
        maximize_cats = [c for c in preferences if preferences[c] >= 4]  # Want quality
        
        lines = []
        for rank, (_, row) in enumerate(ranked_df.head(top_n).iterrows(), start=1):
            city = row["City"]
            
            explanation_parts = []
            
            # Mention categories user wants cheap
            if minimize_cats:
                cheap_parts = []
                for cat in minimize_cats[:2]:  # Top 2
                    col = CATEGORY_TO_COLUMN[cat]
                    val = row[col]
                    cheap_parts.append(f"{cat.lower()} ({val:.1f})")
                explanation_parts.append(f"Affordable {', '.join(cheap_parts)}")
            
            # Mention categories user wants quality
            if maximize_cats:
                quality_parts = []
                for cat in maximize_cats[:2]:  # Top 2
                    col = CATEGORY_TO_COLUMN[cat]
                    val = row[col]
                    quality_parts.append(f"{cat.lower()} ({val:.1f})")
                explanation_parts.append(f"Quality {', '.join(quality_parts)}")
            
            # If all neutral (all 3s) or mixed without strong preferences
            if not explanation_parts:
                overall_index = row["cost_of_living_index"]
                explanation = f"Balanced city with overall cost index {overall_index:.1f}"
            else:
                explanation = "; ".join(explanation_parts) + " match your preferences."
            
            lines.append(f"Rank {rank}: {city} — {explanation}")

        return "\n".join(lines)


class CityRecommender:
    def __init__(self, data_path: str = "cost_index_results.csv"):
        self.data_path = data_path

    def run(self) -> None:
        collector = InputCollector()
        preferences = collector.collect()

        calculator = WeightCalculator()
        weights = calculator.compute_weights(preferences)

        engine = ScoringEngine(data_path=self.data_path)
        ranked_df = engine.score_cities(weights)

        formatter = RecommendationFormatter()
        output = formatter.format(ranked_df, weights, preferences)

        print(output)
