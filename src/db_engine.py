"""
Geospatial Database and Proximity Query Engine.
Executes spatial distance queries (Haversine formula & SQLite / PostGIS engine) across 50 Indian cities.
"""
import math
import sqlite3
import pandas as pd
from typing import List, Dict, Any, Optional

from website.city_coordinates import get_all_cities_with_coords


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate Great Circle distance between two points in km."""
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


class SpatialDatabaseEngine:
    """
    In-memory SQLite & Spatial Engine for city spatial proximity queries.
    """

    def __init__(self, cost_df: pd.DataFrame):
        self.cost_df = cost_df.copy()
        self.coords = get_all_cities_with_coords()
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self._init_db()

    def _init_db(self):
        """Build SQLite schema and populate city coordinates + cost metrics."""
        # Merge coordinates into cost DataFrame
        coords_df = pd.DataFrame([
            {"City": city, "latitude": data["lat"], "longitude": data["lon"]}
            for city, data in self.coords.items()
        ])
        
        merged = self.cost_df.merge(coords_df, on="City", how="left")
        merged['latitude'] = merged['latitude'].fillna(20.5937)
        merged['longitude'] = merged['longitude'].fillna(78.9629)

        # Write to SQLite
        merged.to_sql("cities_spatial", self.conn, if_exists="replace", index=False)

    def find_cities_nearby(
        self,
        center_city: str,
        radius_km: float = 300.0,
        max_cost_index: Optional[float] = None,
        min_savings_pct: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Finds cities within radius_km of center_city matching cost index constraints.
        """
        df = pd.read_sql("SELECT * FROM cities_spatial", self.conn)
        
        center_match = df[df['City'].str.lower() == center_city.lower()]
        if center_match.empty:
            return []
            
        center_row = center_match.iloc[0]
        c_lat, c_lon = center_row['latitude'], center_row['longitude']
        c_index = center_row.get('cost_of_living_index', 100)

        results = []
        for _, row in df.iterrows():
            if row['City'].lower() == center_city.lower():
                continue
                
            dist = haversine_distance(c_lat, c_lon, row['latitude'], row['longitude'])
            if dist <= radius_km:
                city_index = row.get('cost_of_living_index', 100)
                savings_pct = round(((c_index - city_index) / c_index) * 100, 1)

                # Filter by max cost index if specified
                if max_cost_index is not None and city_index > max_cost_index:
                    continue
                # Filter by min savings if specified
                if min_savings_pct is not None and savings_pct < min_savings_pct:
                    continue

                results.append({
                    "city": row['City'],
                    "distance_km": round(dist, 1),
                    "cost_of_living_index": float(city_index),
                    "base_city_index": float(c_index),
                    "savings_vs_base_pct": savings_pct,
                    "tier": row.get('Tier', None),
                    "state": row.get('State', None),
                    "housing_index": float(row.get('housing_index', 100)),
                    "latitude": float(row['latitude']),
                    "longitude": float(row['longitude'])
                })

        # Sort closest distance first
        results.sort(key=lambda x: x['distance_km'])
        return results
