import os
import requests
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import logging
import time
from playsound import playsound
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Get the API key from environment variables
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

if not google_maps_api_key:
    raise ValueError("API key not found. Please set the GOOGLE_MAPS_API_KEY environment variable.")

# Example coordinates for origin and destination
origin = "52.57043146808288,13.520488110623809"
destination = "52.522072764462955,13.41329526829186"

# Example speed variable (in km/h)
speed_override = 35  # Use this variable to simulate speed

def generate_random_speed():
    return random.randint(30, 50)

speed_override = generate_random_speed()
print(speed_override)


def get_route(api_key, origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] != 'OK':
        raise ValueError(f"Error getting directions: {data.get('error_message')}")
    
    route = data['routes'][0]
    legs = route['legs'][0]
    waypoints = [(step['start_location']['lat'], step['start_location']['lng']) for step in legs['steps']]
    waypoints.append((legs['end_location']['lat'], legs['end_location']['lng']))
    
    return waypoints

def get_traffic_info(api_key, waypoints, speed_override=None):
    origins = "|".join([f"{lat},{lon}" for lat, lon in waypoints[:-1]])
    destinations = "|".join([f"{lat},{lon}" for lat, lon in waypoints[1:]])
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&departure_time=now&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] != 'OK':
        raise ValueError(f"Error getting traffic info: {data.get('error_message')}")
    
    traffic_data = []
    for i, row in enumerate(data['rows']):
        for j, element in enumerate(row['elements']):
            try:
                traffic_status = element['duration_in_traffic']['text']
                distance = element['distance']['text']
                duration = element['duration']['text']
                duration_in_traffic_value = element['duration_in_traffic']['value']
            except KeyError:
                traffic_status = 'No data'
                distance = 'No data'
                duration = 'No data'
                duration_in_traffic_value = None
            
            speed_override = generate_random_speed()
            speed = speed_override if speed_override is not None else waypoints[i][2]  # Use override speed if provided
            is_danger = (duration_in_traffic_value is not None and duration_in_traffic_value > 900 and speed > 40)  # Check if speed > 40 in red traffic
            
            if is_danger:
                logging.info(f"Danger! Speed is {speed_override:.2f} km/h in heavy traffic at waypoint {i}-{j}.")
                
                playsound('alert.mp3')
            
            traffic_data.append({
                'origin_latitude': waypoints[i][0],
                'origin_longitude': waypoints[i][1],
                'destination_latitude': waypoints[j+1][0],
                'destination_longitude': waypoints[j+1][1],
                'traffic_status': traffic_status,
                'distance': distance,
                'duration': duration,
                'duration_in_traffic_value': duration_in_traffic_value,
                'speed': speed,
                'danger': is_danger
            })
    
    return traffic_data

def categorize_traffic(duration_in_traffic_value, danger):
    if danger:
        return 'black'
    if duration_in_traffic_value is None:
        return 'gray'
    elif duration_in_traffic_value < 300:  # less than 5 minutes
        return 'green'
    elif duration_in_traffic_value < 900:  # 5-15 minutes
        return 'yellow'
    else:
        return 'red'

# Function to check traffic condition and log the results
def check_traffic_condition():
    # Collect waypoints
    waypoints = get_route(google_maps_api_key, origin, destination)

    # Collect traffic data for waypoints with the speed_override variable
    traffic_data = get_traffic_info(google_maps_api_key, waypoints, speed_override)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create a pandas DataFrame
    df = pd.DataFrame(traffic_data)
    df['timestamp'] = timestamp

    # Save the DataFrame to a CSV file
    df.to_csv('gps_traffic_data.csv', mode='a', header=not os.path.exists('gps_traffic_data.csv'), index=False)

    # Print the DataFrame
    print(df)

    # Prepare data for bar plot
    df['color'] = df.apply(lambda row: categorize_traffic(row['duration_in_traffic_value'], row['danger']), axis=1)
    df['waypoint'] = range(len(df))

    # Plotting the traffic data as a bar plot
    plt.figure(figsize=(14, 8))

    bars = plt.bar(df['waypoint'], df['duration_in_traffic_value'] / 60, color=df['color'], edgecolor='black')

    # Customize plot
    plt.xlabel('Waypoints')
    plt.ylabel('Duration in Traffic (minutes)')
    plt.title('Traffic Conditions Over Journey')
    plt.xticks(ticks=df['waypoint'], labels=df['waypoint'])
    plt.grid(True)
    plt.tight_layout()

    # Add legend
    import matplotlib.patches as mpatches
    green_patch = mpatches.Patch(color='green', label='Less than 5 min')
    yellow_patch = mpatches.Patch(color='yellow', label='5-15 min')
    red_patch = mpatches.Patch(color='red', label='More than 15 min')
    black_patch = mpatches.Patch(color='black', label='Danger')
    plt.legend(handles=[green_patch, yellow_patch, red_patch, black_patch])

    # Show plot
    plt.show()

# Main loop to check traffic condition every 5 minutes
while True:
    check_traffic_condition()
    logging.info("Checked traffic condition. Waiting for next check...")
    time.sleep(300)  # Wait for 5 minutes (300 seconds)