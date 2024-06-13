import os
import requests
import json
import pandas as pd
from datetime import datetime

# Get the API keys from environment variables
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

if not google_maps_api_key:
    raise ValueError("API key not found. Please set the GOOGLE_MAPS_API_KEY environment variable.")

# Example coordinates
latitude = 52.57043146808288
longitude = 13.520488110623809
#latitude = 37.7749
#longitude = -122.4194

def get_traffic_info(api_key, latitude, longitude):
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={latitude},{longitude}&destinations={latitude},{longitude}&departure_time=now&key={api_key}'
    response = requests.get(url)
    data = response.json()
    
    # Print the API response for debugging
    print("Google Maps API response:", json.dumps(data, indent=2))
    
    try:
        traffic_status = data['rows'][0]['elements'][0]['duration_in_traffic']['text']
    except (IndexError, KeyError):
        traffic_status = 'No data'
    
    return traffic_status

# Collect data
traffic_status = get_traffic_info(google_maps_api_key, latitude, longitude)
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Create a pandas DataFrame
data = {
    'timestamp': [timestamp],
    'latitude': [latitude],
    'longitude': [longitude],
    'traffic_status': [traffic_status]
}

df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('gps_traffic_data.csv', index=False)

# Print the DataFrame
print(df)
