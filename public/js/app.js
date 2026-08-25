/**
 * India Smart City Cost Recommender - Client Application Engine
 * Blazing-fast client-side recommendation engine & Leaflet mapping
 */

(function() {
  'use strict';

  // Constants & Baseline Weights
  const CATEGORIES = [
    'Housing', 'Grocery', 'Transport', 'Healthcare', 
    'Education', 'Electricity', 'Restaurant', 'Movies'
  ];

  const BASE_WEIGHTS = {
    Housing: 0.3030,
    Grocery: 0.3636,
    Transport: 0.1091,
    Healthcare: 0.0642,
    Education: 0.0606,
    Electricity: 0.0303,
    Restaurant: 0.0485,
    Movies: 0.0207
  };

  const CATEGORY_TO_FIELD = {
    Housing: 'housing_index',
    Grocery: 'grocery_index',
    Transport: 'transport_index',
    Healthcare: 'healthcare_index',
    Education: 'education_index',
    Electricity: 'electricity_index',
    Restaurant: 'restaurant_index',
    Movies: 'movie_index'
  };

  // State
  let citiesData = [];
  let leafletMap = null;
  let mapMarkersLayer = null;
  let currentRankedCities = [];

  // DOM Elements
  const weightsForm = document.getElementById('weights-form');
  const btnCalculate = document.getElementById('btn-calculate');
  const btnResetWeights = document.getElementById('btn-reset-weights');
  const selectTopN = document.getElementById('select-top-n');
  const weightsTableBody = document.getElementById('weights-table-body');
  const cityCardsContainer = document.getElementById('city-cards-container');
  const resultsCountHeading = document.getElementById('results-count-heading');
  const allCitiesTbody = document.getElementById('all-cities-tbody');
  const filterCityInput = document.getElementById('filter-city-input');

  // Initialization
  async function init() {
    setupSliderListeners();
    initLeafletMap();
    await loadCitiesData();
    calculateAndRender();
    if (window.lucide) {
      window.lucide.createIcons();
    }
  }

  // Load Cities Data
  async function loadCitiesData() {
    if (window.CITIES_DATA && Array.isArray(window.CITIES_DATA) && window.CITIES_DATA.length > 0) {
      citiesData = window.CITIES_DATA;
      return;
    }

    try {
      const response = await fetch('data/cities.json');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      citiesData = await response.json();
    } catch (err) {
      console.warn('Loading fallback embedded city data:', err);
      try {
        const fallbackRes = await fetch('./data/cities.json');
        citiesData = await fallbackRes.json();
      } catch (e) {
        console.error('Failed to load cities data:', e);
      }
    }
  }

  // Slider Listeners & Dynamic Badges
  function setupSliderListeners() {
    CATEGORIES.forEach(cat => {
      const slider = document.getElementById(`slider-${cat}`);
      const valBadge = document.getElementById(`val-${cat}`);
      if (slider && valBadge) {
        slider.addEventListener('input', (e) => {
          valBadge.textContent = e.target.value;
          // Trigger instant calculation on change
          calculateAndRender();
        });
      }
    });

    if (selectTopN) {
      selectTopN.addEventListener('change', () => calculateAndRender());
    }

    if (btnCalculate) {
      btnCalculate.addEventListener('click', () => {
        calculateAndRender();
        const resultsSection = document.getElementById('results-section');
        if (resultsSection) {
          resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    }

    if (btnResetWeights) {
      btnResetWeights.addEventListener('click', () => {
        CATEGORIES.forEach(cat => {
          const slider = document.getElementById(`slider-${cat}`);
          const valBadge = document.getElementById(`val-${cat}`);
          if (slider && valBadge) {
            slider.value = 5;
            valBadge.textContent = '5';
          }
        });
        calculateAndRender();
      });
    }

    if (filterCityInput) {
      filterCityInput.addEventListener('input', (e) => {
        filterAllCitiesTable(e.target.value.trim().toLowerCase());
      });
    }
  }

  // Leaflet Map Initialization
  function initLeafletMap() {
    const mapContainer = document.getElementById('city-map');
    if (!mapContainer) return;

    // Center on geographic center of India
    leafletMap = L.map('city-map', {
      center: [21.5, 78.9629],
      zoom: 5,
      scrollWheelZoom: false
    });

    // High quality OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(leafletMap);

    mapMarkersLayer = L.layerGroup().addTo(leafletMap);
  }

  // Get current slider weights
  function getSliderWeights() {
    const sliders = {};
    CATEGORIES.forEach(cat => {
      const slider = document.getElementById(`slider-${cat}`);
      sliders[cat] = slider ? parseInt(slider.value, 10) : 5;
    });
    return sliders;
  }

  // Calculate Weights and City Rankings
  function calculateRankings(sliders) {
    const newWeights = {};
    const multipliers = {};

    CATEGORIES.forEach(cat => {
      const val = sliders[cat] || 5;
      let mult;
      if (val <= 5) {
        mult = 0.1 + (val - 1) * (0.9 / 4.0);
      } else {
        mult = 1.0 + (val - 5) * (1.0 / 5.0);
      }
      multipliers[cat] = mult;
      newWeights[cat] = BASE_WEIGHTS[cat] * mult;
    });

    // Normalize weights to 1.0
    const totalWeight = Object.values(newWeights).reduce((a, b) => a + b, 0);
    const normWeights = {};
    CATEGORIES.forEach(cat => {
      normWeights[cat] = newWeights[cat] / totalWeight;
    });

    // Compute custom index for each city
    const calculatedCities = citiesData.map(city => {
      let customIndex = 0.0;
      const contributions = [];

      CATEGORIES.forEach(cat => {
        const field = CATEGORY_TO_FIELD[cat];
        const val = city[field] || 100.0;
        const impact = val * normWeights[cat];
        customIndex += impact;
        contributions.push({
          category: cat,
          indexVal: val,
          weight: normWeights[cat],
          impact: impact
        });
      });

      // Sort by cost driver impact
      contributions.sort((a, b) => b.impact - a.impact);

      return {
        ...city,
        custom_index: customIndex,
        top_drivers: contributions.slice(0, 2),
        all_contributions: contributions
      };
    });

    // Sort ascending (most affordable first)
    calculatedCities.sort((a, b) => a.custom_index - b.custom_index);

    // Assign ranks
    calculatedCities.forEach((city, index) => {
      city.rank = index + 1;
    });

    return {
      rankedCities: calculatedCities,
      normWeights: normWeights,
      multipliers: multipliers
    };
  }

  // Main Render Routine
  function calculateAndRender() {
    if (!citiesData || citiesData.length === 0) return;

    const sliders = getSliderWeights();
    const topN = parseInt(selectTopN ? selectTopN.value : '10', 10);
    const { rankedCities, normWeights, multipliers } = calculateRankings(sliders);
    currentRankedCities = rankedCities;

    // 1. Render Weights Breakdown Table
    renderWeightsTable(normWeights, multipliers);

    // 2. Render Top N City Cards
    renderCityCards(rankedCities.slice(0, topN));

    // 3. Update Leaflet Map with Top N Cities
    updateMapMarkers(rankedCities.slice(0, Math.min(topN, 10)));

    // 4. Render Complete 50 Cities Table
    renderAllCitiesTable(rankedCities);

    // Refresh icons
    if (window.lucide) {
      window.lucide.createIcons();
    }
  }

  // Render Weights Table
  function renderWeightsTable(normWeights, multipliers) {
    if (!weightsTableBody) return;

    const rows = CATEGORIES.map(cat => {
      const basePct = (BASE_WEIGHTS[cat] * 100).toFixed(1) + '%';
      const mult = multipliers[cat].toFixed(2) + 'x';
      const effPct = (normWeights[cat] * 100).toFixed(1) + '%';

      return `
        <tr>
          <td><strong>${cat}</strong></td>
          <td>${basePct}</td>
          <td><span class="badge-tag">${mult}</span></td>
          <td><strong>${effPct}</strong></td>
        </tr>
      `;
    }).join('');

    weightsTableBody.innerHTML = rows;
  }

  // Render Recommendation Cards
  function renderCityCards(topCities) {
    if (!cityCardsContainer) return;

    if (resultsCountHeading) {
      resultsCountHeading.textContent = `Top ${topCities.length} Recommended Cities`;
    }

    const cardsHtml = topCities.map(city => {
      const d1 = city.top_drivers[0];
      const d2 = city.top_drivers[1];

      const rawPills = CATEGORIES.map(cat => {
        const field = CATEGORY_TO_FIELD[cat];
        const val = (city[field] || 100).toFixed(1);
        return `
          <div class="mini-index-pill">
            <span class="mini-index-label">${cat}</span>
            <span class="mini-index-val">${val}</span>
          </div>
        `;
      }).join('');

      return `
        <article class="city-card">
          <div class="city-card-header">
            <span class="rank-badge">Rank ${city.rank}</span>
            <h3 class="city-card-name">${city.city}</h3>
          </div>

          <div class="city-card-body">
            
            <div class="city-explanation-box">
              <div class="city-explanation-text">
                <strong>Custom Cost Index: ${city.custom_index.toFixed(1)}</strong>
              </div>
              <ul class="city-drivers-list">
                <li><strong>${d1.category}:</strong> Index ${d1.indexVal.toFixed(0)} (Effective Weight: ${(d1.weight * 100).toFixed(1)}%)</li>
                <li><strong>${d2.category}:</strong> Index ${d2.indexVal.toFixed(0)} (Effective Weight: ${(d2.weight * 100).toFixed(1)}%)</li>
              </ul>
            </div>

            <div class="metric-container">
              <div class="metric-label">Custom Index</div>
              <div class="metric-value">${city.custom_index.toFixed(1)}</div>
              <div class="metric-delta">Your Personal Weights</div>
            </div>

            <div class="metric-container">
              <div class="metric-label">Baseline Index</div>
              <div class="metric-value">${city.cost_of_living_index.toFixed(1)}</div>
              <div class="metric-delta">Default National Weights</div>
            </div>

          </div>

          <details class="card-details-expander">
            <summary class="card-details-summary">
              <span>View raw index breakdown for ${city.city} (Delhi = 100)</span>
              <i data-lucide="chevron-down" class="icon-micro"></i>
            </summary>
            <div class="card-details-content">
              <div class="indices-mini-grid">
                ${rawPills}
              </div>
            </div>
          </details>

        </article>
      `;
    }).join('');

    cityCardsContainer.innerHTML = cardsHtml;
  }

  // Update Leaflet Map Markers
  function updateMapMarkers(topCities) {
    if (!leafletMap || !mapMarkersLayer) return;

    mapMarkersLayer.clearLayers();
    const latLngs = [];

    topCities.forEach(city => {
      if (!city.lat || !city.lon) return;

      const latLng = [city.lat, city.lon];
      latLngs.push(latLng);

      const markerClass = city.rank <= 5 ? `marker-rank-${city.rank}` : 'marker-rank-other';
      const customIcon = L.divIcon({
        className: 'custom-map-pin',
        html: `<div class="custom-rank-marker ${markerClass}">#${city.rank}</div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
      });

      const popupContent = `
        <div class="map-popup-card">
          <h4>#${city.rank} ${city.city}</h4>
          <hr style="margin: 6px 0; border: none; border-top: 1px solid #E5DBCD;">
          <p><strong>Custom Index:</strong> ${city.custom_index.toFixed(1)}</p>
          <p><strong>Baseline Index:</strong> ${city.cost_of_living_index.toFixed(1)}</p>
        </div>
      `;

      const marker = L.marker(latLng, { icon: customIcon })
        .bindPopup(popupContent, { maxWidth: 220 })
        .bindTooltip(`#${city.rank} ${city.city}`, { direction: 'top', offset: [0, -12] });

      mapMarkersLayer.addLayer(marker);
    });

    if (latLngs.length > 0) {
      const bounds = L.latLngBounds(latLngs);
      leafletMap.fitBounds(bounds, { padding: [50, 50], maxZoom: 7 });
    }
  }

  // Render All 50 Cities Table
  function renderAllCitiesTable(rankedCities) {
    if (!allCitiesTbody) return;

    const rowsHtml = rankedCities.map(city => {
      return `
        <tr data-city-name="${city.city.toLowerCase()}">
          <td><strong>#${city.rank}</strong></td>
          <td><strong>${city.city}</strong></td>
          <td><span class="badge-tag">${city.custom_index.toFixed(1)}</span></td>
          <td>${city.cost_of_living_index.toFixed(1)}</td>
          <td>${city.housing_index.toFixed(1)}</td>
          <td>${city.grocery_index.toFixed(1)}</td>
          <td>${city.transport_index.toFixed(1)}</td>
        </tr>
      `;
    }).join('');

    allCitiesTbody.innerHTML = rowsHtml;
  }

  // Filter All Cities Table
  function filterAllCitiesTable(searchTerm) {
    if (!allCitiesTbody) return;
    const rows = allCitiesTbody.querySelectorAll('tr');
    rows.forEach(row => {
      const cityName = row.getAttribute('data-city-name') || '';
      if (cityName.includes(searchTerm)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  }

  // Boot Application
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
