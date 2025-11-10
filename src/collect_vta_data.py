"""
collect_vta_data.py
-------------------
Author: Tony Ngo

Description:
    This script connects to the VTA (Valley Transportation Authority) real time API 
    using data provided by 511.org. It downloads live information about bus and 
    light rail vehicle locations in Santa Clara County.

This program:
    Connects to the VTA API using your personal API key.
    Collects the latest transit data.
    Saves the data into the "data/raw" folder for later analysis.

    The data will help build models that can predict bus or train delays later on.
"""


import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from google.transit import gtfs_realtime_pb2

# Load API key from environment variables

load_dotenv()
VTA_API_KEY = os.getenv("VTA_API_KEY")

# Create data directory if it doesn’t exist

os.makedirs("data/raw", exist_ok=True)

# 511.org provides real time transit data for VTA
# Documentation: https://511.org/open-data/transit

VTA_API_URL = f"http://api.511.org/transit/vehiclepositions?api_key={VTA_API_KEY}&agency=SC"


def fetch_vta_data():
    
    """
    Fetches live VTA vehicle position data from the 511.org API.
    Parses GTFS-realtime protobuf format and returns a Pandas DataFrame.
    """
    
    try:
        response = requests.get(VTA_API_URL, timeout=10)
        response.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        
        vehicles = []
        for entity in feed.entity:
            if entity.HasField('vehicle'):
                vehicle = entity.vehicle
                vehicle_data = {
                    'timestamp': datetime.now(),
                    'vehicle_id': vehicle.vehicle.id if vehicle.HasField('vehicle') else None,
                    'latitude': vehicle.position.latitude if vehicle.HasField('position') else None,
                    'longitude': vehicle.position.longitude if vehicle.HasField('position') else None,
                    'bearing': vehicle.position.bearing if vehicle.HasField('position') and vehicle.position.HasField('bearing') else None,
                    'speed': vehicle.position.speed if vehicle.HasField('position') and vehicle.position.HasField('speed') else None,
                    'trip_id': vehicle.trip.trip_id if vehicle.HasField('trip') else None,
                    'route_id': vehicle.trip.route_id if vehicle.HasField('trip') else None,
                    'stop_id': vehicle.stop_id if vehicle.HasField('stop_id') else None,
                    'current_status': vehicle.current_status if vehicle.HasField('current_status') else None,
                }
                vehicles.append(vehicle_data)
        
        if vehicles:
            df = pd.DataFrame(vehicles)
            print(f"Successfully fetched {len(df)} vehicle records from VTA API.")
            return df
        else:
            print("No vehicle data found in feed.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Network/API error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def save_vta_data(df):
    
    """
    Saves the fetched DataFrame to a CSV file under data/raw/.
    Automatically timestamps each saved file.
    """
    
    if df is not None and not df.empty:
        filename = f"data/raw/vta_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save (possibly protobuf format).")


if __name__ == "__main__":
    print("Collecting real-time VTA transit data...")
    df = fetch_vta_data()
    save_vta_data(df)
    print("Data collection complete.")
