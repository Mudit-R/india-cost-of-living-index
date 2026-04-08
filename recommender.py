#!/usr/bin/env python3
"""
City Recommender — suggests best Indian cities based on user preferences.
Usage: python -c "from recommender import CityRecommender; CityRecommender().run()"
"""

import pandas as pd
import numpy as np


class CityRecommender:
    def __init__(self, data_file='cost_index_results.csv'):
        self.df = pd.read_csv(data_file)
        self.components = [
            ('housing_index',     'Housing'),
            ('grocery_index',     'Grocery'),
            ('transport_index',   'Transport'),
            ('healthcare_index',  'Healthcare'),
            ('electricity_index', 'Electricity'),
            ('restaurant_index',  'Restaurants'),
            ('movie_index',       'Movies'),
        ]

    def _ask(self, prompt, valid=None, default=None):
        while True:
            val = input(prompt).strip()
            if val == '' and default is not None:
                return default
            if valid is None:
                return val
            if val.lower() in [v.lower() for v in valid]:
                return val.lower()
            print(f"  Please enter one of: {', '.join(valid)}")

    def run(self):
        print("\n" + "="*60)
        print("  INDIA CITY RECOMMENDER (Delhi = 100)")
        print("="*60)

        # 1. Budget
        print("\nWhat's your cost-of-living budget?")
        print("  1. Tight    (index < 75)")
        print("  2. Moderate (index 75–100)")
        print("  3. Flexible (index > 100)")
        budget = self._ask("Choose [1/2/3]: ", valid=['1','2','3'], default='2')
        budget_ranges = {'1': (0, 75), '2': (75, 100), '3': (100, 999)}
        lo, hi = budget_ranges[budget]

        # 2. Priority component
        print("\nWhich cost factor matters most to you?")
        for i, (_, label) in enumerate(self.components, 1):
            print(f"  {i}. {label}")
        print("  8. No preference")
        choice = self._ask("Choose [1-8]: ",
                           valid=[str(i) for i in range(1, 9)], default='8')

        # 3. Filter by budget
        filtered = self.df[
            (self.df['cost_of_living_index'] >= lo) &
            (self.df['cost_of_living_index'] < hi)
        ].copy()

        if filtered.empty:
            print("\nNo cities found in that budget range. Showing closest matches instead.\n")
            filtered = self.df.copy()

        # 4. Sort by priority
        if choice != '8':
            col, label = self.components[int(choice) - 1]
            if col in filtered.columns:
                filtered = filtered.sort_values(col)
                print(f"\n  Sorted by lowest {label} first.\n")
        else:
            filtered = filtered.sort_values('cost_of_living_index')

        # 5. Show top 10
        top = filtered.head(10).reset_index(drop=True)

        print("="*60)
        print(f"  TOP RECOMMENDED CITIES")
        print("="*60)
        print(f"  {'#':<3} {'City':<22} {'Overall':>8}  {'Housing':>8}  {'Grocery':>8}  {'Transport':>10}")
        print("  " + "-"*58)
        for i, row in top.iterrows():
            print(f"  {i+1:<3} {row['City']:<22} "
                  f"{row['cost_of_living_index']:>8.1f}  "
                  f"{row.get('housing_index', 0):>8.1f}  "
                  f"{row.get('grocery_index', 0):>8.1f}  "
                  f"{row.get('transport_index', 0):>10.1f}")

        print("="*60)
        print("  (Index < 100 = cheaper than Delhi, > 100 = pricier)\n")
