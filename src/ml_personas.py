"""
ML City Archetype Classifier and Price Anomaly Detector.
Uses K-Means clustering and standard statistical metrics to group cities into lifestyle archetypes.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class CityArchetypeClassifier:
    """
    Groups 50 Indian cities into ML archetypes and detects expense anomalies.
    """

    ARCHETYPE_LABELS = {
        0: {"name": "🚀 Tech & Metro Powerhouses", "description": "High-rent, vibrant IT hubs with premium dining & entertainment."},
        1: {"name": "🎓 Education & Family Hubs", "description": "Balanced cost structure with strong schooling and health facilities."},
        2: {"name": "🌿 Affordable Tier-2 Gems", "description": "Low overall living costs across housing, transport, and daily groceries."},
        3: {"name": "💼 High-Cost Metro Capitals", "description": "Peak living expenses driven by high housing rent and utilities."}
    }

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.feature_cols = [
            'housing_index', 'grocery_index', 'transport_index',
            'healthcare_index', 'electricity_index', 'restaurant_index',
            'movie_index', 'education_index'
        ]
        # Fill missing feature columns if any
        for col in self.feature_cols:
            if col not in self.df.columns:
                self.df[col] = 100.0

    def fit_clusters(self, n_clusters: int = 4) -> pd.DataFrame:
        """Runs K-Means clustering on standard-scaled expense features."""
        X = self.df[self.feature_cols].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.df['cluster'] = kmeans.fit_predict(X_scaled)
        
        # Assign archetype names
        self.df['archetype_name'] = self.df['cluster'].map(
            lambda c: self.ARCHETYPE_LABELS.get(c, {}).get('name', f'Cluster {c}')
        )
        self.df['archetype_description'] = self.df['cluster'].map(
            lambda c: self.ARCHETYPE_LABELS.get(c, {}).get('description', '')
        )
        return self.df

    def detect_anomalies(self, threshold_std: float = 1.5) -> List[Dict[str, Any]]:
        """
        Detects price anomalies per city (e.g. city where Healthcare is > 1.5 std dev below housing index).
        """
        anomalies = []
        for _, row in self.df.iterrows():
            city = row['City']
            overall = row.get('cost_of_living_index', 100)
            
            city_anomalies = []
            for col in self.feature_cols:
                val = row[col]
                # Compare column value against city overall index
                diff = val - overall
                col_name = col.replace('_index', '').capitalize()
                
                if diff < -25:
                    city_anomalies.append(f"Unusually affordable {col_name} ({val:.0f} vs overall {overall:.0f})")
                elif diff > 35:
                    city_anomalies.append(f"Unusually high {col_name} ({val:.0f} vs overall {overall:.0f})")
                    
            if city_anomalies:
                anomalies.append({
                    "city": city,
                    "overall_index": overall,
                    "anomalies": city_anomalies
                })
        return anomalies

    def get_archetype_summary(self) -> Dict[str, Any]:
        """Returns structured archetype clusters for API consumption."""
        if 'cluster' not in self.df.columns:
            self.fit_clusters()
            
        summary = {}
        for cluster_id in sorted(self.df['cluster'].unique()):
            cluster_df = self.df[self.df['cluster'] == cluster_id]
            info = self.ARCHETYPE_LABELS.get(cluster_id, {"name": f"Cluster {cluster_id}", "description": ""})
            
            cities_info = []
            for _, r in cluster_df.iterrows():
                cities_info.append({
                    "city": r['City'],
                    "cost_index": round(float(r.get('cost_of_living_index', 100)), 1),
                    "housing_index": round(float(r.get('housing_index', 100)), 1)
                })
                
            summary[info['name']] = {
                "description": info['description'],
                "city_count": len(cluster_df),
                "avg_cost_index": round(float(cluster_df['cost_of_living_index'].mean()), 1) if 'cost_of_living_index' in cluster_df else 100.0,
                "cities": cities_info
            }
        return summary
