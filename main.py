#!/usr/bin/env python3
"""
Cost of Living Index Calculator for 50 Indian Cities
"""

from data_loader import DataLoader
from cost_calculator import CostIndexCalculator
from visualizer import Visualizer
import pandas as pd

def print_separator():
    print("\n" + "="*80 + "\n")

def main():
    print("="*80)
    print("COST OF LIVING INDEX - 50 INDIAN CITIES")
    print("="*80)
    
    # Step 1: Load all data
    print("\n[1/5] Loading data from all sources...")
    loader = DataLoader()
    
    fuel_df = loader.load_fuel_prices()
    print(f"  ✓ Loaded fuel prices for {len(fuel_df)} cities")
    
    uber_df = loader.load_uber_prices()
    print(f"  ✓ Loaded Uber prices for {len(uber_df)} cities")
    
    doctor_df = loader.load_doctor_fees()
    print(f"  ✓ Loaded doctor fees for {len(doctor_df)} cities")
    
    grocery_df = loader.load_blinkit_data()
    print(f"  ✓ Loaded grocery prices for {len(grocery_df)} cities")
    
    housing_df = loader.load_housing_data()
    print(f"  ✓ Loaded housing prices for {len(housing_df)} cities")
    
    swiggy_df = loader.load_swiggy_data()
    print(f"  ✓ Loaded restaurant prices (Swiggy) for {len(swiggy_df)} cities")

    movie_df = loader.load_movie_ticket_prices()
    print(f"  ✓ Loaded movie ticket prices for {len(movie_df)} cities")

    electricity_df = loader.load_electricity_prices()
    print(f"  ✓ Loaded electricity rates for {len(electricity_df)} cities")
    
    tutor_df = loader.load_tutor_data()
    print(f"  ✓ Loaded tutor/education fees for {len(tutor_df)} cities")
    
    # Step 2: Merge and calculate index
    print("\n[2/5] Merging datasets and calculating cost index...")
    calculator = CostIndexCalculator()
    
    merged_df = calculator.merge_all_data(
        fuel_df, uber_df, doctor_df, grocery_df, housing_df,
        swiggy_df=swiggy_df, movie_df=movie_df, electricity_df=electricity_df,
        tutor_df=tutor_df
    )
    print(f"  ✓ Merged data for {len(merged_df)} cities")
    
    result_df = calculator.calculate_index(merged_df, base_city='Delhi')
    print(f"  ✓ Calculated cost index (Base: {calculator.base_city} = 100)")
    
    # Step 3: Save results
    print("\n[3/5] Saving results...")
    output_file = 'cost_index_results.csv'
    result_df.to_csv(output_file, index=False)
    print(f"  ✓ Saved complete results to: {output_file}")
    
    # Step 4: Generate visualizations
    print("\n[4/5] Generating visualizations...")
    viz = Visualizer()
    viz.plot_top_bottom_cities(result_df, n=10)
    viz.plot_component_breakdown(result_df, cities=result_df.head(10)['City'].tolist())
    viz.plot_distribution(result_df)
    viz.plot_heatmap(result_df)
    viz.plot_restaurant_prices(result_df)
    viz.plot_movie_ticket_prices(result_df)
    viz.plot_entertainment_vs_dining(result_df)
    viz.plot_electricity_rates(result_df)
    print("  ✓ All visualizations saved to 'visualizations/' folder")
    
    # Step 5: Display summary
    print_separator()
    print("[5/5] SUMMARY & KEY FINDINGS")
    print_separator()
    
    stats = calculator.get_summary_stats(result_df)
    
    print(f"Total Cities Analyzed: {stats['total_cities']}")
    print(f"Base City: {stats['base_city']} (Index = 100)")
    print(f"\nMost Expensive City: {stats['highest_cost_city']} (Index = {stats['highest_cost_index']:.2f})")
    print(f"Most Affordable City: {stats['lowest_cost_city']} (Index = {stats['lowest_cost_index']:.2f})")
    print(f"\nAverage Index: {stats['mean_index']:.2f}")
    print(f"Median Index: {stats['median_index']:.2f}")
    
    print_separator()
    print("TOP 10 MOST EXPENSIVE CITIES")
    print_separator()
    
    top_10 = result_df.head(10)[['City', 'cost_of_living_index', 'housing_index', 
                                   'grocery_index', 'transport_index']]
    print(top_10.to_string(index=False))
    
    print_separator()
    print("TOP 10 MOST AFFORDABLE CITIES")
    print_separator()
    
    bottom_10 = result_df.tail(10)[['City', 'cost_of_living_index', 'housing_index', 
                                      'grocery_index', 'transport_index']]
    print(bottom_10.to_string(index=False))
    
    print_separator()
    print("WEIGHTAGE DISTRIBUTION (re-normalised to 100%)")
    print_separator()
    w = calculator._active_weights
    for label, key in [("Housing", "housing"), ("Food/Grocery", "grocery"),
                        ("Transport", "transportation"), ("Healthcare", "healthcare"),
                        ("Electricity", "electricity"), ("Restaurants", "restaurant"),
                        ("Movies", "movie"), ("Education", "education")]:
        if key in w:
            print(f"{label:<20} {w[key]*100:.2f}%")
    
    print_separator()
    print("KEY OBSERVATIONS")
    print_separator()
    
    # Calculate some insights
    high_housing = result_df.nlargest(3, 'housing_index')['City'].tolist()
    low_housing = result_df.nsmallest(3, 'housing_index')['City'].tolist()
    
    print(f"1. Housing costs vary significantly across cities")
    print(f"   Highest: {', '.join(high_housing)}")
    print(f"   Lowest: {', '.join(low_housing)}")
    
    print(f"\n2. Cost spread: {stats['highest_cost_index']:.1f} / {stats['lowest_cost_index']:.1f} = "
          f"{stats['highest_cost_index']/stats['lowest_cost_index']:.2f}x difference")
    
    above_base = len(result_df[result_df['cost_of_living_index'] > 100])
    print(f"\n3. {above_base} cities are more expensive than {stats['base_city']}")
    print(f"   {stats['total_cities'] - above_base} cities are more affordable than {stats['base_city']}")
    
    print_separator()
    print("✓ Analysis complete! Check 'visualizations/' folder for charts.")
    print_separator()

if __name__ == "__main__":
    main()
