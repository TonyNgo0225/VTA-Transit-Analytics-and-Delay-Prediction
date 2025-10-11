import requests
import pandas as pd
import time
from datetime import datetime
import os

# Optionally, load environment variables (if you use API keys, etc.)
from dotenv import load_dotenv
load_dotenv()

# ========== Configuration ==========
# These may need to change depending on the actual API spec
RTVIP_BASE = "https://rtvip.vta.org/api/fetch"  # base for RTVIP requests :contentReference[oaicite:1]{index=1}
FETCH_TYPE = "vehicle_positions"  # example type — check API docs
RECORD_COUNT = 1000  # how many records to request
ORDER = "desc"
COUNTER = 0

OUTPUT_DIR = "data/raw"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "vta_realtime_snapshot.csv")

# Create directory if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def build_url(fetch_type=FETCH_TYPE, count=RECORD_COUNT, order=ORDER, counter=COUNTER):
    """
    Build the RTVIP API URL for fetching real-time data.
    Format based on VTA API docs: /api/fetch/{type}/{count}/{order}/{counter} :contentReference[oaicite:2]{index=2}
    """
    url = f"{RTVIP_BASE}/{fetch_type}/{count}/{order}/{counter}"
    return url


def fetch_vta_realtime():
    url = build_url()
    resp = requests.get(url)
    resp.raise_for_status()
    # The response might be JSON or XML depending on the API.
    # We'll assume JSON for now — you’ll adjust if it’s XML.
    return resp.json()


def parse_vehicle_data(json_data):
    """
    Parse JSON response into a DataFrame.
    You’ll need to adjust field names based on the API structure.
    """
    records = []
    entities = json_data.get("entity", [])
    for ent in entities:
        # some APIs wrap vehicle info under “vehicle” key, etc.
        veh = ent.get("vehicle", {})
        trip = veh.get("trip", {})
        pos = veh.get("position", {})
        rec = {
            "entity_id": ent.get("id"),
            "trip_id": trip.get("trip_id"),
            "route_id": trip.get("route_id"),
            "direction_id": trip.get("direction_id"),
            "latitude": pos.get("latitude"),
            "longitude": pos.get("longitude"),
            "timestamp": veh.get("timestamp") or ent.get("timestamp"),
        }
        # convert timestamp to datetime, if present
        if rec["timestamp"] is not None:
            try:
                rec["datetime"] = datetime.fromtimestamp(int(rec["timestamp"]))
            except Exception as e:
                rec["datetime"] = None
        records.append(rec)
    df = pd.DataFrame(records)
    return df


def save_snapshot(df, output_csv=OUTPUT_CSV):
    """
    Save the DataFrame to CSV (appending with timestamp).
    """
    # If file doesn't exist, write header; else append
    if not os.path.isfile(output_csv):
        df.to_csv(output_csv, index=False)
    else:
        df.to_csv(output_csv, mode="a", header=False, index=False)


def main(poll_interval_s=60):
    """
    Continuously fetch and append live data every poll_interval_s seconds.
    """
    while True:
        try:
            json_data = fetch_vta_realtime()
            df = parse_vehicle_data(json_data)
            print(f"[{datetime.now()}] Retrieved {len(df)} records.")
            save_snapshot(df)
        except Exception as e:
            print("Error fetching or saving data:", e)
        time.sleep(poll_interval_s)


if __name__ == "__main__":
    # For one-time run:
    json_data = fetch_vta_realtime()
    df = parse_vehicle_data(json_data)
    print(df.head())
    # Optionally save a snapshot
    save_snapshot(df)
    # Or to run continuously:
    # main(poll_interval_s=60)

