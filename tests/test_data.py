#!/usr/bin/env python3
"""
Quick test script to verify data loading
"""

import sys

def test_imports():
    """Test if required packages are installed"""
    try:
        import pandas as pd
        import numpy as np
        import matplotlib
        import seaborn
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing package: {e}")
        print("\nPlease install requirements:")
        print("  pip install -r requirements.txt")
        return False

def test_data_files():
    """Test if data files exist"""
    import os
    
    files = [
        "Fuel Prices by city (1).csv",
        "City Wise Uber Price Per km .xlsx",
        "General Physician Fee City wise.xlsx",
    ]
    
    folders = [
        "blinkit_citywise",
        "Magic Bricks data"
    ]
    
    all_exist = True
    
    for file in files:
        if os.path.exists(file):
            print(f"✓ Found: {file}")
        else:
            print(f"✗ Missing: {file}")
            all_exist = False
    
    for folder in folders:
        if os.path.exists(folder) and os.path.isdir(folder):
            file_count = len([f for f in os.listdir(folder) if not f.startswith('.')])
            print(f"✓ Found: {folder}/ ({file_count} files)")
        else:
            print(f"✗ Missing: {folder}/")
            all_exist = False
    
    return all_exist

def test_data_loading():
    """Test if data can be loaded"""
    try:
        from data_loader import DataLoader
        
        loader = DataLoader()
        
        print("\nTesting data loading...")
        
        fuel_df = loader.load_fuel_prices()
        print(f"✓ Loaded fuel prices: {len(fuel_df)} cities")
        
        uber_df = loader.load_uber_prices()
        print(f"✓ Loaded Uber prices: {len(uber_df)} cities")
        
        doctor_df = loader.load_doctor_fees()
        print(f"✓ Loaded doctor fees: {len(doctor_df)} cities")
        
        grocery_df = loader.load_blinkit_data()
        print(f"✓ Loaded grocery prices: {len(grocery_df)} cities")
        
        housing_df = loader.load_housing_data()
        print(f"✓ Loaded housing prices: {len(housing_df)} cities")
        
        print(f"\nTotal unique cities: {len(loader.cities)}")
        
        return True
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("="*60)
    print("DATA VERIFICATION TEST")
    print("="*60)
    
    print("\n[1/3] Checking Python packages...")
    if not test_imports():
        sys.exit(1)
    
    print("\n[2/3] Checking data files...")
    if not test_data_files():
        print("\n⚠ Some data files are missing!")
        sys.exit(1)
    
    print("\n[3/3] Testing data loading...")
    if not test_data_loading():
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED!")
    print("="*60)
    print("\nYou can now run: python main.py")

if __name__ == "__main__":
    main()
