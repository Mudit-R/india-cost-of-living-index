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
    print("\n2. Test Scenario: High Housing and Grocery priority")
    priorities = {
        'Housing': 10,
        'Grocery': 8,
        'Transport': 5,
        'Healthcare': 5,
        'Education': 5,
        'Electricity': 3,
        'Restaurant': 2,
        'Movies': 1
    }
    
    recs, norm_w = recommender.get_recommendations(priorities, top_n=5)
    print(f"   ✓ Generated {len(recs)} recommendations")
    print("\n   Top 5 Cities:")
    for rec in recs:
        print(f"   {rec['rank']}. {rec['city']}")
        print(f"      Custom Index: {rec['custom_index']:.1f}")
        print(f"      Overall Index: {rec['overall_index']:.1f}")
        print(f"      {rec['explanation'][:100]}...")
        print()
    
    # Test Scenario 2: High Education Priority
    print("\n3. Test Scenario: High Education Priority")
    priorities_edu = {cat: 5 for cat in CATEGORIES}
    priorities_edu['Education'] = 10
    
    recs, norm_w = recommender.get_recommendations(priorities_edu, top_n=5)
    print(f"   ✓ Generated {len(recs)} recommendations")
    print("\n   Top 5 Recommended Cities:")
    for rec in recs:
        print(f"   {rec['rank']}. {rec['city']} - Custom Index: {rec['custom_index']:.1f}")
    
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
