import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

class Visualizer:
    """Create visualizations for cost index analysis"""

    # Human-readable labels for every possible index column
    COMPONENT_LABELS = {
        'housing_index':      'Housing',
        'grocery_index':      'Grocery',
        'transport_index':    'Transport',
        'healthcare_index':   'Healthcare',
        'electricity_index':  'Electricity',
        'restaurant_index':   'Restaurants',
        'movie_index':        'Movies',
    }
    COMPONENT_COLORS = {
        'housing_index':      '#3498db',
        'grocery_index':      '#e74c3c',
        'transport_index':    '#f39c12',
        'healthcare_index':   '#9b59b6',
        'electricity_index':  '#1abc9c',
        'restaurant_index':   '#e67e22',
        'movie_index':        '#e91e63',
    }

    def __init__(self, output_dir='../outputs/visualizations'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        sns.set_style('whitegrid')

    def _active_components(self, df):
        """Return index columns that are actually present in df."""
        return [c for c in self.COMPONENT_LABELS if c in df.columns]

    # ------------------------------------------------------------------
    # 1. Top / Bottom cities bar chart
    # ------------------------------------------------------------------
    def plot_top_bottom_cities(self, df, n=10):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        top_n = df.head(n)
        ax1.barh(top_n['City'], top_n['cost_of_living_index'], color='#e74c3c')
        ax1.set_xlabel('Cost of Living Index')
        ax1.set_title(f'Top {n} Most Expensive Cities')
        ax1.axvline(100, color='black', linestyle='--', alpha=0.4, label='Delhi = 100')
        ax1.invert_yaxis()
        ax1.legend()

        bottom_n = df.tail(n)
        ax2.barh(bottom_n['City'], bottom_n['cost_of_living_index'], color='#27ae60')
        ax2.set_xlabel('Cost of Living Index')
        ax2.set_title(f'Top {n} Most Affordable Cities')
        ax2.axvline(100, color='black', linestyle='--', alpha=0.4, label='Delhi = 100')
        ax2.invert_yaxis()
        ax2.legend()

        plt.tight_layout()
        path = f'{self.output_dir}/top_bottom_cities.png'
        plt.savefig(path, dpi=150, bbox_inches='tight')
        print(f"Saved: {path}")
        plt.close()

    # ------------------------------------------------------------------
    # 2. Component breakdown grouped bar chart (all 7 components)
    # ------------------------------------------------------------------
    def plot_component_breakdown(self, df, cities=None):
        if cities is None:
            cities = df.head(10)['City'].tolist()

        subset = df[df['City'].isin(cities)].copy()
        components = self._active_components(df)

        n_cities = len(subset)
        n_comp   = len(components)
        width    = 0.8 / n_comp

        fig, ax = plt.subplots(figsize=(max(14, n_cities * 1.4), 8))
        x = np.arange(n_cities)

        for i, comp in enumerate(components):
            offset = width * (i - n_comp / 2 + 0.5)
            ax.bar(x + offset, subset[comp], width,
                   label=self.COMPONENT_LABELS[comp],
                   color=self.COMPONENT_COLORS[comp])

        ax.set_xlabel('City')
        ax.set_ylabel('Index Value (Delhi = 100)')
        ax.set_title('Cost Component Breakdown by City (All 7 Components)')
        ax.set_xticks(x)
        ax.set_xticklabels(subset['City'], rotation=45, ha='right')
        ax.axhline(y=100, color='black', linestyle='--', alpha=0.4, label='Base 100')
        ax.legend(loc='upper right')

        plt.tight_layout()
        path = f'{self.output_dir}/component_breakdown.png'
        plt.savefig(path, dpi=150, bbox_inches='tight')
        print(f"Saved: {path}")
        plt.close()

    # ------------------------------------------------------------------
    # 3. Distribution histograms (one per component + overall)
    # ------------------------------------------------------------------
    def plot_distribution(self, df):
        components = self._active_components(df)
        all_cols = [('cost_of_living_index', 'Overall Cost Index')] + \
                   [(c, self.COMPONENT_LABELS[c]) for c in components]

        n = len(all_cols)
        ncols = 3
        nrows = (n + ncols - 1) // ncols

        fig, axes = plt.subplots(nrows, ncols, figsize=(16, 5 * nrows))
        axes_flat = axes.flat if nrows > 1 else [axes] if ncols == 1 else axes.flat

        for ax, (col, title) in zip(axes_flat, all_cols):
            data = df[col].dropna()
            color = self.COMPONENT_COLORS.get(col, '#3498db')
            ax.hist(data, bins=15, color=color, alpha=0.75, edgecolor='white')
            ax.axvline(data.mean(), color='red',   linestyle='--', label=f'Mean {data.mean():.1f}')
            ax.axvline(100,         color='black', linestyle='--', alpha=0.5, label='Base 100')
            ax.set_xlabel('Index Value')
            ax.set_ylabel('# Cities')
            ax.set_title(title)
            ax.legend(fontsize=8)

        # Hide any unused subplots
        for ax in list(axes_flat)[len(all_cols):]:
            ax.set_visible(False)

        plt.tight_layout()
        path = f'{self.output_dir}/distribution.png'
        plt.savefig(path, dpi=150, bbox_inches='tight')
        print(f"Saved: {path}")
        plt.close()

    # ------------------------------------------------------------------
    # 4. Heatmap — all components, top 20 cities
    # ------------------------------------------------------------------
    def plot_heatmap(self, df):
        components = self._active_components(df)
        top20 = df.head(20)[['City'] + components].set_index('City')
        top20.columns = [self.COMPONENT_LABELS[c] for c in components]

        plt.figure(figsize=(len(components) * 1.6 + 2, 12))
        sns.heatmap(top20, annot=True, fmt='.1f', cmap='RdYlGn_r',
                    center=100, linewidths=0.4,
                    cbar_kws={'label': 'Index (Delhi = 100)'})
        plt.title('Cost Component Heatmap — Top 20 Cities (All Components)')
        plt.tight_layout()
        path = f'{self.output_dir}/heatmap.png'
        plt.savefig(path, dpi=150, bbox_inches='tight')
        print(f"Saved: {path}")
        plt.close()

    # ------------------------------------------------------------------
    # 5. NEW — Restaurant prices: all 50 cities ranked
    # ------------------------------------------------------------------
    def plot_restaurant_prices(self, df):
        if 'restaurant_index' not in df.columns:
            print("No restaurant data — skipping chart.")
            return

        sorted_df = df.sort_values('restaurant_index', ascending=True)
        colors = ['#e74c3c' if v >= 100 else '#27ae60'
                  for v in sorted_df['restaurant_index']]

        fig, ax = plt.subplots(figsize=(10, 14))
        ax.barh(sorted_df['City'], sorted_df['restaurant_index'], color=colors)
        ax.axvline(100, color='black', linestyle='--', linewidth=1.2, label='Delhi = 100')
        ax.set_xlabel('Restaurant Price Index')
        ax.set_title('Restaurant Cost Index — All 50 Cities\n(Red = pricier than Delhi, Green = cheaper)')
        ax.legend()
        plt.tight_layout()
        path = f'{self.output_dir}/restaurant_index.png'
        plt.savefig(path, dpi=150, bbox_inches='tight')
        print(f"Saved: {path}")
        plt.close()

    # ------------------------------------------------------------------
    # 6. NEW — Movie ticket prices: all 50 cities ranked
    # ------------------------------------------------------------------
    def plot_movie_ticket_prices(self, df):
        if 'movie_index' not in df.columns:
            print("No movie ticket data — skipping chart.")
            return

        sorted_df = df.sort_values('movie_index', ascending=True)
        colors = ['#e74c3c' if v >= 100 else '#27ae60'
                  for v in sorted_df['movie_index']]

        fig, ax = plt.subplots(figsize=(10, 14))
        ax.barh(sorted_df['City'], sorted_df['movie_index'], color=colors)
        ax.axvline(100, color='black', linestyle='--', linewidth=1.2, label='Delhi = 100')
        ax.set_xlabel('Movie Ticket Price Index')
        ax.set_title('Movie Ticket Price Index — All 50 Cities\n(Red = pricier than Delhi, Green = cheaper)')
        ax.legend()
        plt.tight_layout()
        path = f'{self.output_dir}/movie_ticket_index.png'
        plt.savefig(path, dpi=150, bbox_inches='tight')
        print(f"Saved: {path}")
        plt.close()

    # ------------------------------------------------------------------
    # 8. NEW — Electricity rates: all 50 cities ranked
    # ------------------------------------------------------------------
    def plot_electricity_rates(self, df):
        if 'electricity_index' not in df.columns:
            print("No electricity data — skipping chart.")
            return

        sorted_df = df.sort_values('electricity_index', ascending=True)
        colors = ['#e74c3c' if v >= 100 else '#27ae60'
                  for v in sorted_df['electricity_index']]

        fig, ax = plt.subplots(figsize=(10, 14))
        ax.barh(sorted_df['City'], sorted_df['electricity_index'], color=colors)
        ax.axvline(100, color='black', linestyle='--', linewidth=1.2, label='Delhi = 100')
        ax.set_xlabel('Electricity Rate Index')
        ax.set_title('Electricity Rate Index — All 50 Cities\n(Red = pricier than Delhi, Green = cheaper)')
        ax.legend()
        plt.tight_layout()
        path = f'{self.output_dir}/electricity_index.png'
        plt.savefig(path, dpi=150, bbox_inches='tight')
        print(f"Saved: {path}")
        plt.close()
    def plot_entertainment_vs_dining(self, df):
        has_rest  = 'restaurant_index' in df.columns
        has_movie = 'movie_index'      in df.columns
        if not (has_rest or has_movie):
            return

        sorted_df = df.sort_values('cost_of_living_index', ascending=False)
        x = np.arange(len(sorted_df))
        width = 0.4

        fig, ax = plt.subplots(figsize=(18, 7))
        if has_rest:
            ax.bar(x - width/2, sorted_df['restaurant_index'], width,
                   label='Restaurants', color='#e67e22', alpha=0.85)
        if has_movie:
            ax.bar(x + width/2, sorted_df['movie_index'], width,
                   label='Movies', color='#e91e63', alpha=0.85)

        ax.axhline(100, color='black', linestyle='--', alpha=0.5, label='Delhi = 100')
        ax.set_xticks(x)
        ax.set_xticklabels(sorted_df['City'], rotation=90, fontsize=8)
        ax.set_ylabel('Index (Delhi = 100)')
        ax.set_title('Dining & Entertainment Cost Index — All 50 Cities')
        ax.legend()
        plt.tight_layout()
        path = f'{self.output_dir}/dining_entertainment.png'
        plt.savefig(path, dpi=150, bbox_inches='tight')
        print(f"Saved: {path}")
        plt.close()
