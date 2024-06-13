import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from plyer import gps, storagepath
import csv
import os
import platform
import requests
from datetime import datetime
#import get_traffic_info  # Import your script

# Get the API key from environment variable
api_key = os.getenv('GOOGLE_MAPS_API_KEY')
api_key= "AIzaSyDbMb_tC5_lWNKpGT5S_5jhYzDCRAIDMak"


class GPSTrafficLoggerApp(App):
    def build(self):
        self.label = Label(text="Press Start to log GPS and traffic data")
        self.start_button = Button(text="Start Logging")
        self.start_button.bind(on_press=self.start_logging)
        
        self.stop_button = Button(text="Stop Logging")
        self.stop_button.bind(on_press=self.stop_logging)
        
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(self.start_button)
        layout.add_widget(self.stop_button)
        
        self.logging = False
        self.data_file = os.path.join(storagepath.get_documents_dir(), 'gps_traffic_data.csv')
        
        # Initialize CSV file
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', newline='') as csvfile:
                fieldnames = ['timestamp', 'latitude', 'longitude', 'speed', 'traffic_status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        
        return layout
    
    def start_logging(self, instance):
        if not self.logging:
            self.logging = True
            self.label.text = "Logging GPS and traffic data..."
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            gps.start(minTime=1000, minDistance=1)
            Clock.schedule_interval(self.update, 1)
    
    def stop_logging(self, instance):
        if self.logging:
            self.logging = False
            self.label.text = "Logging stopped"
            gps.stop()
            Clock.unschedule(self.update)
    
    def on_location(self, **kwargs):
        if self.logging:
            latitude = kwargs.get('lat')
            longitude = kwargs.get('lon')
            traffic_status = self.get_traffic_info(latitude, longitude)
            with open(self.data_file, 'a', newline='') as csvfile:
                fieldnames = ['timestamp', 'latitude', 'longitude', 'speed', 'traffic_status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'latitude': latitude,
                    'longitude': longitude,
                    'speed': kwargs.get('speed', 0),
                    'traffic_status': traffic_status
                })
    
    def get_traffic_info(self, latitude, longitude):
        # Optionally use the traffic data from get_traffic_info.py
        traffic_data = get_traffic_info.get_traffic_data()
        
        # Your existing traffic information code
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={latitude},{longitude}&destinations={latitude},{longitude}&departure_time=now&key={api_key}'
        response = requests.get(url)
        data = response.json()
        try:
            traffic_status = data['rows'][0]['elements'][0]['duration_in_traffic']['text']
        except KeyError:
            traffic_status = 'No data'
        return traffic_status
    
    def on_status(self, stype, status):
        self.label.text = 'GPS Status: {}'.format(status)
    
    def update(self, dt):
        pass

if __name__ == '__main__':
    GPSTrafficLoggerApp().run()