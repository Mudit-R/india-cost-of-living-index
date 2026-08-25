/**
 * India Smart City Cost Intelligence Platform - Client Application Engine
 * Pure client-side calculations, Leaflet mapping, Salary PPP, and City Comparator
 * Strictly zero emojis.
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

  // Lifestyle Presets (1 to 10 scale)
  const PRESETS = {
    tech: {
      Housing: 9, Transport: 8, Restaurant: 8, Movies: 7,
      Electricity: 6, Grocery: 4, Healthcare: 3, Education: 2
    },
    family: {
      Education: 10, Healthcare: 9, Housing: 8, Grocery: 8,
      Electricity: 6, Transport: 5, Restaurant: 3, Movies: 3
    },
    frugal: {
      Housing: 10, Grocery: 8, Transport: 8, Electricity: 8,
      Healthcare: 6, Education: 4, Restaurant: 2, Movies: 2
    },
    student: {
      Housing: 10, Restaurant: 8, Movies: 7, Grocery: 6,
      Transport: 6, Education: 5, Electricity: 4, Healthcare: 3
    },
    balanced: {
      Housing: 5, Grocery: 5, Transport: 5, Healthcare: 5,
      Education: 5, Electricity: 5, Restaurant: 5, Movies: 5
    }
  };

  // State
  let citiesData = [];
  let leafletMap = null;
  let mapMarkersLayer = null;
  let currentRankedCities = [];

  // DOM Elements - Recommender
  const weightsForm = document.getElementById('weights-form');
  const btnCalculate = document.getElementById('btn-calculate');
  const btnResetWeights = document.getElementById('btn-reset-weights');
  const selectTopN = document.getElementById('select-top-n');
  const weightsTableBody = document.getElementById('weights-table-body');
  const cityCardsContainer = document.getElementById('city-cards-container');
  const resultsCountHeading = document.getElementById('results-count-heading');
  const allCitiesTbody = document.getElementById('all-cities-tbody');
  const filterCityInput = document.getElementById('filter-city-input');

  // DOM Elements - Salary Calculator
  const salaryCurrCity = document.getElementById('salary-curr-city');
  const salaryTargetCity = document.getElementById('salary-target-city');
  const salaryAmount = document.getElementById('salary-amount');
  const btnCalculateSalary = document.getElementById('btn-calculate-salary');
  const salaryDisplayCurr = document.getElementById('salary-display-curr');
  const salaryDisplayCurrCity = document.getElementById('salary-display-curr-city');
  const salaryDisplayEquiv = document.getElementById('salary-display-equiv');
  const salaryDisplayTargetCity = document.getElementById('salary-display-target-city');
  const salaryDisplayMonthly = document.getElementById('salary-display-monthly');
  const salaryDisplayDiffPct = document.getElementById('salary-display-diff-pct');
  const salaryCategoryTbody = document.getElementById('salary-category-tbody');

  // DOM Elements - City Comparator
  const compareCityA = document.getElementById('compare-city-a');
  const compareCityB = document.getElementById('compare-city-b');
  const compareNameA = document.getElementById('compare-name-a');
  const compareNameB = document.getElementById('compare-name-b');
  const compareIndexA = document.getElementById('compare-index-a');
  const compareIndexB = document.getElementById('compare-index-b');
  const compareDiffVal = document.getElementById('compare-diff-val');
  const compareDiffDesc = document.getElementById('compare-diff-desc');
  const compareThA = document.getElementById('compare-th-a');
  const compareThB = document.getElementById('compare-th-b');
  const compareTbody = document.getElementById('compare-tbody');

  // Initialization
  async function init() {
    setupTabNavigation();
    setupSliderListeners();
    setupPresetListeners();
    setupSalaryCalculatorListeners();
    setupComparatorListeners();
    initLeafletMap();
    await loadCitiesData();
    populateCityDropdowns();
    calculateAndRenderRecommender();
    calculateAndRenderSalary();
    calculateAndRenderComparator();
    if (window.lucide) {
      window.lucide.createIcons();
    }
  }

  // Tab Navigation
  function setupTabNavigation() {
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetTabId = tab.getAttribute('data-tab');
        
        // Update active tab button
        navTabs.forEach(t => {
          t.classList.remove('active');
          t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('active');
        tab.setAttribute('aria-selected', 'true');

        // Update active tab panel
        document.querySelectorAll('.tab-panel').forEach(panel => {
          panel.classList.remove('active');
        });
        const targetPanel = document.getElementById(targetTabId);
        if (targetPanel) {
          targetPanel.classList.add('active');
        }

        // If switching to recommender, invalidate map size to render correctly
        if (targetTabId === 'tab-recommender' && leafletMap) {
          setTimeout(() => leafletMap.invalidateSize(), 100);
        }

        if (window.lucide) {
          window.lucide.createIcons();
        }
      });
    });
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

  // Populate Dropdown Selectors
  function populateCityDropdowns() {
    if (!citiesData || citiesData.length === 0) return;

    const sortedCities = [...citiesData].sort((a, b) => a.city.localeCompare(b.city));

    const buildOptions = (selectedName) => {
      return sortedCities.map(c => {
        const isSel = c.city.toLowerCase() === selectedName.toLowerCase() ? 'selected' : '';
        return `<option value="${c.city}" ${isSel}>${c.city}</option>`;
      }).join('');
    };

    if (salaryCurrCity) salaryCurrCity.innerHTML = buildOptions('Mumbai');
    if (salaryTargetCity) salaryTargetCity.innerHTML = buildOptions('Pune');
    if (compareCityA) compareCityA.innerHTML = buildOptions('Mumbai');
    if (compareCityB) compareCityB.innerHTML = buildOptions('Bengaluru');
  }

  // =========================================================================
  // TAB 1: RECOMMENDER LOGIC
  // =========================================================================

  function setupSliderListeners() {
    CATEGORIES.forEach(cat => {
      const slider = document.getElementById(`slider-${cat}`);
      const valBadge = document.getElementById(`val-${cat}`);
      if (slider && valBadge) {
        slider.addEventListener('input', (e) => {
          valBadge.textContent = e.target.value;
          // Clear active state from presets when manually adjusted
          document.querySelectorAll('.preset-chip').forEach(c => c.classList.remove('active'));
          calculateAndRenderRecommender();
        });
      }
    });

    if (selectTopN) {
      selectTopN.addEventListener('change', () => calculateAndRenderRecommender());
    }

    if (btnCalculate) {
      btnCalculate.addEventListener('click', () => {
        calculateAndRenderRecommender();
        const resultsSection = document.getElementById('results-section');
        if (resultsSection) {
          resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    }

    if (btnResetWeights) {
      btnResetWeights.addEventListener('click', () => {
        applyPreset('balanced');
      });
    }

    if (filterCityInput) {
      filterCityInput.addEventListener('input', (e) => {
        filterAllCitiesTable(e.target.value.trim().toLowerCase());
      });
    }
  }

  function setupPresetListeners() {
    const chips = document.querySelectorAll('.preset-chip');
    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        chips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        const presetKey = chip.getAttribute('data-preset');
        applyPreset(presetKey);
      });
    });
  }

  function applyPreset(presetKey) {
    const preset = PRESETS[presetKey];
    if (!preset) return;

    CATEGORIES.forEach(cat => {
      const slider = document.getElementById(`slider-${cat}`);
      const valBadge = document.getElementById(`val-${cat}`);
      if (slider && valBadge) {
        const val = preset[cat] || 5;
        slider.value = val;
        valBadge.textContent = val;
      }
    });

    calculateAndRenderRecommender();
  }

  function initLeafletMap() {
    const mapContainer = document.getElementById('city-map');
    if (!mapContainer) return;

    leafletMap = L.map('city-map', {
      center: [21.5, 78.9629],
      zoom: 5,
      scrollWheelZoom: false
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(leafletMap);

    mapMarkersLayer = L.layerGroup().addTo(leafletMap);
  }

  function getSliderWeights() {
    const sliders = {};
    CATEGORIES.forEach(cat => {
      const slider = document.getElementById(`slider-${cat}`);
      sliders[cat] = slider ? parseInt(slider.value, 10) : 5;
    });
    return sliders;
  }

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

    const totalWeight = Object.values(newWeights).reduce((a, b) => a + b, 0);
    const normWeights = {};
    CATEGORIES.forEach(cat => {
      normWeights[cat] = newWeights[cat] / totalWeight;
    });

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

      contributions.sort((a, b) => b.impact - a.impact);

      return {
        ...city,
        custom_index: customIndex,
        top_drivers: contributions.slice(0, 2),
        all_contributions: contributions
      };
    });

    calculatedCities.sort((a, b) => a.custom_index - b.custom_index);

    calculatedCities.forEach((city, index) => {
      city.rank = index + 1;
    });

    return {
      rankedCities: calculatedCities,
      normWeights: normWeights,
      multipliers: multipliers
    };
  }

  function calculateAndRenderRecommender() {
    if (!citiesData || citiesData.length === 0) return;

    const sliders = getSliderWeights();
    const topN = parseInt(selectTopN ? selectTopN.value : '10', 10);
    const { rankedCities, normWeights, multipliers } = calculateRankings(sliders);
    currentRankedCities = rankedCities;

    renderWeightsTable(normWeights, multipliers);
    renderCityCards(rankedCities.slice(0, topN));
    updateMapMarkers(rankedCities.slice(0, Math.min(topN, 10)));
    renderAllCitiesTable(rankedCities);

    if (window.lucide) {
      window.lucide.createIcons();
    }
  }

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
        iconSize: [30, 30],
        iconAnchor: [15, 15]
      });

      const popupContent = `
        <div class="map-popup-card">
          <h4>#${city.rank} ${city.city}</h4>
          <hr style="margin: 5px 0; border: none; border-top: 1px solid #E5DBCD;">
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
      leafletMap.fitBounds(bounds, { padding: [40, 40], maxZoom: 7 });
    }
  }

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

  // =========================================================================
  // TAB 2: SALARY PARITY LOGIC
  // =========================================================================

  function setupSalaryCalculatorListeners() {
    if (btnCalculateSalary) {
      btnCalculateSalary.addEventListener('click', calculateAndRenderSalary);
    }
    if (salaryCurrCity) salaryCurrCity.addEventListener('change', calculateAndRenderSalary);
    if (salaryTargetCity) salaryTargetCity.addEventListener('change', calculateAndRenderSalary);
    if (salaryAmount) salaryAmount.addEventListener('input', calculateAndRenderSalary);
  }

  function calculateAndRenderSalary() {
    if (!citiesData || citiesData.length === 0) return;

    const currName = salaryCurrCity ? salaryCurrCity.value : 'Mumbai';
    const tgtName = salaryTargetCity ? salaryTargetCity.value : 'Pune';
    const currentSalaryLpa = parseFloat(salaryAmount ? salaryAmount.value : '15') || 15.0;

    const currCity = citiesData.find(c => c.city.toLowerCase() === currName.toLowerCase());
    const tgtCity = citiesData.find(c => c.city.toLowerCase() === tgtName.toLowerCase());

    if (!currCity || !tgtCity) return;

    const curIndex = currCity.cost_of_living_index;
    const tgtIndex = tgtCity.cost_of_living_index;

    const ratio = tgtIndex / curIndex;
    const equivSalaryLpa = (currentSalaryLpa * ratio);
    const annualDiffLpa = (currentSalaryLpa - equivSalaryLpa);
    const monthlySavingsRupees = Math.round((annualDiffLpa * 100000.0) / 12.0);
    const pctChange = (((tgtIndex - curIndex) / curIndex) * 100.0);

    if (salaryDisplayCurr) salaryDisplayCurr.textContent = `${currentSalaryLpa.toFixed(1)} LPA`;
    if (salaryDisplayCurrCity) salaryDisplayCurrCity.textContent = `in ${currCity.city}`;
    if (salaryDisplayEquiv) salaryDisplayEquiv.textContent = `${equivSalaryLpa.toFixed(1)} LPA`;
    if (salaryDisplayTargetCity) salaryDisplayTargetCity.textContent = `in ${tgtCity.city} for identical standard of living`;

    if (salaryDisplayMonthly) {
      const sign = monthlySavingsRupees >= 0 ? '+' : '-';
      const formattedRs = Math.abs(monthlySavingsRupees).toLocaleString('en-IN');
      salaryDisplayMonthly.textContent = `${sign}Rs ${formattedRs} / mo`;
    }

    if (salaryDisplayDiffPct) {
      const direction = pctChange < 0 ? 'lower' : 'higher';
      salaryDisplayDiffPct.textContent = `${Math.abs(pctChange).toFixed(1)}% ${direction} overall living cost`;
    }

    // Category breakdown
    if (salaryCategoryTbody) {
      const rows = CATEGORIES.map(cat => {
        const field = CATEGORY_TO_FIELD[cat];
        const valA = currCity[field] || 100.0;
        const valB = tgtCity[field] || 100.0;
        const diff = (((valB - valA) / valA) * 100.0);

        let badgeClass = 'variance-equal';
        let badgeText = '0.0%';
        if (diff < -1) {
          badgeClass = 'variance-cheaper';
          badgeText = `${diff.toFixed(1)}% cheaper`;
        } else if (diff > 1) {
          badgeClass = 'variance-more-expensive';
          badgeText = `+${diff.toFixed(1)}% higher`;
        } else {
          badgeText = 'Parity';
        }

        return `
          <tr>
            <td><strong>${cat}</strong></td>
            <td>${valA.toFixed(1)}</td>
            <td>${valB.toFixed(1)}</td>
            <td><span class="variance-tag ${badgeClass}">${badgeText}</span></td>
          </tr>
        `;
      }).join('');

      salaryCategoryTbody.innerHTML = rows;
    }

    if (window.lucide) {
      window.lucide.createIcons();
    }
  }

  // =========================================================================
  // TAB 3: CITY HEAD-TO-HEAD COMPARATOR LOGIC
  // =========================================================================

  function setupComparatorListeners() {
    if (compareCityA) compareCityA.addEventListener('change', calculateAndRenderComparator);
    if (compareCityB) compareCityB.addEventListener('change', calculateAndRenderComparator);
  }

  function calculateAndRenderComparator() {
    if (!citiesData || citiesData.length === 0) return;

    const nameA = compareCityA ? compareCityA.value : 'Mumbai';
    const nameB = compareCityB ? compareCityB.value : 'Bengaluru';

    const cityA = citiesData.find(c => c.city.toLowerCase() === nameA.toLowerCase());
    const cityB = citiesData.find(c => c.city.toLowerCase() === nameB.toLowerCase());

    if (!cityA || !cityB) return;

    const idxA = cityA.cost_of_living_index;
    const idxB = cityB.cost_of_living_index;
    const pctDiff = (((idxB - idxA) / idxA) * 100.0);

    if (compareNameA) compareNameA.textContent = cityA.city;
    if (compareNameB) compareNameB.textContent = cityB.city;
    if (compareIndexA) compareIndexA.textContent = idxA.toFixed(1);
    if (compareIndexB) compareIndexB.textContent = idxB.toFixed(1);

    if (compareDiffVal) {
      const sign = pctDiff > 0 ? '+' : '';
      compareDiffVal.textContent = `${sign}${pctDiff.toFixed(1)}%`;
      compareDiffVal.className = 'diff-percent ' + (pctDiff < 0 ? 'diff-negative' : (pctDiff > 0 ? 'diff-positive' : 'diff-neutral'));
    }

    if (compareDiffDesc) {
      if (pctDiff < 0) {
        compareDiffDesc.textContent = `${cityB.city} is ${Math.abs(pctDiff).toFixed(1)}% more affordable overall than ${cityA.city}.`;
      } else if (pctDiff > 0) {
        compareDiffDesc.textContent = `${cityB.city} is ${pctDiff.toFixed(1)}% more expensive overall than ${cityA.city}.`;
      } else {
        compareDiffDesc.textContent = `${cityA.city} and ${cityB.city} have identical cost of living indices.`;
      }
    }

    if (compareThA) compareThA.textContent = `${cityA.city} Index`;
    if (compareThB) compareThB.textContent = `${cityB.city} Index`;

    if (compareTbody) {
      const rows = CATEGORIES.map(cat => {
        const field = CATEGORY_TO_FIELD[cat];
        const valA = cityA[field] || 100.0;
        const valB = cityB[field] || 100.0;
        const catDiff = (((valB - valA) / valA) * 100.0);

        let badgeClass = 'variance-equal';
        let badgeText = 'Parity';
        if (catDiff < -1) {
          badgeClass = 'variance-cheaper';
          badgeText = `${catDiff.toFixed(1)}% (${cityB.city} cheaper)`;
        } else if (catDiff > 1) {
          badgeClass = 'variance-more-expensive';
          badgeText = `+${catDiff.toFixed(1)}% (${cityB.city} higher)`;
        }

        return `
          <tr>
            <td><strong>${cat}</strong></td>
            <td>${valA.toFixed(1)}</td>
            <td>${valB.toFixed(1)}</td>
            <td><span class="variance-tag ${badgeClass}">${badgeText}</span></td>
          </tr>
        `;
      }).join('');

      compareTbody.innerHTML = rows;
    }

    if (window.lucide) {
      window.lucide.createIcons();
    }
  }

  // Boot Application
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
