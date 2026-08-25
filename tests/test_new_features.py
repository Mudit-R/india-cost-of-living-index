"""
Pytest unit and integration tests for AI Copilot, Spatial Engine, Salary Calculator, and Cache.
"""
import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app
from src.ai_engine import AIRelocationParser, AIRelocationAdvisor
from src.cache_engine import MultiLayerCacheEngine

client = TestClient(app)


def test_ai_prompt_parser():
    prompt = "I am a software engineer earning 15 LPA, I have 2 school kids, need cheap housing and top schools."
    res = AIRelocationParser.parse_prompt(prompt)
    assert res["extracted_salary_lpa"] == 15.0
    assert res["weights"]["Housing"] >= 5
    assert res["weights"]["Education"] >= 7
    assert "Family & Education Focused" in res["detected_lifestyle"]


def test_ai_relocation_advisor():
    insight = AIRelocationAdvisor.generate_relocation_insight(
        current_city="Delhi",
        target_city="Indore",
        current_salary_lpa=12.0,
        current_city_index=100.0,
        target_city_index=75.0
    )
    assert insight["equivalent_salary_lpa"] == 9.0
    assert insight["monthly_savings_rupees"] > 0
    assert "Indore" in insight["verdict"]


def test_cache_engine_fallback():
    cache = MultiLayerCacheEngine()
    cache.set("test_key", {"data": 123})
    assert cache.get("test_key") == {"data": 123}


def test_api_ai_parse_prompt_endpoint():
    payload = {"prompt": "I am a dev earning 20 LPA, prefer cheap rent and metro commute."}
    response = client.post("/api/v1/ai/parse-prompt", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["extracted_salary_lpa"] == 20.0
    assert "weights" in data


def test_api_ai_relocation_insight_endpoint():
    payload = {
        "current_city": "Mumbai",
        "target_city": "Indore",
        "current_salary_lpa": 15.0
    }
    response = client.post("/api/v1/ai/relocation-insight", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "financial_advice" in data
    assert data["monthly_savings_rupees"] > 0


def test_api_salary_swap_endpoint():
    payload = {
        "current_city": "Delhi",
        "target_city": "Bengaluru",
        "current_salary_lpa": 10.0
    }
    response = client.post("/api/v1/salary-swap", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "equivalent_salary_lpa" in data
    assert "category_breakdown" in data


def test_api_spatial_nearby_endpoint():
    response = client.get("/api/v1/spatial/nearby?center_city=Bengaluru&radius_km=300")
    assert response.status_code == 200
    data = response.json()
    assert data["center_city"] == "Bengaluru"
    assert data["cities_found"] > 0


def test_api_city_compare_endpoint():
    response = client.get("/api/v1/cities/compare?city1=Mumbai&city2=Indore")
    assert response.status_code == 200
    data = response.json()
    assert data["cheaper_city"] == "Indore"
    assert "categories_comparison" in data


def test_api_ml_archetypes_endpoint():
    response = client.get("/api/v1/ai/city-archetypes")
    assert response.status_code == 200
    data = response.json()
    assert "archetype_clusters" in data
    assert "detected_anomalies" in data
