# iroute

![Alt text](./Screenshot%202024-06-07%20at%2010.28.37.png)

### README: Traffic Monitoring System

---

#### Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Output](#output)
7. [Customization](#customization)
8. [Logging](#logging)
9. [Contributing](#contributing)
10. [License](#license)

---

### Overview

This repository contains a Python-based Traffic Monitoring System that leverages the Google Maps API to monitor and log traffic conditions between a specified origin and destination. The system provides real-time traffic updates, logs dangerous driving conditions, and visualizes traffic data over time. The system is designed to run continuously, with checks performed at regular intervals.

---

### Features

- **Real-time Traffic Monitoring**: Continuously checks and logs traffic conditions between specified locations.
- **Speed Simulation**: Randomly generates driving speeds to simulate different scenarios.
- **Danger Alerts**: Logs and triggers audible alerts when hazardous conditions are detected.
- **Data Logging**: Saves traffic data to a CSV file for further analysis.
- **Visualization**: Plots traffic conditions using bar charts with color-coded traffic delays.
- **Audible Alerts**: Plays a sound alert when dangerous conditions are detected.

---

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/traffic-monitoring-system.git
   cd traffic-monitoring-system
   ```

2. **Install Dependencies**:
   Install the required Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Google Maps API Key**:
   Obtain a Google Maps API key and set it as an environment variable:
   ```bash
   export GOOGLE_MAPS_API_KEY=your_api_key
   ```

---

### Usage

To start monitoring traffic, run the script:
```bash
python traffic_monitor.py
```
The script will continuously check traffic conditions every 5 minutes and log the results.

---

### Configuration

- **API Key**: Ensure your Google Maps API key is set as an environment variable (`GOOGLE_MAPS_API_KEY`).
- **Origin and Destination**: Edit the `origin` and `destination` variables in `traffic_monitor.py` with your desired coordinates:
  ```python
  origin = "52.57043146808288,13.520488110623809"
  destination = "52.522072764462955,13.41329526829186"
  ```
- **Sound Alert**: Place an `alert.mp3` file in the project directory for sound alerts when dangerous conditions are detected.

---

### Output

1. **CSV Logging**: Traffic data is logged in `gps_traffic_data.csv`, including:
   - Coordinates of origin and destination
   - Traffic status, distance, and duration
   - Duration in traffic and simulated speed
   - Danger status

2. **Visualizations**: The script generates bar plots to visualize traffic conditions at various waypoints along the route. The bars are color-coded:
   - **Green**: Delay less than 5 minutes
   - **Yellow**: Delay between 5-15 minutes
   - **Red**: Delay greater than 15 minutes
   - **Black**: Danger (high speed in heavy traffic)

---

### Customization

- **Speed Range**: Modify the `generate_random_speed()` function in `traffic_monitor.py` to change the range of simulated speeds.
- **Check Interval**: Adjust the `time.sleep(300)` interval in the main loop to change how frequently traffic conditions are checked.

---

### Logging

The system uses Python’s `logging` module to record:
- Routine traffic checks
- Dangerous conditions, with timestamps for easy tracking.

---

### Contributing

Contributions are welcome! If you have any ideas, suggestions, or find a bug, please open an issue or submit a pull request.

---

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This README provides all the information needed to install, configure, and run the Traffic Monitoring System. Feel free to customize the script as per your requirements and contribute to improving the system.