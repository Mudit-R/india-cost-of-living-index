#!/usr/bin/env python3
"""
Machine Learning Demo for Cost of Living Index
Demonstrates practical ML applications on the dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score, silhouette_score
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

class CostOfLivingML:
    """ML applications for Cost of Living analysis"""
    
    def __init__(self, data_file='cost_index_results.csv'):
        self.df = pd.read_csv(data_file)
        self.features = ['housing_index', 'grocery_index', 'transport_index', 
                        'healthcare_index', 'fuel_index']
        self.scaler = StandardScaler()
        
    def city_clustering(self, n_clusters=4):
        """Cluster cities based on cost patterns"""
        print("\n" + "="*80)
        print("1. CITY CLUSTERING ANALYSIS")
        print("="*80)
        
        # Prepare data
        X = self.df[self.features]
        X_scaled = self.scaler.fit_transform(X)
        
        # Find optimal clusters using elbow method
        inertias = []
        silhouette_scores = []
        K_range = range(2, 8)
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
        
        # Perform clustering with chosen k
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.df['cluster'] = kmeans.fit_predict(X_scaled)
        
        # Analyze clusters
        print(f"\nClustering with {n_clusters} clusters:")
        print(f"Silhouette Score: {silhouette_score(X_scaled, self.df['cluster']):.3f}")
        
        print("\nCluster Statistics:")
        for i in range(n_clusters):
            cluster_cities = self.df[self.df['cluster'] == i]
            print(f"\n  Cluster {i} ({len(cluster_cities)} cities):")
            print(f"    Avg Cost Index: {cluster_cities['cost_of_living_index'].mean():.2f}")
            print(f"    Cities: {', '.join(cluster_cities['City'].head(5).tolist())}")
            if len(cluster_cities) > 5:
                print(f"            ... and {len(cluster_cities)-5} more")
        
        # Visualize clusters
        self._plot_clusters(X_scaled, n_clusters)
        
        return self.df['cluster']
    
    def _plot_clusters(self, X_scaled, n_clusters):
        """Visualize clusters using PCA"""
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], 
                            c=self.df['cluster'], cmap='viridis', 
                            s=200, alpha=0.6, edgecolors='black')
        
        # Add city labels for notable cities
        for idx, row in self.df.iterrows():
            if row['cost_of_living_index'] > 100 or row['cost_of_living_index'] < 60:
                plt.annotate(row['City'], (X_pca[idx, 0], X_pca[idx, 1]),
                           fontsize=8, alpha=0.7)
        
        plt.colorbar(scatter, label='Cluster')
        plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
        plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
        plt.title('City Clusters (PCA Visualization)')
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig('ml_city_clusters.png', dpi=300, bbox_inches='tight')
        print("\n  ✅ Saved: ml_city_clusters.png")
    
    def cost_prediction(self):
        """Predict cost of living using ML"""
        print("\n" + "="*80)
        print("2. COST PREDICTION MODEL")
        print("="*80)
        
        # Prepare data - predict overall cost from components
        X = self.df[self.features]
        y = self.df['cost_of_living_index']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X, y, cv=5, 
                                    scoring='neg_mean_absolute_error')
        
        print(f"\nModel Performance:")
        print(f"  Mean Absolute Error: {mae:.2f}")
        print(f"  R² Score: {r2:.3f}")
        print(f"  Cross-Val MAE: {-cv_scores.mean():.2f} (±{cv_scores.std():.2f})")
        
        # Feature importance
        print(f"\nFeature Importance:")
        importances = sorted(zip(self.features, model.feature_importances_), 
                           key=lambda x: x[1], reverse=True)
        for feature, importance in importances:
            print(f"  {feature:20s}: {importance:.3f} {'█' * int(importance*50)}")
        
        # Visualize predictions
        self._plot_predictions(y_test, y_pred)
        
        return model
    
    def _plot_predictions(self, y_test, y_pred):
        """Visualize prediction accuracy"""
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred, alpha=0.6, s=100, edgecolors='black')
        plt.plot([y_test.min(), y_test.max()], 
                [y_test.min(), y_test.max()], 
                'r--', lw=2, label='Perfect Prediction')
        plt.xlabel('Actual Cost Index')
        plt.ylabel('Predicted Cost Index')
        plt.title('Cost Prediction: Actual vs Predicted')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig('ml_cost_prediction.png', dpi=300, bbox_inches='tight')
        print("\n  ✅ Saved: ml_cost_prediction.png")
    
    def city_recommender(self, city_name, n=5):
        """Recommend similar cities"""
        print("\n" + "="*80)
        print("3. CITY RECOMMENDATION SYSTEM")
        print("="*80)
        
        # Calculate similarity
        features_matrix = self.df[self.features].values
        similarities = cosine_similarity(features_matrix)
        
        # Get city index
        try:
            city_idx = self.df[self.df['City'] == city_name].index[0]
        except IndexError:
            print(f"City '{city_name}' not found!")
            return None
        
        # Get similar cities
        similar_indices = similarities[city_idx].argsort()[-n-1:-1][::-1]
        recommendations = self.df.iloc[similar_indices][
            ['City', 'cost_of_living_index'] + self.features
        ]
        
        print(f"\nTop {n} cities similar to {city_name}:")
        print(f"(Based on cost component patterns)\n")
        
        for i, (idx, row) in enumerate(recommendations.iterrows(), 1):
            similarity = similarities[city_idx][idx]
            print(f"  {i}. {row['City']:<25} "
                  f"Index: {row['cost_of_living_index']:>6.2f}  "
                  f"Similarity: {similarity:.3f}")
        
        return recommendations
    
    def anomaly_detection(self):
        """Detect cities with unusual cost patterns"""
        print("\n" + "="*80)
        print("4. ANOMALY DETECTION")
        print("="*80)
        
        from sklearn.ensemble import IsolationForest
        
        # Prepare data
        X = self.df[self.features]
        X_scaled = self.scaler.fit_transform(X)
        
        # Detect anomalies
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        self.df['anomaly'] = iso_forest.fit_predict(X_scaled)
        self.df['anomaly_score'] = iso_forest.score_samples(X_scaled)
        
        # Find anomalies
        anomalies = self.df[self.df['anomaly'] == -1].sort_values('anomaly_score')
        
        print(f"\nDetected {len(anomalies)} anomalous cities:")
        print("(Cities with unusual cost patterns)\n")
        
        for idx, row in anomalies.iterrows():
            print(f"  • {row['City']:<25} "
                  f"Index: {row['cost_of_living_index']:>6.2f}  "
                  f"Anomaly Score: {row['anomaly_score']:>6.3f}")
            
            # Identify unusual components
            unusual = []
            for feat in self.features:
                if row[feat] > 150 or row[feat] < 30:
                    unusual.append(f"{feat.replace('_index', '')}: {row[feat]:.1f}")
            if unusual:
                print(f"    Unusual: {', '.join(unusual)}")
        
        return anomalies
    
    def feature_correlation_analysis(self):
        """Analyze correlations between features"""
        print("\n" + "="*80)
        print("5. FEATURE CORRELATION ANALYSIS")
        print("="*80)
        
        # Calculate correlations
        corr_matrix = self.df[self.features + ['cost_of_living_index']].corr()
        
        print("\nCorrelation with Overall Cost Index:")
        correlations = corr_matrix['cost_of_living_index'].drop('cost_of_living_index')
        correlations = correlations.sort_values(ascending=False)
        
        for feature, corr in correlations.items():
            print(f"  {feature:20s}: {corr:>6.3f} {'█' * int(abs(corr)*30)}")
        
        # Visualize correlation matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, linewidths=1)
        plt.title('Feature Correlation Matrix')
        plt.tight_layout()
        plt.savefig('ml_correlation_matrix.png', dpi=300, bbox_inches='tight')
        print("\n  ✅ Saved: ml_correlation_matrix.png")
        
        return corr_matrix

def main():
    """Run ML demo"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "MACHINE LEARNING DEMO - COST OF LIVING" + " "*20 + "║")
    print("╚" + "="*78 + "╝")
    
    # Initialize
    ml = CostOfLivingML()
    
    # 1. Clustering
    ml.city_clustering(n_clusters=4)
    
    # 2. Prediction
    model = ml.cost_prediction()
    
    # 3. Recommendations
    ml.city_recommender('Delhi', n=5)
    ml.city_recommender('Mumbai', n=5)
    
    # 4. Anomaly Detection
    ml.anomaly_detection()
    
    # 5. Correlation Analysis
    ml.feature_correlation_analysis()
    
    print("\n" + "="*80)
    print("✅ ML ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated Files:")
    print("  • ml_city_clusters.png - Cluster visualization")
    print("  • ml_cost_prediction.png - Prediction accuracy")
    print("  • ml_correlation_matrix.png - Feature correlations")
    print("\nNext Steps:")
    print("  • Collect temporal data for time series forecasting")
    print("  • Add external features (population, GDP, etc.)")
    print("  • Build production recommendation API")
    print("  • Deploy models for real-time predictions")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
