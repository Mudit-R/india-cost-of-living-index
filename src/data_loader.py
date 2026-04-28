import pandas as pd
import numpy as np
import os
import glob
from pathlib import Path

class DataLoader:
    """Load and process data from various sources"""
    
    def __init__(self):
        self.cities = set()
    
    def load_fuel_prices(self, filepath="../data/raw/transport/Fuel Prices by city (1).csv"):
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
    
    def load_uber_prices(self, filepath="../data/raw/transport/City Wise Uber Price Per km .xlsx"):
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
    
    def load_doctor_fees(self, filepath="../data/raw/healthcare/General Physician Fee City wise.xlsx"):
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
    
    def load_blinkit_data(self, folder="../data/raw/grocery/blinkit_citywise"):
        """Load grocery prices from Blinkit data using product-level price comparison.
        
        Instead of using median prices, this method:
        1. Identifies common products across cities
        2. Compares prices for the same products
        3. Calculates average price ratio relative to Delhi
        """
        import re
        
        # First pass: Load all data and normalize product names
        city_data = {}
        
        for file in glob.glob(f"{folder}/*.xlsx"):
            city_name = Path(file).stem.replace('blinkit_', '').title()
            try:
                df = pd.read_excel(file)
                if len(df) > 0 and len(df.columns) >= 2:
                    # Get product names and prices
                    products = df.iloc[:, 0].astype(str)
                    
                    # Try to find price column (could be column 1 or 2)
                    price_col = None
                    for col_idx in [1, 2]:
                        if col_idx < len(df.columns):
                            col_name = str(df.columns[col_idx]).lower()
                            if 'discount' in col_name or 'price' in col_name:
                                # Prefer discounted price if available
                                if 'discount' in col_name:
                                    price_col = col_idx
                                    break
                                elif price_col is None:
                                    price_col = col_idx
                    
                    if price_col is None:
                        price_col = 1  # Default to second column
                    
                    prices = pd.to_numeric(df.iloc[:, price_col], errors='coerce')
                    
                    # Create product-price mapping
                    product_prices = {}
                    for prod, price in zip(products, prices):
                        if pd.notna(price) and price > 0:
                            # Normalize product name for matching
                            # Remove regional names in parentheses, keep base product
                            normalized = re.sub(r'\s*\([^)]*\)', '', str(prod))
                            normalized = normalized.strip().lower()
                            
                            # Store with original name for reference
                            product_prices[normalized] = {
                                'price': price,
                                'original_name': prod
                            }
                    
                    city_data[city_name] = product_prices
                    
            except Exception as e:
                print(f"Error loading {file}: {e}")
        
        # Second pass: Find common products and calculate price ratios
        if 'Delhi' not in city_data:
            print("Warning: Delhi data not found, using first city as base")
            base_city = list(city_data.keys())[0]
        else:
            base_city = 'Delhi'
        
        base_products = city_data[base_city]
        
        # Calculate grocery index for each city
        city_indices = []
        
        for city_name, city_products in city_data.items():
            # Find common products between this city and base city
            common_products = set(base_products.keys()) & set(city_products.keys())
            
            if len(common_products) < 5:
                # Not enough common products, skip this city
                continue
            
            # Calculate price ratios for common products
            price_ratios = []
            for product in common_products:
                base_price = base_products[product]['price']
                city_price = city_products[product]['price']
                
                if base_price > 0:
                    ratio = city_price / base_price
                    # Filter out extreme outliers (likely data errors)
                    if 0.1 < ratio < 10:  # Reasonable price variation range
                        price_ratios.append(ratio)
            
            if len(price_ratios) >= 3:
                # Calculate average price ratio (mean of ratios)
                avg_ratio = np.mean(price_ratios)
                
                # Convert to price relative to base city
                # If base city average is 100, this city's average is:
                relative_price = avg_ratio * 100
                
                city_indices.append({
                    'City': city_name,
                    'grocery_price': relative_price,
                    'common_products': len(common_products),
                    'price_ratios_used': len(price_ratios)
                })
        
        df = pd.DataFrame(city_indices)
        
        # Normalize so Delhi = 100 (or base city = 100)
        if not df.empty:
            base_value = df[df['City'] == base_city]['grocery_price'].values[0]
            df['grocery_price'] = (df['grocery_price'] / base_value) * 100
            
            self.cities.update(df['City'].tolist())
            
            # Print summary
            print(f"\nGrocery Price Comparison Summary:")
            print(f"  Base city: {base_city}")
            print(f"  Cities with data: {len(df)}")
            print(f"  Avg common products: {df['common_products'].mean():.0f}")
            print(f"  Method: Product-level price comparison")
        
        return df[['City', 'grocery_price']]
    
    def load_electricity_prices(self, filepath="../data/raw/utilities/Electricity Price.xlsx"):
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

    def load_swiggy_data(self, filepath="../data/raw/entertainment/swiggy dataset.xlsx"):
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

    def load_movie_ticket_prices(self, filepath="../data/raw/entertainment/Movieticketprices.xlsx"):
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

    def load_tutor_data(self, filepath="../data/raw/education/TutorData_Filtered.xlsx"):
        """Load tutor/education fees data (per-hour only)"""
        city_fees = []
        try:
            df = pd.read_excel(filepath)
            df.columns = df.columns.str.strip()
            
            # Filter out rows where City is NaN or Fee is NaN
            df = df.dropna(subset=['City', 'Fee'])
            df['City'] = df['City'].astype(str).str.strip()
            
            # Filter to only include per-hour fees (exclude monthly fees)
            df = df[df['Fee'].str.contains('/hour', case=False, na=False)]
            
            # Extract numeric fee values from the Fee column
            # Format: ₹300–1,000/hour or ₹500–800/hour
            def extract_fee_range(fee_str):
                """Extract average of fee range"""
                try:
                    # Extract numbers from string like "₹300–1,000/hour"
                    import re
                    numbers = re.findall(r'₹([\d,]+)', str(fee_str))
                    if len(numbers) >= 2:
                        # Get min and max, remove commas, convert to float
                        min_fee = float(numbers[0].replace(',', ''))
                        max_fee = float(numbers[1].replace(',', ''))
                        return (min_fee + max_fee) / 2
                    elif len(numbers) == 1:
                        return float(numbers[0].replace(',', ''))
                    return None
                except:
                    return None
            
            df['fee_numeric'] = df['Fee'].apply(extract_fee_range)
            df = df.dropna(subset=['fee_numeric'])
            
            # Group by city and calculate average (mean) with outlier removal
            for city, grp in df.groupby('City'):
                fees = grp['fee_numeric']
                if len(fees) >= 3:  # Need at least 3 data points
                    # Remove outliers using IQR method
                    Q1, Q3 = fees.quantile(0.25), fees.quantile(0.75)
                    IQR = Q3 - Q1
                    clean = fees[(fees >= Q1 - 1.5*IQR) & (fees <= Q3 + 1.5*IQR)]
                    if len(clean) > 0:
                        city_fees.append({'City': city, 'tutor_fee': clean.mean()})
        except Exception as e:
            print(f"Error loading tutor data: {e}")
        
        result = pd.DataFrame(city_fees)
        if not result.empty:
            self.cities.update(result['City'].tolist())
        return result

    def load_housing_data(self, folder="../data/raw/Magic Bricks data"):
        """Load housing prices from MagicBricks data.
        Uses median price_per_sq_ft with outlier removal for robustness.
        """
        city_prices = []

        def _extract_price(file):
            try:
                df = pd.read_csv(file)
                
                # Use price_per_sq_ft column
                if 'price_per_sq_ft' in df.columns:
                    prices = pd.to_numeric(df['price_per_sq_ft'], errors='coerce').dropna()
                    prices = prices[prices > 0]
                    
                    if len(prices) < 5:
                        return None
                    
                    # IQR outlier removal
                    Q1, Q3 = prices.quantile(0.25), prices.quantile(0.75)
                    IQR = Q3 - Q1
                    clean = prices[(prices >= Q1 - 1.5*IQR) & (prices <= Q3 + 1.5*IQR)]
                    
                    return float(clean.median()) if len(clean) > 0 else None
                else:
                    return None
            except Exception as e:
                print(f"Error loading {file}: {e}")
                return None

        # Load all CSV files with new naming format: CityName_magicbricks.csv
        for file in glob.glob(f"{folder}/*_magicbricks.csv"):
            # Extract city name from filename (e.g., "Delhi_magicbricks.csv" -> "Delhi")
            city_name = Path(file).stem.replace('_magicbricks', '').strip()
            price = _extract_price(file)
            if price:
                city_prices.append({'City': city_name, 'housing_price': price})

        df = pd.DataFrame(city_prices)
        if not df.empty:
            self.cities.update(df['City'].tolist())
        return df
