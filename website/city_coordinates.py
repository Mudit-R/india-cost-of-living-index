"""
City coordinates for mapping Indian cities
Latitude and Longitude data for all 50 cities in the analysis
"""

CITY_COORDINATES = {
    'Mumbai': {'lat': 19.0760, 'lon': 72.8777},
    'Delhi': {'lat': 28.7041, 'lon': 77.1025},
    'Bengaluru': {'lat': 12.9716, 'lon': 77.5946},
    'Hyderabad': {'lat': 17.3850, 'lon': 78.4867},
    'Ahmedabad': {'lat': 23.0225, 'lon': 72.5714},
    'Chennai': {'lat': 13.0827, 'lon': 80.2707},
    'Kolkata': {'lat': 22.5726, 'lon': 88.3639},
    'Pune': {'lat': 18.5204, 'lon': 73.8567},
    'Jaipur': {'lat': 26.9124, 'lon': 75.7873},
    'Surat': {'lat': 21.1702, 'lon': 72.8311},
    'Lucknow': {'lat': 26.8467, 'lon': 80.9462},
    'Kanpur': {'lat': 26.4499, 'lon': 80.3319},
    'Nagpur': {'lat': 21.1458, 'lon': 79.0882},
    'Indore': {'lat': 22.7196, 'lon': 75.8577},
    'Bhopal': {'lat': 23.2599, 'lon': 77.4126},
    'Visakhapatnam': {'lat': 17.6868, 'lon': 83.2185},
    'Patna': {'lat': 25.5941, 'lon': 85.1376},
    'Vadodara': {'lat': 22.3072, 'lon': 73.1812},
    'Ludhiana': {'lat': 30.9010, 'lon': 75.8573},
    'Agra': {'lat': 27.1767, 'lon': 78.0081},
    'Nashik': {'lat': 19.9975, 'lon': 73.7898},
    'Rajkot': {'lat': 22.3039, 'lon': 70.8022},
    'Meerut': {'lat': 28.9845, 'lon': 77.7064},
    'Jabalpur': {'lat': 23.1815, 'lon': 79.9864},
    'Coimbatore': {'lat': 11.0168, 'lon': 76.9558},
    'Madurai': {'lat': 9.9252, 'lon': 78.1198},
    'Kochi': {'lat': 9.9312, 'lon': 76.2673},
    'Kozhikode': {'lat': 11.2588, 'lon': 75.7804},
    'Thiruvananthapuram': {'lat': 8.5241, 'lon': 76.9366},
    'Mysuru': {'lat': 12.2958, 'lon': 76.6394},
    'Mangaluru': {'lat': 12.9141, 'lon': 74.8560},
    'Tiruchirappalli': {'lat': 10.7905, 'lon': 78.7047},
    'Salem': {'lat': 11.6643, 'lon': 78.1460},
    'Erode': {'lat': 11.3410, 'lon': 77.7172},
    'Chandigarh': {'lat': 30.7333, 'lon': 76.7794},
    'Bhubaneswar': {'lat': 20.2961, 'lon': 85.8245},
    'Raipur': {'lat': 21.2514, 'lon': 81.6296},
    'Aurangabad': {'lat': 19.8762, 'lon': 75.3433},
    'Solapur': {'lat': 17.6599, 'lon': 75.9064},
    'Kolhapur': {'lat': 16.7050, 'lon': 74.2433},
    'Sangli': {'lat': 16.8524, 'lon': 74.5815},
    'Jamnagar': {'lat': 22.4707, 'lon': 70.0577},
    'Hubli': {'lat': 15.3647, 'lon': 75.1240},
    'Asansol': {'lat': 23.6739, 'lon': 86.9524},
    'Amaravati region': {'lat': 16.5062, 'lon': 80.6480},
    'Kannur': {'lat': 11.8745, 'lon': 75.3704},
    'Kollam': {'lat': 8.8932, 'lon': 76.6141},
    'Kottayam': {'lat': 9.5916, 'lon': 76.5222},
    'Thrissur': {'lat': 10.5276, 'lon': 76.2144},
    'Malappuram': {'lat': 11.0510, 'lon': 76.0711}
}

def get_coordinates(city_name):
    """Get coordinates for a city"""
    return CITY_COORDINATES.get(city_name, None)

def get_all_cities_with_coords():
    """Get list of all cities with their coordinates"""
    return CITY_COORDINATES
