"""
FastAPI REST API Server for India Cost of Living Index & Smart City Recommender.
Includes AI Copilot, Geospatial Queries, Salary Swap Parity, and ML Archetypes.
"""
import time
import sys
import os
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.schemas import (
    CategoryWeights,
    RecommendationRequest,
    RecommendationResponse,
    CitySummary,
    PCAAnalyticsResponse,
    HealthResponse,
    AIPromptRequest,
    AIPromptResponse,
    AIRelocationRequest,
    AIRelocationResponse,
    SalarySwapRequest,
    SalarySwapResponse,
    SpatialProximityResponse,
    CityComparisonResponse
)
from api.services import get_service, RecommenderService

app = FastAPI(
    title="India Cost of Living & Smart City Recommender API",
    description="High-performance REST API with AI Relocation Assistance, Spatial Distance Engine, Salary Parity, and ML Archetypes.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for full-stack frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = round((time.perf_counter() - start_time) * 1000, 3)
    response.headers["X-Process-Time-Ms"] = str(process_time)
    return response


@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
def health_check(service: RecommenderService = Depends(get_service)):
    """Health check endpoint confirming API status and loaded city datasets."""
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        cities_loaded=service.get_city_count()
    )


@app.get("/api/v1/cities", response_model=List[CitySummary], tags=["Cities"])
def list_cities(service: RecommenderService = Depends(get_service)):
    """Retrieve all 50 Indian cities with baseline cost of living index scores."""
    return service.get_all_cities()


@app.get("/api/v1/cities/compare", response_model=CityComparisonResponse, tags=["Cities"])
def compare_cities(
    city1: str = Query(..., example="Mumbai"),
    city2: str = Query(..., example="Indore"),
    service: RecommenderService = Depends(get_service)
):
    """Side-by-side category cost comparison between any two cities."""
    try:
        return service.get_city_comparison(city1, city2)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/v1/cities/{city_name}", tags=["Cities"])
def get_city_details(city_name: str, service: RecommenderService = Depends(get_service)):
    """Retrieve detailed expense category breakdown for a specific city."""
    city_data = service.get_city_by_name(city_name)
    if not city_data:
        raise HTTPException(status_code=404, detail=f"City '{city_name}' not found in dataset.")
    return city_data


@app.post("/api/v1/recommend", response_model=RecommendationResponse, tags=["Recommender"])
def recommend_cities(
    payload: RecommendationRequest,
    service: RecommenderService = Depends(get_service)
):
    """
    Generate personalized city cost recommendations based on custom priority weights.
    Returns ranked cities, normalized weights, and execution query times.
    """
    return service.recommend(weights=payload.weights, top_k=payload.top_k)


# ==================== NEW AI & ADVANCED ENDPOINTS ====================

@app.post("/api/v1/ai/parse-prompt", response_model=AIPromptResponse, tags=["AI Copilot"])
def parse_ai_prompt(
    payload: AIPromptRequest,
    service: RecommenderService = Depends(get_service)
):
    """Parse natural language lifestyle prompt into CategoryWeights and extracted budget metrics."""
    return service.parse_ai_prompt(payload.prompt)


@app.post("/api/v1/ai/relocation-insight", response_model=AIRelocationResponse, tags=["AI Copilot"])
def get_ai_relocation_insight(
    payload: AIRelocationRequest,
    service: RecommenderService = Depends(get_service)
):
    """Generate executive AI relocation report with purchasing power parity & monthly savings."""
    try:
        return service.get_ai_relocation_insight(payload.current_city, payload.target_city, payload.current_salary_lpa)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/v1/salary-swap", response_model=SalarySwapResponse, tags=["Salary Calculator"])
def calculate_salary_swap(
    payload: SalarySwapRequest,
    service: RecommenderService = Depends(get_service)
):
    """Calculate Purchasing Power Parity (PPP) equivalent salary between any two cities."""
    try:
        return service.get_salary_swap(payload.current_city, payload.target_city, payload.current_salary_lpa)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/v1/spatial/nearby", response_model=SpatialProximityResponse, tags=["Geospatial Engine"])
def get_nearby_cities(
    center_city: str = Query(..., example="Bengaluru"),
    radius_km: float = Query(300.0, ge=10.0, le=2000.0),
    service: RecommenderService = Depends(get_service)
):
    """Find all cities within radius_km of center_city with cost savings analysis."""
    return service.get_spatial_nearby(center_city, radius_km)


@app.get("/api/v1/ai/city-archetypes", tags=["Analytics & ML"])
def get_ml_archetypes(service: RecommenderService = Depends(get_service)):
    """Retrieve ML K-Means city archetype clusters and price anomaly reports."""
    return service.get_ml_archetypes()


@app.get("/api/v1/analytics/pca", response_model=PCAAnalyticsResponse, tags=["Analytics & ML"])
def get_pca_analytics(service: RecommenderService = Depends(get_service)):
    """Retrieve PCA variance components, factor loadings, and top expense drivers."""
    return service.get_pca_analytics()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
