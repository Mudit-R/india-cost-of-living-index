#!/usr/bin/env python3
"""
Weight Optimizer — fine-tune component weights by comparing against third-party data.
Uses scipy.optimize to minimize error between our index and reference data.
"""

import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt


class WeightOptimizer:
    def __init__(self, data_file='cost_index_results.csv'):
        self.df = pd.read_csv(data_file)
        self.components = [
            'housing_index',
            'grocery_index', 
            'transport_index',
            'healthcare_index',
            'electricity_index',
            'restaurant_index',
            'movie_index',
        ]
        
        # Current weights (normalized)
        self.current_weights = {
            'housing_index':      0.3225,
            'grocery_index':      0.3870,
            'transport_index':    0.1161,
            'healthcare_index':   0.0684,
            'electricity_index':  0.0323,
            'restaurant_index':   0.0516,
            'movie_index':        0.0221,
        }
    
    def load_reference_data(self, source='numbeo'):
        """
        Load third-party cost index data.
        You'll need to provide this data — either scraped or manually entered.
        
        Expected format: CSV with columns ['City', 'reference_index']
        where reference_index is their cost-of-living index (Delhi = 100 or similar)
        """
        print(f"\n[1] Loading reference data from {source}...")
        
        # Numbeo Cost of Living Index (2026)
        # Source: Numbeo.com rankings
        # Raw indices — will normalize to Delhi = 100
        numbeo_raw = {
            'Mumbai': 26.3,
            'Gurgaon': 24.7,
            'Delhi': 23.0,
            'Pune': 22.8,
            'Bangalore': 21.9,
            'Noida': 21.9,
            'Hyderabad': 21.7,
            'Ahmedabad': 21.2,
            'Chandigarh': 20.9,
            'Chennai': 20.7,
            'Thane': 20.7,
            'Vadodara': 20.6,
            'Bhubaneswar': 19.4,
            'Patna': 19.4,
            'Bhopal': 19.2,
            'Kolkata': 19.2,
            'Kochi': 19.0,
            'Jaipur': 19.0,
            'Surat': 18.7,
            'Indore': 18.4,
            'Lucknow': 17.8,
            'Coimbatore': 17.6,
        }
        
        # Normalize to Delhi = 100
        delhi_base = numbeo_raw['Delhi']
        reference = {city: (val / delhi_base) * 100 
                    for city, val in numbeo_raw.items()}
        
        # Map alternate city names
        reference['Bengaluru'] = reference.pop('Bangalore')
        
        ref_df = pd.DataFrame(list(reference.items()), 
                              columns=['City', 'reference_index'])
        
        print(f"  ✓ Loaded {len(ref_df)} cities from {source}")
        return ref_df
    
    def calculate_index_with_weights(self, weights_array):
        """Calculate cost index using given weights array"""
        # Ensure weights sum to 1
        weights_array = weights_array / weights_array.sum()
        
        # Calculate weighted index
        index = np.zeros(len(self.df))
        for i, comp in enumerate(self.components):
            if comp in self.df.columns:
                index += self.df[comp].values * weights_array[i]
        
        return index
    
    def objective_function(self, weights_array, ref_df):
        """
        Objective: minimize RMSE between our index and reference index.
        Only for cities present in both datasets.
        """
        # Calculate our index with these weights
        self.df['temp_index'] = self.calculate_index_with_weights(weights_array)
        
        # Merge with reference
        merged = self.df[['City', 'temp_index']].merge(ref_df, on='City', how='inner')
        
        if len(merged) == 0:
            return 1e6  # penalty if no overlap
        
        # RMSE
        error = np.sqrt(((merged['temp_index'] - merged['reference_index'])**2).mean())
        return error
    
    def optimize_weights(self, ref_df):
        """Find optimal weights using scipy.optimize"""
        print("\n[2] Optimizing weights...")
        
        # Initial guess (current weights)
        x0 = np.array([self.current_weights[c] for c in self.components])
        
        # Constraints: all weights >= 0, sum = 1
        constraints = {'type': 'eq', 'fun': lambda x: x.sum() - 1}
        bounds = [(0, 1) for _ in self.components]
        
        result = minimize(
            self.objective_function,
            x0,
            args=(ref_df,),
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': 1000}
        )
        
        if result.success:
            print(f"  ✓ Optimization converged")
            print(f"  ✓ Final RMSE: {result.fun:.2f}")
        else:
            print(f"  ⚠ Optimization did not converge: {result.message}")
        
        return result.x
    
    def compare_weights(self, optimized_weights, ref_df):
        """Compare current vs optimized weights"""
        print("\n" + "="*80)
        print("WEIGHT COMPARISON")
        print("="*80)
        
        print(f"\n{'Component':<20} {'Current':>12} {'Optimized':>12} {'Change':>12}")
        print("-" * 60)
        
        for i, comp in enumerate(self.components):
            label = comp.replace('_index', '').title()
            current = self.current_weights[comp]
            optimized = optimized_weights[i]
            change = ((optimized - current) / current) * 100
            
            print(f"{label:<20} {current*100:>11.2f}% {optimized*100:>11.2f}% "
                  f"{change:>+10.1f}%")
        
        print("-" * 60)
        print(f"{'TOTAL':<20} {100.0:>11.2f}% {100.0:>11.2f}%")
    
    def compare_results(self, optimized_weights, ref_df):
        """Compare index results: current vs optimized vs reference"""
        print("\n" + "="*80)
        print("INDEX COMPARISON (Cities in Reference Data)")
        print("="*80)
        
        # Calculate both indices
        self.df['current_index'] = self.df['cost_of_living_index']
        self.df['optimized_index'] = self.calculate_index_with_weights(optimized_weights)
        
        # Merge with reference
        comparison = self.df[['City', 'current_index', 'optimized_index']].merge(
            ref_df, on='City', how='inner'
        )
        
        # Calculate errors
        comparison['current_error'] = abs(comparison['current_index'] - 
                                          comparison['reference_index'])
        comparison['optimized_error'] = abs(comparison['optimized_index'] - 
                                            comparison['reference_index'])
        
        # Sort by reference index
        comparison = comparison.sort_values('reference_index', ascending=False)
        
        print(f"\n{'City':<18} {'Reference':>10} {'Current':>10} {'Optimized':>10} "
              f"{'Curr Err':>10} {'Opt Err':>10}")
        print("-" * 80)
        
        for _, row in comparison.iterrows():
            print(f"{row['City']:<18} {row['reference_index']:>10.1f} "
                  f"{row['current_index']:>10.1f} {row['optimized_index']:>10.1f} "
                  f"{row['current_error']:>10.1f} {row['optimized_error']:>10.1f}")
        
        print("-" * 80)
        print(f"{'MEAN ERROR':<18} {'':<10} "
              f"{comparison['current_error'].mean():>10.1f} "
              f"{comparison['optimized_error'].mean():>10.1f}")
        print(f"{'RMSE':<18} {'':<10} "
              f"{np.sqrt((comparison['current_error']**2).mean()):>10.1f} "
              f"{np.sqrt((comparison['optimized_error']**2).mean()):>10.1f}")
        
        return comparison
    
    def plot_comparison(self, comparison):
        """Visualize current vs optimized vs reference"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Plot 1: Scatter — Current vs Reference
        ax1 = axes[0]
        ax1.scatter(comparison['reference_index'], comparison['current_index'], 
                   alpha=0.7, s=80, label='Current')
        ax1.plot([50, 180], [50, 180], 'k--', alpha=0.3, label='Perfect match')
        ax1.set_xlabel('Reference Index')
        ax1.set_ylabel('Our Index')
        ax1.set_title('Current Weights vs Reference')
        ax1.legend()
        ax1.grid(alpha=0.3)
        
        # Plot 2: Scatter — Optimized vs Reference
        ax2 = axes[1]
        ax2.scatter(comparison['reference_index'], comparison['optimized_index'],
                   alpha=0.7, s=80, color='green', label='Optimized')
        ax2.plot([50, 180], [50, 180], 'k--', alpha=0.3, label='Perfect match')
        ax2.set_xlabel('Reference Index')
        ax2.set_ylabel('Our Index')
        ax2.set_title('Optimized Weights vs Reference')
        ax2.legend()
        ax2.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('weight_optimization_comparison.png', dpi=150, bbox_inches='tight')
        print(f"\n  ✓ Saved: weight_optimization_comparison.png")
        plt.close()
    
    def run(self, reference_source='numbeo'):
        """Main workflow"""
        print("="*80)
        print("WEIGHT OPTIMIZATION — Fine-tune using Third-Party Data")
        print("="*80)
        
        # Load reference data
        ref_df = self.load_reference_data(reference_source)
        
        # Optimize
        optimized_weights = self.optimize_weights(ref_df)
        
        # Compare weights
        self.compare_weights(optimized_weights, ref_df)
        
        # Compare results
        comparison = self.compare_results(optimized_weights, ref_df)
        
        # Visualize
        self.plot_comparison(comparison)
        
        # Export optimized weights
        weights_dict = {comp: float(w) for comp, w in 
                       zip(self.components, optimized_weights)}
        
        print("\n" + "="*80)
        print("OPTIMIZED WEIGHTS (Python dict format)")
        print("="*80)
        print("\nCOST_WEIGHTS = {")
        for comp, weight in weights_dict.items():
            label = comp.replace('_index', '')
            print(f"    '{label}': {weight:.6f},")
        print("}")
        
        print("\n" + "="*80)
        print("✓ Optimization complete!")
        print("="*80)
        print("\nNext steps:")
        print("  1. Review the comparison chart: weight_optimization_comparison.png")
        print("  2. If optimized weights look better, update cost_calculator.py")
        print("  3. Re-run main.py to recalculate all indices")
        print("="*80)


if __name__ == "__main__":
    optimizer = WeightOptimizer()
    optimizer.run()
