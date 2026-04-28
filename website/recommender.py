import pandas as pd
import numpy as np

CATEGORIES = [
    "Housing",
    "Grocery",
    "Transport",
    "Healthcare",
    "Education",
    "Electricity",
    "Restaurant",
    "Movies",
]

CATEGORY_TO_COLUMN = {
    "Housing": "housing_index",
    "Grocery": "grocery_index",
    "Transport": "transport_index",
    "Healthcare": "healthcare_index",
    "Education": "education_index",
    "Electricity": "electricity_index",
    "Restaurant": "restaurant_index",
    "Movies": "movie_index",
}


class CityRecommender:
    """
    Smart city recommender that finds cities matching your cost priorities
    by creating a personalized cost of living index based on slider weights.
    """
    
    def __init__(self, data_path: str = "../outputs/reports/cost_index_results.csv"):
        self.data_path = data_path
        self.df = None
        
    def load_data(self):
        """Load city cost data"""
        try:
            self.df = pd.read_csv(self.data_path)
            
            # Verify required columns exist
            for col in CATEGORY_TO_COLUMN.values():
                if col not in self.df.columns:
                    raise KeyError(f"Column '{col}' not found in data")
            
            # Fill any missing values with median
            for col in CATEGORY_TO_COLUMN.values():
                if self.df[col].isna().any():
                    median_val = self.df[col].median()
                    self.df[col] = self.df[col].fillna(median_val)
                    
            return True
            
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Data file not found: {self.data_path}\n"
                "Please run: cd src && python main.py"
            )
    
    def find_cities(self, sliders: dict):
        """
        Calculates a personalized cost of living index based on 1-10 slider inputs.
        Returns the sorted DataFrame and the normalized customized weights.
        """
        if self.df is None:
            self.load_data()
            
        df = self.df.copy()
        
        base_weights = {
            "Housing": 0.3030,
            "Grocery": 0.3636,
            "Transport": 0.1091,
            "Healthcare": 0.0642,
            "Education": 0.0606,
            "Electricity": 0.0303,
            "Restaurant": 0.0485,
            "Movies": 0.0207
        }
        
        new_weights = {}
        for cat in CATEGORIES:
            val = sliders.get(cat, 5)
            if val <= 5:
                multiplier = 0.1 + (val - 1) * (0.9 / 4.0)
            else:
                multiplier = 1.0 + (val - 5) * (1.0 / 5.0)
                
            new_weights[cat] = base_weights[cat] * multiplier
            
        # Normalize weights
        total_weight = sum(new_weights.values())
        norm_weights = {cat: w / total_weight for cat, w in new_weights.items()}
        
        # Compute custom cost index relative to Delhi
        df['custom_index'] = 0.0
        for cat in CATEGORIES:
            col = CATEGORY_TO_COLUMN[cat]
            df['custom_index'] += df[col] * norm_weights[cat]
            
        # Sort affordable to expensive
        df = df.sort_values('custom_index').reset_index(drop=True)
        return df, norm_weights
        
    def get_recommendations(self, sliders: dict, top_n: int = 10) -> list:
        ranked_df, norm_weights = self.find_cities(sliders)
        
        recommendations = []
        for idx, row in ranked_df.head(top_n).iterrows():
            city_name = row['City']
            
            # Find the component with the biggest impact (weight * index) for this city
            contributions = {}
            for cat in CATEGORIES:
                col = CATEGORY_TO_COLUMN[cat]
                contributions[cat] = {
                    'index': row[col],
                    'weight': norm_weights[cat],
                    'impact': row[col] * norm_weights[cat]
                }
            
            # Sort by impact to see what's driving the cost in this city
            sorted_impact = sorted(contributions.items(), key=lambda x: x[1]['impact'], reverse=True)
            
            exp_lines = []
            exp_lines.append(f"Custom Cost Index: {row['custom_index']:.1f}")
            exp_lines.append("Top drivers:")
            for i in range(2):
                cat, data = sorted_impact[i]
                exp_lines.append(f"• {cat}: {data['index']:.0f} (Effective Weight: {data['weight']*100:.1f}%)")
                
            recommendations.append({
                'rank': idx + 1,
                'city': city_name,
                'custom_index': row['custom_index'],
                'overall_index': row['cost_of_living_index'],
                'explanation': "\n".join(exp_lines),
                'all_indices': {cat: row[CATEGORY_TO_COLUMN[cat]] for cat in CATEGORIES}
            })
            
        return recommendations, norm_weights
    
    def get_category_stats(self, city_name: str) -> dict:
        """Get detailed stats for a specific city"""
        if self.df is None:
            self.load_data()
        
        city_row = self.df[self.df['City'] == city_name]
        
        if city_row.empty:
            return None
        
        city_row = city_row.iloc[0]
        
        stats = {
            'city': city_name,
            'overall_index': city_row['cost_of_living_index'],
            'categories': {}
        }
        
        for cat in CATEGORIES:
            col = CATEGORY_TO_COLUMN[cat]
            index_val = city_row[col]
            
            # Calculate percentile rank
            percentile = (self.df[col] < index_val).sum() / len(self.df) * 100
            
            stats['categories'][cat] = {
                'index': index_val,
                'percentile': percentile,
                'rank': (self.df[col] < index_val).sum() + 1
            }
        
        return stats


def format_recommendations_text(recommendations: list) -> str:
    """Format recommendations as plain text"""
    lines = []
    
    for rec in recommendations:
        lines.append(f"\nRank {rec['rank']}: {rec['city']}")
        lines.append(f"Overall Cost Index: {rec['overall_index']:.1f} (Delhi = 100)")
        lines.append(f"Match Score: {rec['match_score']:.2f} (lower is better)")
        lines.append(f"\n{rec['explanation']}")
        lines.append("-" * 60)
    
    return "\n".join(lines)
