# Smart City Cost Index & Recommender Platform

A full-stack analytics platform and high-performance microservice engine analyzing cost of living metrics across 50 Indian cities using multi-source scraped data (50K+ listings), automated ETL pipelines, PCA dimensionality reduction, and custom priority-matching algorithms.

```
                         ┌─────────────────────────┐
                         │   Streamlit Web Client  │
                         │    (Interactive UI)     │
                         └────────────┬────────────┘
                                      │ HTTP REST / JSON
                                      ▼
                         ┌─────────────────────────┐
                         │   FastAPI REST Engine   │
                         │   (Uvicorn / Async)     │
                         └─────┬─────────────┬─────┘
                               │             │
                      Cache Hit│             │ DB / Index Scan
                               ▼             ▼
                        ┌───────────┐   ┌───────────┐
                        │  LRU Key  │   │ Analytics │
                        │   Cache   │   │  Engine   │
                        └───────────┘   └───────────┘
```

---

## 🚀 Key Features

* **Full-Stack Architecture**: Decoupled FastAPI REST service with an interactive Streamlit UI frontend.
* **Sub-50ms Recommendation Engine**: Custom multi-attribute scoring algorithm with LRU query caching for low latency.
* **RESTful API Services**: Comprehensive OpenAPI endpoints (`/docs`) for city data, multi-criteria recommendation queries, and PCA variance metrics.
* **Docker Containerization**: Production multi-container orchestration via `docker-compose.yml`.
* **Automated Data Engineering**: Asynchronous Web Scraping (BeautifulSoup/Selenium) and NLP normalization across 50K+ real-estate, grocery, healthcare, and education listings.
* **PCA Dimensionality Reduction**: Identified Housing and Grocery as key variance drivers ($65\%$ explained variance) with a $0.93$ correlation to economic benchmarks.
* **CI/CD Integration**: Automated GitHub Actions workflow for linting and Pytest API verification.

---

## 🛠 Tech Stack

* **Backend & API**: Python 3.10+, FastAPI, Uvicorn, Pydantic v2
* **Frontend**: Streamlit, Folium (Leaflet Interactive Maps), Custom CSS
* **Data Science & ML**: Pandas, NumPy, Scikit-Learn (PCA & Clustering)
* **Storage & Caching**: CSV/Relational Storage, In-Memory LRU Cache
* **DevOps & Testing**: Docker, Docker Compose, Pytest, GitHub Actions CI/CD

---

## ⚡ Quick Start

### 1. Launch with Docker Compose (Recommended)
```bash
docker-compose up --build
```
* **FastAPI Swagger Docs**: `http://localhost:8000/docs`
* **Streamlit Web UI**: `http://localhost:8501`

### 2. Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI Backend Server
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Start Streamlit Frontend Client (in a separate terminal)
streamlit run website/app.py
```

---

## 📡 REST API Documentation

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/health` | `GET` | Service status & city dataset metadata |
| `/api/v1/cities` | `GET` | List all 50 cities with cost of living indices |
| `/api/v1/cities/{city_name}` | `GET` | Detailed category breakdown for a specific city |
| `/api/v1/recommend` | `POST` | Execute priority-weighted recommendation search |
| `/api/v1/analytics/pca` | `GET` | PCA component variance breakdown & factor loadings |

### Example Recommendation Request:
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/recommend' \
  -H 'Content-Type: application/json' \
  -d '{
  "weights": {
    "Housing": 10,
    "Grocery": 8,
    "Transport": 5,
    "Healthcare": 5,
    "Education": 5,
    "Electricity": 3,
    "Restaurant": 2,
    "Movies": 1
  },
  "top_k": 5
}'
```

---

## 🧪 Running Tests

Execute the automated Pytest suite:
```bash
pytest tests/ -v
```

---

## 📁 Repository Structure

```
├── api/                    # FastAPI REST Application Layer
│   ├── main.py             # API routes & middleware
│   ├── schemas.py          # Pydantic request & response models
│   └── services.py         # Recommender engine & caching layer
│
├── website/                # Streamlit Frontend Client
│   ├── app.py              # Interactive UI & Folium map integration
│   └── recommender.py      # Core ranking algorithms
│
├── src/                    # Data Processing & ML Scripts
│   ├── data_loader.py      # Multi-source web scraper ETL
│   ├── pca_analysis.py     # PCA statistical modeling
│   └── cost_calculator.py  # Composite index calculator
│
├── tests/                  # Automated Test Suite
│   └── test_api.py         # Pytest API integration tests
│
├── outputs/                # Calculated Reports & Visualizations
├── Dockerfile.api          # Backend Docker container configuration
├── Dockerfile.web          # Frontend Docker container configuration
├── docker-compose.yml      # Multi-container orchestration setup
└── .github/workflows/ci.yml # GitHub Actions CI/CD Pipeline
```
