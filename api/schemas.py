"""
Pydantic schemas for FastAPI REST API endpoints.
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class CategoryWeights(BaseModel):
    Housing: int = Field(default=5, ge=1, le=10, description="Priority weight for Housing (1=Lowest, 10=Highest)")
    Grocery: int = Field(default=5, ge=1, le=10, description="Priority weight for Grocery (1=Lowest, 10=Highest)")
    Transport: int = Field(default=5, ge=1, le=10, description="Priority weight for Transport (1=Lowest, 10=Highest)")
    Healthcare: int = Field(default=5, ge=1, le=10, description="Priority weight for Healthcare (1=Lowest, 10=Highest)")
    Education: int = Field(default=5, ge=1, le=10, description="Priority weight for Education (1=Lowest, 10=Highest)")
    Electricity: int = Field(default=5, ge=1, le=10, description="Priority weight for Electricity (1=Lowest, 10=Highest)")
    Restaurant: int = Field(default=5, ge=1, le=10, description="Priority weight for Restaurant (1=Lowest, 10=Highest)")
    Movies: int = Field(default=5, ge=1, le=10, description="Priority weight for Movies (1=Lowest, 10=Highest)")


class RecommendationRequest(BaseModel):
    weights: CategoryWeights = Field(default_factory=CategoryWeights)
    top_k: int = Field(default=5, ge=1, le=50, description="Number of recommended cities to return")


class CityDetail(BaseModel):
    rank: int
    city: str
    custom_index: float
    official_index: Optional[float] = None
    tier: Optional[str] = None
    state: Optional[str] = None
    categories: Dict[str, float]


class RecommendationResponse(BaseModel):
    query_time_ms: float
    cached: bool
    top_k: int
    total_cities_evaluated: int
    normalized_weights: Dict[str, float]
    recommendations: List[CityDetail]


class CitySummary(BaseModel):
    city: str
    cost_of_living_index: float
    tier: Optional[str] = None
    state: Optional[str] = None
    housing_index: float
    grocery_index: float
    transport_index: float


class PCAAnalyticsResponse(BaseModel):
    n_components: int
    total_variance_explained: float
    explained_variance_ratio: Dict[str, float]
    top_cost_drivers: List[str]


class HealthResponse(BaseModel):
    status: str
    version: str
    cities_loaded: int


# ==================== NEW AI & EXTENDED SCHEMAS ====================

class AIPromptRequest(BaseModel):
    prompt: str = Field(..., description="Natural language lifestyle / budget prompt", example="I am a software engineer earning 15 LPA, I have 2 school kids, prefer low rent and top schools.")


class AIPromptResponse(BaseModel):
    prompt: str
    weights: CategoryWeights
    extracted_salary_lpa: Optional[float] = None
    detected_lifestyle: List[str]
    ai_summary: str


class AIRelocationRequest(BaseModel):
    current_city: str = Field(default="Delhi")
    target_city: str = Field(default="Bengaluru")
    current_salary_lpa: float = Field(default=15.0, ge=1.0)


class AIRelocationResponse(BaseModel):
    current_city: str
    target_city: str
    verdict: str
    financial_advice: str
    current_salary_lpa: float
    equivalent_salary_lpa: float
    monthly_savings_rupees: float
    overall_index_diff_pct: float
    key_tradeoffs: List[str]


class SalarySwapRequest(BaseModel):
    current_city: str = Field(..., example="Mumbai")
    target_city: str = Field(..., example="Indore")
    current_salary_lpa: float = Field(default=12.0, ge=0.5)


class SalarySwapResponse(BaseModel):
    current_city: str
    target_city: str
    current_salary_lpa: float
    equivalent_salary_lpa: float
    annual_difference_lpa: float
    monthly_savings_rupees: float
    cost_of_living_diff_pct: float
    category_breakdown: Dict[str, Dict[str, float]]


class SpatialCityDetail(BaseModel):
    city: str
    distance_km: float
    cost_of_living_index: float
    base_city_index: float
    savings_vs_base_pct: float
    tier: Optional[str] = None
    state: Optional[str] = None
    housing_index: float
    latitude: float
    longitude: float


class SpatialProximityResponse(BaseModel):
    center_city: str
    radius_km: float
    cities_found: int
    results: List[SpatialCityDetail]


class CityComparisonResponse(BaseModel):
    city1: str
    city2: str
    overall_index_1: float
    overall_index_2: float
    cheaper_city: str
    overall_diff_pct: float
    categories_comparison: Dict[str, Dict[str, Any]]
