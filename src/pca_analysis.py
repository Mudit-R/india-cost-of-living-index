"""
PCA Analysis for Cost of Living Index
Applies Principal Component Analysis to understand cost patterns across cities
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def load_data():
    """Load the cost index results"""
    df = pd.read_csv('../outputs/reports/cost_index_results.csv')
    return df

def perform_pca_analysis(df):
    """Perform PCA on cost components"""
    
    # Select the 8 cost component indices
    components = [
        'housing_index', 'grocery_index', 'transport_index', 
        'healthcare_index', 'electricity_index', 'restaurant_index',
        'movie_index', 'education_index'
    ]
    
    X = df[components].values
    cities = df['City'].values
    
    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Apply PCA
    pca = PCA()
    X_pca = pca.fit_transform(X_scaled)
    
    return pca, X_pca, X_scaled, cities, components

def plot_explained_variance(pca):
    """Plot explained variance ratio"""
    plt.figure(figsize=(12, 5))
    
    # Subplot 1: Explained variance per component
    plt.subplot(1, 2, 1)
    plt.bar(range(1, len(pca.explained_variance_ratio_) + 1), 
            pca.explained_variance_ratio_ * 100)
    plt.xlabel('Principal Component')
    plt.ylabel('Explained Variance (%)')
    plt.title('Explained Variance by Principal Component')
    plt.xticks(range(1, len(pca.explained_variance_ratio_) + 1))
    
    # Add percentage labels on bars
    for i, v in enumerate(pca.explained_variance_ratio_ * 100):
        plt.text(i + 1, v + 1, f'{v:.1f}%', ha='center', va='bottom')
    
    # Subplot 2: Cumulative explained variance
    plt.subplot(1, 2, 2)
    cumsum = np.cumsum(pca.explained_variance_ratio_ * 100)
    plt.plot(range(1, len(cumsum) + 1), cumsum, 'bo-')
    plt.axhline(y=80, color='r', linestyle='--', label='80% threshold')
    plt.axhline(y=90, color='g', linestyle='--', label='90% threshold')
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative Explained Variance (%)')
    plt.title('Cumulative Explained Variance')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(range(1, len(cumsum) + 1))
    
    plt.tight_layout()
    plt.savefig('../outputs/visualizations/pca_explained_variance.png', dpi=300, bbox_inches='tight')
    print("Saved: ../outputs/visualizations/pca_explained_variance.png")
    plt.close()

def plot_component_loadings(pca, components):
    """Plot component loadings (feature importance)"""
    plt.figure(figsize=(14, 10))
    
    # Plot first 4 principal components
    for i in range(min(4, len(pca.components_))):
        plt.subplot(2, 2, i + 1)
        loadings = pca.components_[i]
        
        # Sort by absolute value
        sorted_idx = np.argsort(np.abs(loadings))[::-1]
        sorted_components = [components[j] for j in sorted_idx]
        sorted_loadings = loadings[sorted_idx]
        
        colors = ['red' if x < 0 else 'green' for x in sorted_loadings]
        plt.barh(sorted_components, sorted_loadings, color=colors, alpha=0.7)
        plt.xlabel('Loading Value')
        plt.title(f'PC{i+1} Loadings ({pca.explained_variance_ratio_[i]*100:.1f}% variance)')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        plt.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('../outputs/visualizations/pca_component_loadings.png', dpi=300, bbox_inches='tight')
    print("Saved: ../outputs/visualizations/pca_component_loadings.png")
    plt.close()

def plot_2d_projection(X_pca, cities, df):
    """Plot cities in 2D PCA space"""
    plt.figure(figsize=(16, 12))
    
    # Get overall cost index for color coding
    cost_index = df['cost_of_living_index'].values
    
    # Create scatter plot
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], 
                         c=cost_index, cmap='RdYlGn_r', 
                         s=200, alpha=0.7, edgecolors='black', linewidth=1)
    
    # Add city labels
    for i, city in enumerate(cities):
        plt.annotate(city, (X_pca[i, 0], X_pca[i, 1]), 
                    fontsize=8, ha='center', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    plt.xlabel('First Principal Component (PC1)', fontsize=12)
    plt.ylabel('Second Principal Component (PC2)', fontsize=12)
    plt.title('Cities Projected onto First Two Principal Components\n(Color = Cost of Living Index)', 
              fontsize=14, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Cost of Living Index', rotation=270, labelpad=20)
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../outputs/visualizations/pca_2d_projection.png', dpi=300, bbox_inches='tight')
    print("Saved: ../outputs/visualizations/pca_2d_projection.png")
    plt.close()

def plot_3d_projection(X_pca, cities, df):
    """Plot cities in 3D PCA space"""
    from mpl_toolkits.mplot3d import Axes3D
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    cost_index = df['cost_of_living_index'].values
    
    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], X_pca[:, 2],
                        c=cost_index, cmap='RdYlGn_r',
                        s=200, alpha=0.7, edgecolors='black', linewidth=1)
    
    # Add labels for top/bottom cities
    top_5_idx = np.argsort(cost_index)[-5:]
    bottom_5_idx = np.argsort(cost_index)[:5]
    
    for idx in np.concatenate([top_5_idx, bottom_5_idx]):
        ax.text(X_pca[idx, 0], X_pca[idx, 1], X_pca[idx, 2], 
               cities[idx], fontsize=8)
    
    ax.set_xlabel('PC1', fontsize=12)
    ax.set_ylabel('PC2', fontsize=12)
    ax.set_zlabel('PC3', fontsize=12)
    ax.set_title('Cities in 3D PCA Space\n(Top 5 & Bottom 5 labeled)', 
                fontsize=14, fontweight='bold')
    
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label('Cost of Living Index', rotation=270, labelpad=20)
    
    plt.tight_layout()
    plt.savefig('../outputs/visualizations/pca_3d_projection.png', dpi=300, bbox_inches='tight')
    print("Saved: ../outputs/visualizations/pca_3d_projection.png")
    plt.close()

def perform_clustering_on_pca(X_pca, cities, df, n_clusters=4):
    """Perform K-means clustering on PCA-reduced data"""
    
    # Use first 3 principal components
    X_reduced = X_pca[:, :3]
    
    # K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_reduced)
    
    # Add clusters to dataframe
    df_clustered = df.copy()
    df_clustered['cluster'] = clusters
    
    # Plot clusters
    plt.figure(figsize=(16, 12))
    
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    
    for cluster in range(n_clusters):
        mask = clusters == cluster
        plt.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                   c=colors[cluster], label=f'Cluster {cluster+1}',
                   s=200, alpha=0.7, edgecolors='black', linewidth=1)
        
        # Add city labels
        for i, city in enumerate(cities[mask]):
            idx = np.where(cities == city)[0][0]
            plt.annotate(city, (X_pca[idx, 0], X_pca[idx, 1]), 
                        fontsize=8, ha='center', va='bottom',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    plt.xlabel('First Principal Component (PC1)', fontsize=12)
    plt.ylabel('Second Principal Component (PC2)', fontsize=12)
    plt.title(f'City Clusters Based on PCA ({n_clusters} clusters)', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../outputs/visualizations/pca_clustering.png', dpi=300, bbox_inches='tight')
    print("Saved: ../outputs/visualizations/pca_clustering.png")
    plt.close()
    
    return df_clustered

def print_cluster_analysis(df_clustered):
    """Print analysis of each cluster"""
    print("\n" + "="*80)
    print("CLUSTER ANALYSIS")
    print("="*80)
    
    for cluster in sorted(df_clustered['cluster'].unique()):
        cluster_cities = df_clustered[df_clustered['cluster'] == cluster]
        
        print(f"\n{'='*80}")
        print(f"CLUSTER {cluster + 1} ({len(cluster_cities)} cities)")
        print(f"{'='*80}")
        
        print(f"\nCities: {', '.join(cluster_cities['City'].values)}")
        
        print(f"\nAverage Cost Index: {cluster_cities['cost_of_living_index'].mean():.2f}")
        print(f"Range: {cluster_cities['cost_of_living_index'].min():.2f} - {cluster_cities['cost_of_living_index'].max():.2f}")
        
        print("\nAverage Component Indices:")
        components = ['housing_index', 'grocery_index', 'transport_index', 
                     'healthcare_index', 'electricity_index', 'restaurant_index',
                     'movie_index', 'education_index']
        
        for comp in components:
            avg = cluster_cities[comp].mean()
            print(f"  {comp.replace('_index', '').capitalize():15s}: {avg:6.2f}")

def create_biplot(pca, X_scaled, X_pca, cities, components, df):
    """Create a biplot showing both cities and component vectors"""
    plt.figure(figsize=(16, 12))
    
    # Plot cities
    cost_index = df['cost_of_living_index'].values
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], 
                         c=cost_index, cmap='RdYlGn_r',
                         s=150, alpha=0.6, edgecolors='black', linewidth=0.5)
    
    # Plot component vectors
    scale = 3.5
    for i, comp in enumerate(components):
        plt.arrow(0, 0, 
                 pca.components_[0, i] * scale, 
                 pca.components_[1, i] * scale,
                 head_width=0.15, head_length=0.15, 
                 fc='red', ec='red', linewidth=2, alpha=0.8)
        
        plt.text(pca.components_[0, i] * scale * 1.15, 
                pca.components_[1, i] * scale * 1.15,
                comp.replace('_index', '').capitalize(),
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    # Add labels for extreme cities
    top_5_idx = np.argsort(cost_index)[-5:]
    bottom_5_idx = np.argsort(cost_index)[:5]
    
    for idx in np.concatenate([top_5_idx, bottom_5_idx]):
        plt.annotate(cities[idx], (X_pca[idx, 0], X_pca[idx, 1]), 
                    fontsize=9, ha='center', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)', fontsize=12)
    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)', fontsize=12)
    plt.title('PCA Biplot: Cities and Cost Components\n(Red arrows = component directions)', 
              fontsize=14, fontweight='bold')
    
    cbar = plt.colorbar(scatter)
    cbar.set_label('Cost of Living Index', rotation=270, labelpad=20)
    
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    plt.tight_layout()
    plt.savefig('../outputs/visualizations/pca_biplot.png', dpi=300, bbox_inches='tight')
    print("Saved: ../outputs/visualizations/pca_biplot.png")
    plt.close()

def main():
    """Main execution function"""
    print("="*80)
    print("PCA ANALYSIS - COST OF LIVING INDEX")
    print("="*80)
    
    # Load data
    print("\n[1/7] Loading data...")
    df = load_data()
    print(f"  ✓ Loaded data for {len(df)} cities")
    
    # Perform PCA
    print("\n[2/7] Performing PCA analysis...")
    pca, X_pca, X_scaled, cities, components = perform_pca_analysis(df)
    print(f"  ✓ PCA completed")
    
    # Print explained variance
    print("\n" + "="*80)
    print("EXPLAINED VARIANCE BY PRINCIPAL COMPONENTS")
    print("="*80)
    for i, var in enumerate(pca.explained_variance_ratio_):
        cumsum = np.sum(pca.explained_variance_ratio_[:i+1])
        print(f"PC{i+1}: {var*100:6.2f}%  (Cumulative: {cumsum*100:6.2f}%)")
    
    # Print component loadings
    print("\n" + "="*80)
    print("PRINCIPAL COMPONENT LOADINGS (PC1 & PC2)")
    print("="*80)
    print(f"\n{'Component':<20} {'PC1':>10} {'PC2':>10}")
    print("-" * 42)
    for i, comp in enumerate(components):
        print(f"{comp:<20} {pca.components_[0, i]:>10.3f} {pca.components_[1, i]:>10.3f}")
    
    # Generate visualizations
    print("\n[3/7] Plotting explained variance...")
    plot_explained_variance(pca)
    
    print("\n[4/7] Plotting component loadings...")
    plot_component_loadings(pca, components)
    
    print("\n[5/7] Creating 2D projection...")
    plot_2d_projection(X_pca, cities, df)
    
    print("\n[6/7] Creating 3D projection...")
    plot_3d_projection(X_pca, cities, df)
    
    print("\n[7/7] Creating biplot...")
    create_biplot(pca, X_scaled, X_pca, cities, components, df)
    
    # Clustering analysis
    print("\n[8/8] Performing clustering on PCA components...")
    df_clustered = perform_clustering_on_pca(X_pca, cities, df, n_clusters=4)
    print_cluster_analysis(df_clustered)
    
    # Save clustered data
    df_clustered.to_csv('../outputs/reports/cost_index_with_clusters.csv', index=False)
    print("\n  ✓ Saved clustered data to: ../outputs/reports/cost_index_with_clusters.csv")
    
    print("\n" + "="*80)
    print("✓ PCA ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated visualizations:")
    print("  - pca_explained_variance.png")
    print("  - pca_component_loadings.png")
    print("  - pca_2d_projection.png")
    print("  - pca_3d_projection.png")
    print("  - pca_biplot.png")
    print("  - pca_clustering.png")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
