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

# Load API key from environment variables

load_dotenv()
VTA_API_KEY = os.getenv("VTA_API_KEY")

# Create data directory if it doesn’t exist

os.makedirs("data/raw", exist_ok=True)

# 511.org provides real time transit data for VTA
# Documentation: https://511.org/open-data/transit

VTA_API_URL = f"https://api.511.org/transit/vehiclepositions?api_key={VTA_API_KEY}&agency=SCVTA"


def fetch_vta_data():
    
    """
    Fetches live VTA vehicle position data from the 511.org API.
    Returns a Pandas DataFrame if JSON data is available, 
    or saves a binary .pb file if GTFS realtime format is returned.
    """
    
    try:
        response = requests.get(VTA_API_URL, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if "application/json" in content_type:
            
            # Parse JSON data into a flat table
            
            data = response.json()
            df = pd.json_normalize(data.get("entity", []))
            print(f"✅ Successfully fetched {len(df)} records from VTA API.")
            return df

        else:
            # Save raw GTFS realtime protobuf if JSON is unavailable
            
            raw_filename = f"data/raw/vta_raw_{timestamp}.pb"
            with open(raw_filename, "wb") as f:
                f.write(response.content)
            print(f"💾 Saved raw GTFS-realtime data as {raw_filename}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Network/API error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def save_vta_data(df):
    
    """
    Saves the fetched DataFrame to a CSV file under data/raw/.
    Automatically timestamps each saved file.
    """
    
    if df is not None and not df.empty:
        filename = f"data/raw/vta_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        print(f"📁 Data saved to {filename}")
    else:
        print("⚠️ No data to save (possibly protobuf format).")


if __name__ == "__main__":
    print("🚏 Collecting real-time VTA transit data...")
    df = fetch_vta_data()
    save_vta_data(df)
    print("✅ Data collection complete.")
