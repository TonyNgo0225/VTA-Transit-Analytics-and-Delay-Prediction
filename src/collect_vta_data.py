"""
collect_vta_data.py
-------------------
Author: Tony Ngo

Description:
    This script connects to the VTA (Valley Transportation Authority) API via 511.org
    to collect real-time transit data. It stores the data locally for use in transit
    delay prediction models.

This program:
    Connects to the 511.org API using your personal API key.
    Collects real-time VTA bus and light rail position data.
    Saves the data into the "data/raw" folder as a CSV file for later analysis.
"""

import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from google.transit import gtfs_realtime_pb2

load_dotenv()
VTA_API_KEY = os.getenv("VTA_API_KEY")

os.makedirs("data/raw", exist_ok=True)

API_URL = f"https://api.511.org/transit/vehiclepositions?api_key={VTA_API_KEY}&agency=SC"

def fetch_vta_data():
    """
    Fetches current VTA vehicle position data from 511.org API.
    Returns parsed GTFS-RT feed or None if the request fails.
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        print(f"Successfully fetched VTA data. {len(feed.entity)} vehicles found.")
        return feed

    except requests.exceptions.RequestException as e:
        print(f"Network/API error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def parse_vta_data(feed):
    """
    Extracts vehicle position information from GTFS-RT feed and converts to DataFrame.
    """
    if feed is None:
        return None

    records = []
    timestamp = datetime.now()

    for entity in feed.entity:
        if entity.HasField('vehicle'):
            vehicle = entity.vehicle
            record = {
                "timestamp": timestamp,
                "vehicle_id": vehicle.vehicle.id if vehicle.HasField('vehicle') else None,
                "trip_id": vehicle.trip.trip_id if vehicle.HasField('trip') else None,
                "route_id": vehicle.trip.route_id if vehicle.HasField('trip') else None,
                "latitude": vehicle.position.latitude if vehicle.HasField('position') else None,
                "longitude": vehicle.position.longitude if vehicle.HasField('position') else None,
                "current_status": vehicle.current_status if vehicle.HasField('current_status') else None,
                "timestamp_unix": vehicle.timestamp if vehicle.HasField('timestamp') else None
            }
            records.append(record)

    if not records:
        print("No vehicle data extracted.")
        return None

    df = pd.DataFrame(records)
    return df

def save_vta_data(df):
    """
    Saves the VTA DataFrame to a CSV file in the data/raw folder.
    """
    if df is not None and not df.empty:
        filename = f"data/raw/vta_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        print(f"VTA data saved to {filename}")
    else:
        print("No data to save (empty or invalid response).")

if __name__ == "__main__":
    print("Collecting real-time VTA transit data...")
    feed = fetch_vta_data()
    df = parse_vta_data(feed)
    save_vta_data(df)
    print("VTA data collection complete.")
