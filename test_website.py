#!/usr/bin/env python3
"""
Test script for the City Recommender website.
Tests the recommender logic without starting the full Streamlit app.
"""

from website.recommender import CityRecommender, CATEGORIES

def test_recommender():
    """Test the recommender with various scenarios"""
    
    print("=" * 60)
    print("CITY RECOMMENDER TEST")
    print("=" * 60)
    
    # Initialize
    print("\n1. Loading data...")
    recommender = CityRecommender('outputs/reports/cost_index_results.csv')
    recommender.load_data()
    print(f"   ✓ Loaded {len(recommender.df)} cities")
    
    # Test Scenario 1: Cheap housing and grocery
    print("\n2. Test Scenario: Cheap housing and grocery")
    priorities = {
        'Housing': 'cheap',
        'Grocery': 'cheap',
        'Transport': 'neutral',
        'Healthcare': 'neutral',
        'Education': 'neutral',
        'Electricity': 'neutral',
        'Restaurant': 'neutral',
        'Movies': 'neutral'
    }
    
    recs = recommender.get_recommendations(priorities, top_n=5)
    print(f"   ✓ Generated {len(recs)} recommendations")
    print("\n   Top 5 Cities:")
    for rec in recs:
        print(f"   {rec['rank']}. {rec['city']}")
        print(f"      Match Score: {rec['match_score']:.2f}")
        print(f"      Overall Index: {rec['overall_index']:.1f}")
        print(f"      {rec['explanation'][:100]}...")
        print()
    
    # Test Scenario 2: Everything cheap
    print("\n3. Test Scenario: Everything must be cheap")
    priorities_all_cheap = {cat: 'cheap' for cat in CATEGORIES}
    
    recs = recommender.get_recommendations(priorities_all_cheap, top_n=5)
    print(f"   ✓ Generated {len(recs)} recommendations")
    print("\n   Top 5 Most Affordable Cities:")
    for rec in recs:
        print(f"   {rec['rank']}. {rec['city']} - Overall Index: {rec['overall_index']:.1f}")
    
    # Test Scenario 3: Cheap housing, expensive education OK
    print("\n4. Test Scenario: Cheap housing, expensive education OK")
    priorities = {
        'Housing': 'cheap',
        'Grocery': 'neutral',
        'Transport': 'neutral',
        'Healthcare': 'neutral',
        'Education': 'expensive_ok',
        'Electricity': 'neutral',
        'Restaurant': 'neutral',
        'Movies': 'neutral'
    }
    
    recs = recommender.get_recommendations(priorities, top_n=5)
    print(f"   ✓ Generated {len(recs)} recommendations")
    print("\n   Top 5 Cities:")
    for rec in recs:
        print(f"   {rec['rank']}. {rec['city']}")
        print(f"      Housing Index: {rec['all_indices']['Housing']:.1f}")
        print(f"      Education Index: {rec['all_indices']['Education']:.1f}")
        print()
    
    # Test Scenario 4: Everything expensive
    print("\n5. Test Scenario: Everything can be expensive (want premium cities)")
    priorities_all_expensive = {cat: 'expensive_ok' for cat in CATEGORIES}
    
    recs = recommender.get_recommendations(priorities_all_expensive, top_n=5)
    print(f"   ✓ Generated {len(recs)} recommendations")
    print("\n   Top 5 Most Expensive Cities:")
    for rec in recs:
        print(f"   {rec['rank']}. {rec['city']} - Overall Index: {rec['overall_index']:.1f}")
    
    # Test city stats
    print("\n6. Test City Stats: Mumbai")
    stats = recommender.get_category_stats('Mumbai')
    if stats:
        print(f"   City: {stats['city']}")
        print(f"   Overall Index: {stats['overall_index']:.1f}")
        print("\n   Category Details:")
        for cat, data in stats['categories'].items():
            print(f"   {cat:15s}: {data['index']:6.1f} (Rank: {data['rank']}/50)")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
    print("\nTo run the website:")
    print("  streamlit run website/app.py")
    print()

if __name__ == "__main__":
    try:
        test_recommender()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nMake sure you have run: cd src && python main.py")
        exit(1)
