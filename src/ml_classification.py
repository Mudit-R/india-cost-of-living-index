#!/usr/bin/env python3
"""
ML Classification — Categorize cities into cost tiers using multiple algorithms
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression


class CityClassifier:
    def __init__(self, data_file='cost_index_results.csv'):
        self.df = pd.read_csv(data_file)
        self.features = [
            'housing_index', 'grocery_index', 'transport_index',
            'healthcare_index', 'electricity_index', 'restaurant_index', 'movie_index'
        ]
        # Filter to only features that exist
        self.features = [f for f in self.features if f in self.df.columns]
        self.scaler = StandardScaler()
        self.models = {}
        
    def create_labels(self):
        """Create city tier labels based on cost index"""
        print("\n" + "="*80)
        print("CREATING CITY TIER LABELS")
        print("="*80)
        
        # Define tiers based on cost index quartiles
        q25 = self.df['cost_of_living_index'].quantile(0.25)
        q50 = self.df['cost_of_living_index'].quantile(0.50)
        q75 = self.df['cost_of_living_index'].quantile(0.75)
        
        def assign_tier(index):
            if index < q25:
                return 'Budget'
            elif index < q50:
                return 'Affordable'
            elif index < q75:
                return 'Mid-Range'
            else:
                return 'Premium'
        
        self.df['tier'] = self.df['cost_of_living_index'].apply(assign_tier)
        
        print(f"\nTier Boundaries:")
        print(f"  Budget:     < {q25:.1f}")
        print(f"  Affordable: {q25:.1f} - {q50:.1f}")
        print(f"  Mid-Range:  {q50:.1f} - {q75:.1f}")
        print(f"  Premium:    > {q75:.1f}")
        
        print(f"\nTier Distribution:")
        for tier in ['Budget', 'Affordable', 'Mid-Range', 'Premium']:
            count = len(self.df[self.df['tier'] == tier])
            cities = self.df[self.df['tier'] == tier]['City'].tolist()
            print(f"  {tier:<12}: {count:>2} cities")
            print(f"               {', '.join(cities[:5])}")
            if len(cities) > 5:
                print(f"               ... and {len(cities)-5} more")
        
        return self.df['tier']
    
    def prepare_data(self):
        """Prepare features and labels for training"""
        X = self.df[self.features]
        y = self.df['tier']
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def train_all_models(self):
        """Train multiple classification algorithms"""
        print("\n" + "="*80)
        print("TRAINING CLASSIFICATION MODELS")
        print("="*80)
        
        X_train, X_test, y_train, y_test = self.prepare_data()
        
        # Define models
        models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(kernel='rbf', random_state=42),
            'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
            'Decision Tree': DecisionTreeClassifier(random_state=42),
            'Naive Bayes': GaussianNB(),
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        }
        
        results = []
        
        for name, model in models.items():
            # Train
            model.fit(X_train, y_train)
            self.models[name] = model
            
            # Predict
            y_pred = model.predict(X_test)
            
            # Evaluate
            accuracy = accuracy_score(y_test, y_pred)
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            
            results.append({
                'Model': name,
                'Test Accuracy': accuracy,
                'CV Mean': cv_scores.mean(),
                'CV Std': cv_scores.std()
            })
            
            print(f"\n{name}:")
            print(f"  Test Accuracy: {accuracy:.3f}")
            print(f"  CV Accuracy:   {cv_scores.mean():.3f} (±{cv_scores.std():.3f})")
        
        # Summary table
        results_df = pd.DataFrame(results).sort_values('Test Accuracy', ascending=False)
        
        print("\n" + "="*80)
        print("MODEL COMPARISON")
        print("="*80)
        print(results_df.to_string(index=False))
        
        # Best model
        best_model_name = results_df.iloc[0]['Model']
        best_accuracy = results_df.iloc[0]['Test Accuracy']
        
        print(f"\n🏆 Best Model: {best_model_name} (Accuracy: {best_accuracy:.3f})")
        
        return results_df, X_test, y_test
    
    def detailed_evaluation(self, model_name='Random Forest'):
        """Detailed evaluation of best model"""
        print("\n" + "="*80)
        print(f"DETAILED EVALUATION: {model_name}")
        print("="*80)
        
        X_train, X_test, y_train, y_test = self.prepare_data()
        model = self.models[model_name]
        y_pred = model.predict(X_test)
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(
            y_test, y_pred,
            target_names=self.label_encoder.classes_,
            digits=3
        ))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        self._plot_confusion_matrix(cm, self.label_encoder.classes_)
        
        # Feature importance (if available)
        if hasattr(model, 'feature_importances_'):
            print("\nFeature Importance:")
            importances = sorted(
                zip(self.features, model.feature_importances_),
                key=lambda x: x[1], reverse=True
            )
            for feature, importance in importances:
                bar = '█' * int(importance * 50)
                print(f"  {feature:<20}: {importance:.3f} {bar}")
            
            self._plot_feature_importance(importances)
    
    def _plot_confusion_matrix(self, cm, labels):
        """Plot confusion matrix"""
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=labels, yticklabels=labels,
                   cbar_kws={'label': 'Count'})
        plt.xlabel('Predicted Tier')
        plt.ylabel('Actual Tier')
        plt.title('Confusion Matrix — City Tier Classification')
        plt.tight_layout()
        plt.savefig('ml_confusion_matrix.png', dpi=300, bbox_inches='tight')
        print("\n  ✅ Saved: ml_confusion_matrix.png")
        plt.close()
    
    def _plot_feature_importance(self, importances):
        """Plot feature importance"""
        features, scores = zip(*importances)
        
        plt.figure(figsize=(10, 6))
        plt.barh(features, scores, color='steelblue', edgecolor='black')
        plt.xlabel('Importance Score')
        plt.title('Feature Importance — City Tier Classification')
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig('ml_feature_importance.png', dpi=300, bbox_inches='tight')
        print("  ✅ Saved: ml_feature_importance.png")
        plt.close()
    
    def predict_new_city(self, city_name, model_name='Random Forest'):
        """Predict tier for a specific city"""
        city_data = self.df[self.df['City'] == city_name]
        
        if city_data.empty:
            print(f"City '{city_name}' not found!")
            return None
        
        X = city_data[self.features]
        X_scaled = self.scaler.transform(X)
        
        model = self.models[model_name]
        prediction = model.predict(X_scaled)[0]
        probabilities = model.predict_proba(X_scaled)[0] if hasattr(model, 'predict_proba') else None
        
        predicted_tier = self.label_encoder.inverse_transform([prediction])[0]
        actual_tier = city_data['tier'].values[0]
        
        print(f"\n{city_name}:")
        print(f"  Predicted Tier: {predicted_tier}")
        print(f"  Actual Tier:    {actual_tier}")
        print(f"  Cost Index:     {city_data['cost_of_living_index'].values[0]:.2f}")
        
        if probabilities is not None:
            print(f"\n  Class Probabilities:")
            for tier, prob in zip(self.label_encoder.classes_, probabilities):
                bar = '█' * int(prob * 30)
                print(f"    {tier:<12}: {prob:.3f} {bar}")
        
        return predicted_tier
    
    def compare_algorithms_visual(self, results_df):
        """Visualize algorithm comparison"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot 1: Test Accuracy
        ax1 = axes[0]
        ax1.barh(results_df['Model'], results_df['Test Accuracy'], 
                color='steelblue', edgecolor='black')
        ax1.set_xlabel('Test Accuracy')
        ax1.set_title('Model Comparison — Test Accuracy')
        ax1.set_xlim(0, 1)
        ax1.grid(axis='x', alpha=0.3)
        
        # Plot 2: CV Mean with error bars
        ax2 = axes[1]
        ax2.barh(results_df['Model'], results_df['CV Mean'],
                xerr=results_df['CV Std'], color='coral', 
                edgecolor='black', capsize=5)
        ax2.set_xlabel('Cross-Validation Accuracy')
        ax2.set_title('Model Comparison — CV Accuracy (±1 std)')
        ax2.set_xlim(0, 1)
        ax2.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('ml_algorithm_comparison.png', dpi=300, bbox_inches='tight')
        print("\n  ✅ Saved: ml_algorithm_comparison.png")
        plt.close()


def main():
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*18 + "ML CLASSIFICATION — CITY TIER PREDICTION" + " "*19 + "║")
    print("╚" + "="*78 + "╝")
    
    # Initialize
    classifier = CityClassifier()
    
    # Create labels
    classifier.create_labels()
    
    # Train all models
    results_df, X_test, y_test = classifier.train_all_models()
    
    # Detailed evaluation of best model
    best_model = results_df.iloc[0]['Model']
    classifier.detailed_evaluation(best_model)
    
    # Visualize comparison
    classifier.compare_algorithms_visual(results_df)
    
    # Test predictions on sample cities
    print("\n" + "="*80)
    print("SAMPLE PREDICTIONS")
    print("="*80)
    
    test_cities = ['Mumbai', 'Delhi', 'Bengaluru', 'Jaipur', 'Indore', 'Surat']
    for city in test_cities:
        if city in classifier.df['City'].values:
            classifier.predict_new_city(city, best_model)
    
    print("\n" + "="*80)
    print("✅ CLASSIFICATION COMPLETE!")
    print("="*80)
    print("\nGenerated Files:")
    print("  • ml_confusion_matrix.png - Classification accuracy by tier")
    print("  • ml_feature_importance.png - Most important cost factors")
    print("  • ml_algorithm_comparison.png - Model performance comparison")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
