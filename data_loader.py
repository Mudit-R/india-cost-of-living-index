import pandas as pd
import numpy as np
import os
import glob
from pathlib import Path

class DataLoader:
    """Load and process data from various sources"""
    
    def __init__(self):
        self.cities = set()
    
    def load_fuel_prices(self, filepath="Fuel Prices by city (1).csv"):
        """Load fuel prices data"""
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.strip()
        df = df.dropna(subset=[df.columns[0]])
        df.rename(columns={df.columns[0]: 'City'}, inplace=True)
        df['City'] = df['City'].str.strip()
        
        # Clean price columns
        for col in ['Petroi', 'Diesel', 'CNG', 'LPG']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace('₹', '').str.replace(',', '').str.strip()
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Calculate average fuel price
        df['avg_fuel_price'] = df[['Petroi', 'Diesel']].mean(axis=1)
        self.cities.update(df['City'].tolist())
        return df[['City', 'avg_fuel_price']]
    
    def load_uber_prices(self, filepath="City Wise Uber Price Per km .xlsx"):
        """Load Uber pricing data"""
        df = pd.read_excel(filepath)
        df.columns = df.columns.str.strip()
        # The actual column is 'Price/Km'
        if 'Price/Km' in df.columns and 'City' in df.columns:
            df = df[['City', 'Price/Km']].copy()
            df.rename(columns={'Price/Km': 'uber_price_per_km'}, inplace=True)
        else:
            df.rename(columns={df.columns[1]: 'City', df.columns[6]: 'uber_price_per_km'}, inplace=True)
            df = df[['City', 'uber_price_per_km']].copy()
        
        df['City'] = df['City'].astype(str).str.strip()
        df['uber_price_per_km'] = pd.to_numeric(df['uber_price_per_km'], errors='coerce')
        df = df.dropna(subset=['City', 'uber_price_per_km'])
        df = df[df['City'] != 'nan']
        self.cities.update(df['City'].tolist())
        return df[['City', 'uber_price_per_km']]
    
    def load_doctor_fees(self, filepath="General Physician Fee City wise.xlsx"):
        """Load doctor consultation fees — wide format: city in col 0, fees across remaining cols"""
        city_fees = []
        try:
            df = pd.read_excel(filepath, header=0)
            for _, row in df.iterrows():
                city = str(row.iloc[0]).strip()
                if city in ('nan', 'CITY', ''):
                    continue
                fees = pd.to_numeric(row.iloc[1:], errors='coerce').dropna()
                if len(fees) == 0:
                    continue
                # Remove outliers with IQR before taking median
                Q1, Q3 = fees.quantile(0.25), fees.quantile(0.75)
                IQR = Q3 - Q1
                clean = fees[(fees >= Q1 - 1.5 * IQR) & (fees <= Q3 + 1.5 * IQR)]
                if len(clean) > 0:
                    city_fees.append({'City': city, 'doctor_fee': clean.median()})
        except Exception as e:
            print(f"Error loading doctor fees: {e}")

        result = pd.DataFrame(city_fees)
        if not result.empty:
            self.cities.update(result['City'].tolist())
        return result[['City', 'doctor_fee']]
    
    def load_blinkit_data(self, folder="blinkit_citywise"):
        """Load grocery prices from Blinkit data with outlier removal"""
        city_prices = []
        
        for file in glob.glob(f"{folder}/*.xlsx"):
            city_name = Path(file).stem.replace('blinkit_', '').title()
            try:
                df = pd.read_excel(file)
                if len(df) > 0 and len(df.columns) >= 2:
                    # Assume price is in second column
                    prices = pd.to_numeric(df.iloc[:, 1], errors='coerce').dropna()
                    if len(prices) > 0:
                        # Remove outliers using IQR method
                        Q1 = prices.quantile(0.25)
                        Q3 = prices.quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        prices_clean = prices[(prices >= lower_bound) & (prices <= upper_bound)]
                        
                        if len(prices_clean) > 0:
                            avg_price = prices_clean.median()  # Use median for robustness
                            city_prices.append({'City': city_name, 'grocery_price': avg_price})
            except Exception as e:
                print(f"Error loading {file}: {e}")
        
        df = pd.DataFrame(city_prices)
        self.cities.update(df['City'].tolist())
        return df
    
    def load_electricity_prices(self, filepath="Electricity Price.xlsx"):
        """Load electricity rates (₹/unit) per city"""
        try:
            df = pd.read_excel(filepath)
            df.columns = df.columns.str.strip()
            df.rename(columns={
                'City': 'City',
                'Effective Rate (₹/unit)': 'electricity_rate'
            }, inplace=True)
            df['City'] = df['City'].astype(str).str.strip()
            df['electricity_rate'] = pd.to_numeric(df['electricity_rate'], errors='coerce')
            df = df[['City', 'electricity_rate']].dropna()
            self.cities.update(df['City'].tolist())
            return df
        except Exception as e:
            print(f"Error loading electricity prices: {e}")
            return pd.DataFrame(columns=['City', 'electricity_rate'])

    def load_swiggy_data(self, filepath="swiggy dataset.xlsx"):
        """Load restaurant prices from Swiggy data"""
        city_prices = []
        try:
            df = pd.read_excel(filepath)
            df.columns = df.columns.str.strip()
            # Columns: 'Average Price', 'Location'
            price_col = [c for c in df.columns if 'price' in c.lower() or 'average' in c.lower()][0]
            city_col  = [c for c in df.columns if 'location' in c.lower() or 'city' in c.lower()][0]
            # Extract digits before copy to avoid Arrow dtype str.extract issues
            df['_price'] = pd.to_numeric(df[price_col].str.extract(r'(\d+)')[0], errors='coerce')
            df = df[[city_col, '_price']].copy()
            df.columns = ['City', 'price']
            df['City'] = df['City'].astype(str).str.strip()
            df = df.dropna(subset=['price'])
            # Per-person price = price / 2
            df['price'] = df['price'] / 2

            for city, grp in df.groupby('City'):
                prices = grp['price']
                Q1, Q3 = prices.quantile(0.25), prices.quantile(0.75)
                IQR = Q3 - Q1
                clean = prices[(prices >= Q1 - 1.5*IQR) & (prices <= Q3 + 1.5*IQR)]
                if len(clean) > 0:
                    city_prices.append({'City': city, 'restaurant_price': clean.median()})
        except Exception as e:
            print(f"Error loading Swiggy data: {e}")

        result = pd.DataFrame(city_prices)

        # For cities with alternate names, also add a row under the canonical name
        aliases = {
            'Bangalore':  'Bengaluru',
            'Mysore':     'Mysuru',
            'Trichy':     'Tiruchirappalli',
            'Vizag':      'Visakhapatnam',
            'Amravati':   'Amaravati region',
        }
        extra_rows = []
        for _, row in result.iterrows():
            if row['City'] in aliases:
                extra_rows.append({'City': aliases[row['City']], 'restaurant_price': row['restaurant_price']})
        if extra_rows:
            result = pd.concat([result, pd.DataFrame(extra_rows)], ignore_index=True)

        if not result.empty:
            self.cities.update(result['City'].tolist())
        return result

    def load_movie_ticket_prices(self, filepath="Movieticketprices.xlsx"):
        """Load movie ticket prices"""
        city_prices = []
        try:
            df = pd.read_excel(filepath, header=1)   # row 0 is a merged header
            # First non-index column is City, rest are ticket prices
            df = df.dropna(how='all')
            city_col = df.columns[1]   # column index 1 holds city names
            df.rename(columns={city_col: 'City'}, inplace=True)
            df['City'] = df['City'].astype(str).str.strip()
            df = df[df['City'].str.len() > 1]

            price_cols = df.columns[2:]   # all columns after City are prices
            for _, row in df.iterrows():
                city = row['City']
                prices = pd.to_numeric(row[price_cols], errors='coerce').dropna()
                if len(prices) > 0:
                    Q1, Q3 = prices.quantile(0.25), prices.quantile(0.75)
                    IQR = Q3 - Q1
                    clean = prices[(prices >= Q1 - 1.5*IQR) & (prices <= Q3 + 1.5*IQR)]
                    if len(clean) > 0:
                        city_prices.append({'City': city, 'movie_ticket_price': clean.median()})
        except Exception as e:
            print(f"Error loading movie ticket prices: {e}")

        result = pd.DataFrame(city_prices)
        if not result.empty:
            self.cities.update(result['City'].tolist())
        return result

    def load_housing_data(self, folder="Magic Bricks data"):
        """Load housing prices from MagicBricks data.
        Uses P25 (lower quartile) to represent affordable/typical housing,
        since MagicBricks skews toward premium listings in many cities.
        """
        city_prices = []

        def _extract_price(file, is_csv=False):
            try:
                df = pd.read_csv(file) if is_csv else pd.read_excel(file)
                # Prefer price_per_sq_ft — removes size bias across cities
                if 'price_per_sq_ft' in df.columns:
                    col = 'price_per_sq_ft'
                else:
                    # fallback to total price if column missing
                    price_cols = [c for c in df.columns
                                  if 'price' in c.lower() and 'sq' not in c.lower()]
                    if not price_cols:
                        return None
                    col = price_cols[0]

                prices = pd.to_numeric(df[col], errors='coerce').dropna()
                prices = prices[prices > 0]
                if len(prices) < 5:
                    return None
                # IQR outlier removal
                Q1, Q3 = prices.quantile(0.25), prices.quantile(0.75)
                IQR = Q3 - Q1
                clean = prices[(prices >= Q1 - 1.5*IQR) & (prices <= Q3 + 1.5*IQR)]
                return float(clean.median()) if len(clean) > 0 else None
            except Exception as e:
                print(f"Error loading {file}: {e}")
                return None

        for file in glob.glob(f"{folder}/*.xlsx"):
            city_name = (Path(file).stem.title()
                         .replace(' Magicbricks', '').replace(' Magic Bricks', '').strip())
            price = _extract_price(file)
            if price:
                city_prices.append({'City': city_name, 'housing_price': price})

        for file in glob.glob(f"{folder}/*.csv"):
            city_name = (Path(file).stem
                         .replace(' magic bricks csv', '').replace(' magicbricks csv', '')
                         .replace(' MagicBricks', '').replace(' Magicbricks', '')
                         .replace('Mysuru:Mysore', 'Mysuru').strip().title())
            price = _extract_price(file, is_csv=True)
            if price:
                city_prices.append({'City': city_name, 'housing_price': price})

        df = pd.DataFrame(city_prices)
        self.cities.update(df['City'].tolist())
        return df
