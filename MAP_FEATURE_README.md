# 🗺️ Interactive Map Feature

## What's New?

The City Cost Recommender now includes an **interactive map** that visualizes the top 5 recommended cities on a map of India!

## Features

### Visual City Location
- See exactly where your recommended cities are located
- Interactive markers with detailed information
- Color-coded by rank (darker green = better value)

### Interactive Elements
- **Click markers** to see detailed city information
- **Hover** to see city name and rank
- **Zoom and pan** to explore the map
- **Circle markers** sized by rank (larger = higher rank)

### Information Displayed
Each marker shows:
- City rank (#1, #2, etc.)
- Custom cost index
- Baseline cost index
- Brief explanation of why it's recommended

## How It Works

### Map Display
1. Set your component weights using sliders
2. Click "Calculate My Index"
3. View your custom weights table
4. **NEW:** See top 5 cities on an interactive map
5. Scroll down for detailed city information

### Color Coding
- **Dark Green** (#1) - Best value
- **Green** (#2) - Excellent value
- **Light Green** (#3) - Very good value
- **Orange** (#4) - Good value
- **Light Orange** (#5) - Decent value

### Map Controls
- **Zoom**: Use mouse wheel or +/- buttons
- **Pan**: Click and drag to move around
- **Markers**: Click for popup with details
- **Tooltip**: Hover for quick city name

## Technical Details

### Libraries Used
- **Folium**: Python library for interactive maps
- **Streamlit-Folium**: Integration with Streamlit
- **OpenStreetMap**: Base map tiles

### City Coordinates
All 50 cities have accurate latitude/longitude coordinates stored in `website/city_coordinates.py`

### Map Center
- Centered on India: 20.5937°N, 78.9629°E
- Initial zoom level: 5 (shows entire country)

## Installation

The required packages are already installed:
```bash
pip install folium streamlit-folium
```

Or use the updated requirements file:
```bash
pip install -r requirements.txt
```

## Usage Example

### Scenario: Looking for affordable cities with good housing

1. **Set Sliders:**
   - Housing: 10 (very important)
   - Others: 5 (normal)

2. **Click Calculate**

3. **View Map:**
   - See top 5 cities plotted on India map
   - Notice they're spread across different regions
   - Click markers to see why each city ranks high

4. **Explore:**
   - Zoom into specific regions
   - Compare geographic distribution
   - See if cities are near your preferred location

## Benefits

### Geographic Context
- Understand where recommended cities are located
- Consider proximity to family/friends
- Evaluate regional preferences

### Visual Decision Making
- Easier to compare city locations
- See clustering of affordable cities
- Identify regional cost patterns

### Interactive Exploration
- Engage with data visually
- Better understanding of recommendations
- More intuitive than just lists

## Map Features

### Markers
- **Icon**: Info sign (ℹ️)
- **Color**: Rank-based (green to orange)
- **Size**: Larger for higher ranks
- **Popup**: Detailed information
- **Tooltip**: Quick preview

### Circle Markers
- **Radius**: 15px for #1, decreasing by 2px per rank
- **Opacity**: 30% fill for subtle emphasis
- **Color**: Matches marker color

## Future Enhancements

Potential additions:
- Show all 50 cities with different colors
- Filter map by cost range
- Add heatmap overlay for cost intensity
- Show travel routes between cities
- Add satellite/terrain view options
- Display nearby cities for comparison

## Troubleshooting

### Map Not Showing
- Ensure `folium` and `streamlit-folium` are installed
- Check that `city_coordinates.py` exists
- Verify internet connection (for map tiles)

### Markers Missing
- Check if city names match exactly
- Verify coordinates in `city_coordinates.py`
- Ensure top 5 cities have valid coordinates

### Slow Loading
- Map loads after calculations complete
- Large zoom levels may take time
- Refresh page if stuck

## Files Modified

1. **website/app.py** - Added map display logic
2. **website/city_coordinates.py** - NEW: City coordinate data
3. **requirements.txt** - Added folium packages

## Code Example

```python
# Create map centered on India
m = folium.Map(
    location=[20.5937, 78.9629],
    zoom_start=5,
    tiles='OpenStreetMap'
)

# Add markers for top 5 cities
for i, rec in enumerate(recommendations[:5], 1):
    city_name = rec['city']
    coords = get_coordinates(city_name)
    
    folium.Marker(
        location=[coords['lat'], coords['lon']],
        popup=city_info,
        tooltip=f"#{i} {city_name}",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Display in Streamlit
st_folium(m, width=1200, height=500)
```

## Conclusion

The interactive map adds a powerful visual dimension to the City Cost Recommender, making it easier to understand where recommended cities are located and how they relate geographically. This helps users make more informed decisions by considering both cost and location factors.

---

**Access the updated website:**
```bash
streamlit run website/app.py
```

Or visit: http://localhost:8501

🗺️ Happy exploring!
