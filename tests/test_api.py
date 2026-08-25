"""
Pytest unit and integration tests for FastAPI REST API endpoints.
"""
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app

client = TestClient(app)


def test_health_check_endpoint():
    """Verify health check status and loaded city count."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["cities_loaded"] == 50
    assert "X-Process-Time-Ms" in response.headers


def test_list_cities_endpoint():
    """Verify list of 50 cities and baseline schema."""
    response = client.get("/api/v1/cities")
    assert response.status_code == 200
    cities = response.json()
    assert len(cities) == 50
    first_city = cities[0]
    assert "city" in first_city
    assert "cost_of_living_index" in first_city
    assert "housing_index" in first_city


def test_get_city_details_success():
    """Verify city detail endpoint for Delhi."""
    response = client.get("/api/v1/cities/Delhi")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Delhi"
    assert data["overall_index"] == 100.0
    assert "Housing" in data["categories"]


def test_get_city_details_not_found():
    """Verify 404 response for invalid city."""
    response = client.get("/api/v1/cities/NonExistentCityXYZ")
    assert response.status_code == 404


def test_recommendation_endpoint():
    """Verify recommendation POST endpoint with custom slider weights."""
    payload = {
        "weights": {
            "Housing": 10,
            "Grocery": 8,
            "Transport": 5,
            "Healthcare": 3,
            "Education": 5,
            "Electricity": 4,
            "Restaurant": 2,
            "Movies": 1
        },
        "top_k": 5
    }
    response = client.post("/api/v1/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["top_k"] == 5
    assert len(data["recommendations"]) == 5
    assert "query_time_ms" in data
    assert "normalized_weights" in data
    assert data["cached"] is False

    # Second call should hit LRU cache
    response_cached = client.post("/api/v1/recommend", json=payload)
    assert response_cached.status_code == 200
    data_cached = response_cached.json()
    assert data_cached["cached"] is True


def test_pca_analytics_endpoint():
    """Verify PCA analytics endpoint."""
    response = client.get("/api/v1/analytics/pca")
    assert response.status_code == 200
    data = response.json()
    assert data["n_components"] == 2
    assert "total_variance_explained" in data
    assert len(data["top_cost_drivers"]) > 0
