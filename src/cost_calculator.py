import pandas as pd
import numpy as np

class CostIndexCalculator:
    """Calculate Cost of Living Index with proper weightages"""
    
    # Raw weights as specified:
    # food=30, housing=25, electricity=2.5, healthcare=5.3,
    # transport=9, movie=1.71, restaurant=4, education=5  → total = 82.51
    # Re-normalised to 100% inside calculate_index.
    WEIGHTS = {
        'housing':        0.25,
        'grocery':        0.30,
        'transportation': 0.09,
        'healthcare':     0.053,
        'electricity':    0.025,
        'movie':          0.0171,
        'restaurant':     0.04,
        'education':      0.05,
    }
    
    def __init__(self):
        self.base_city = None
        self.normalized_data = None
    
    def normalize_city_names(self, df, city_col='City'):
        """Standardize city names across datasets"""
        city_mapping = {
            'Bangalore': 'Bengaluru',
            'Bombay': 'Mumbai',
            'Calcutta': 'Kolkata',
            'Mangaluru:Mangalore': 'Mangaluru',
            'Mangalore': 'Mangaluru',
            'Mysore': 'Mysuru',
            'Trivandrum:Thiruvananthapuram': 'Thiruvananthapuram',
            'Trivandrum': 'Thiruvananthapuram',
            'Trichy Magicbricks': 'Tiruchirappalli',
            'Trichy': 'Tiruchirappalli',
            'Mumbai Magicbricks': 'Mumbai',
            'Delhi NCR': 'Delhi',
            'Bhopal Magicbricks Csv': 'Bhopal',
            'Kollam Magicbricks Csv': 'Kollam',
            'Kottayam Csv': 'Kottayam',
            'Sangli Csv': 'Sangli',
            'Amaravati': 'Amaravati region',
            'Hubballi': 'Hubli',
            'Merrut': 'Meerut',
            'CITY': None,
        }
        df[city_col] = df[city_col].replace(city_mapping)
        df = df[df[city_col].notna()]  # Remove None entries
        return df
    
    def merge_all_data(self, fuel_df, uber_df, doctor_df, grocery_df, housing_df,
                       swiggy_df=None, movie_df=None, electricity_df=None, tutor_df=None):
        """Merge all datasets on City"""
        # Official list of 50 cities
        official_cities = [
            'Agra', 'Ahmedabad', 'Amaravati region', 'Asansol', 'Aurangabad', 
            'Bengaluru', 'Bhopal', 'Bhubaneswar', 'Chandigarh', 'Chennai', 
            'Coimbatore', 'Delhi', 'Erode', 'Hubli', 'Hyderabad', 
            'Indore', 'Jabalpur', 'Jaipur', 'Jamnagar', 'Kannur', 
            'Kanpur', 'Kochi', 'Kolkata', 'Kolhapur', 'Kollam', 
            'Kottayam', 'Kozhikode', 'Lucknow', 'Ludhiana', 'Madurai', 
            'Malappuram', 'Mangaluru', 'Meerut', 'Mumbai', 'Mysuru', 
            'Nagpur', 'Nashik', 'Patna', 'Pune', 'Raipur', 
            'Rajkot', 'Salem', 'Sangli', 'Solapur', 'Surat', 
            'Thiruvananthapuram', 'Thrissur', 'Tiruchirappalli', 'Vadodara', 'Visakhapatnam'
        ]
        
        # Normalize city names
        all_dfs = [fuel_df, uber_df, doctor_df, grocery_df, housing_df]
        if swiggy_df is not None and not swiggy_df.empty:
            all_dfs.append(swiggy_df)
        if movie_df is not None and not movie_df.empty:
            all_dfs.append(movie_df)
        if electricity_df is not None and not electricity_df.empty:
            all_dfs.append(electricity_df)
        if tutor_df is not None and not tutor_df.empty:
            all_dfs.append(tutor_df)
        for df in all_dfs:
            self.normalize_city_names(df)

        # Start with fuel data (kept for transport context, not weighted)
        merged = fuel_df.copy()
        merged = merged.merge(uber_df,   on='City', how='outer')
        merged = merged.merge(doctor_df, on='City', how='outer')
        merged = merged.merge(grocery_df, on='City', how='outer')
        merged = merged.merge(housing_df, on='City', how='outer')
        if swiggy_df is not None and not swiggy_df.empty:
            merged = merged.merge(swiggy_df, on='City', how='outer')
        if movie_df is not None and not movie_df.empty:
            merged = merged.merge(movie_df, on='City', how='outer')
        if electricity_df is not None and not electricity_df.empty:
            merged = merged.merge(electricity_df, on='City', how='outer')
        if tutor_df is not None and not tutor_df.empty:
            merged = merged.merge(tutor_df, on='City', how='outer')
        
        # Group by City and aggregate (take mean for duplicates)
        numeric_cols = merged.select_dtypes(include=['number']).columns
        agg_dict = {col: 'mean' for col in numeric_cols}
        merged = merged.groupby('City', as_index=False).agg(agg_dict)
        
        # Filter to only official 50 cities
        merged = merged[merged['City'].isin(official_cities)]
        
        return merged
    
    def fill_missing_values(self, df):
        """Fill missing values with mean or median"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if df[col].isna().sum() > 0:
                # Use median for better handling of outliers
                median_val = df[col].median()
                if pd.isna(median_val):
                    # If median is NaN, use mean
                    median_val = df[col].mean()
                if pd.isna(median_val):
                    # If still NaN, use a default value
                    median_val = 0
                df[col] = df[col].fillna(median_val)
                print(f"Filled missing values in {col} with: {median_val:.2f}")
        
        return df
    
    def calculate_index(self, df, base_city='Delhi'):
        """Calculate Cost of Living Index with base city = 100"""
        self.base_city = base_city
        
        # Fill missing values
        df = self.fill_missing_values(df)
        
        # Normalize each metric (base city = 100)
        base_row = df[df['City'] == base_city]
        
        if base_row.empty:
            print(f"Warning: Base city '{base_city}' not found. Using first city as base.")
            base_row = df.iloc[0:1]
            self.base_city = df.iloc[0]['City']
        
        def _idx(col):
            return (df[col] / base_row[col].values[0]) * 100

        df['housing_index']      = _idx('housing_price')
        df['grocery_index']      = _idx('grocery_price')
        df['transport_index']    = _idx('uber_price_per_km')
        df['healthcare_index']   = _idx('doctor_fee')

        # Use real electricity rate; fall back to fuel price if missing
        if 'electricity_rate' in df.columns and df['electricity_rate'].notna().sum() > 5:
            df['electricity_index'] = _idx('electricity_rate')
        else:
            df['electricity_index'] = _idx('avg_fuel_price')

        # Optional components
        has_restaurant = 'restaurant_price'    in df.columns
        has_movie      = 'movie_ticket_price'  in df.columns
        has_education  = 'tutor_fee'           in df.columns

        if has_restaurant:
            df['restaurant_index'] = _idx('restaurant_price')
        if has_movie:
            df['movie_index'] = _idx('movie_ticket_price')
        if has_education:
            df['education_index'] = _idx('tutor_fee')

        # Build active weight map and re-normalise
        active_weights = {
            'housing':        self.WEIGHTS['housing'],
            'grocery':        self.WEIGHTS['grocery'],
            'transportation': self.WEIGHTS['transportation'],
            'healthcare':     self.WEIGHTS['healthcare'],
            'electricity':    self.WEIGHTS['electricity'],
        }
        if has_restaurant:
            active_weights['restaurant'] = self.WEIGHTS['restaurant']
        if has_movie:
            active_weights['movie'] = self.WEIGHTS['movie']
        if has_education:
            active_weights['education'] = self.WEIGHTS['education']

        total_w = sum(active_weights.values())
        norm_w  = {k: v / total_w for k, v in active_weights.items()}

        df['cost_of_living_index'] = (
            df['housing_index']      * norm_w['housing'] +
            df['grocery_index']      * norm_w['grocery'] +
            df['transport_index']    * norm_w['transportation'] +
            df['healthcare_index']   * norm_w['healthcare'] +
            df['electricity_index']  * norm_w['electricity']
        )
        if has_restaurant:
            df['cost_of_living_index'] += df['restaurant_index'] * norm_w['restaurant']
        if has_movie:
            df['cost_of_living_index'] += df['movie_index'] * norm_w['movie']
        if has_education:
            df['cost_of_living_index'] += df['education_index'] * norm_w['education']

        df['cost_of_living_index'] = df['cost_of_living_index'].round(2)
        df = df.sort_values('cost_of_living_index', ascending=False).reset_index(drop=True)
        
        self.normalized_data = df
        self._active_weights = norm_w   # store for reporting
        return df
    
    def get_summary_stats(self, df):
        """Get summary statistics"""
        stats = {
            'total_cities': len(df),
            'base_city': self.base_city,
            'highest_cost_city': df.iloc[0]['City'],
            'highest_cost_index': df.iloc[0]['cost_of_living_index'],
            'lowest_cost_city': df.iloc[-1]['City'],
            'lowest_cost_index': df.iloc[-1]['cost_of_living_index'],
            'mean_index': df['cost_of_living_index'].mean(),
            'median_index': df['cost_of_living_index'].median(),
        }
        return stats
