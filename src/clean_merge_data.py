"""
clean_merge_data.py
-------------------
Author: Tony Ngo

Description:
    This script reads and cleans the raw transit data collected from the 
    VTA API and the weather data collected 
    from the OpenWeatherMap API. It prepares the datasets for analysis and 
    machine learning.

This program:
    Loads VTA and weather data files from the "data/raw" folder.
    Cleans missing or inconsistent values.
    Merges the two datasets by timestamp (based on time and date).
    Saves the cleaned and combined dataset into the "data/processed" folder.

    The processed dataset will be used later for visualization and 
    model training to predict transit delays based on weather and time.
"""

import os
import pandas as pd
from datetime import datetime

# Create processed data directory if it doesn’t exist
os.makedirs("data/processed", exist_ok=True)

def load_latest_file(folder_path, keyword):
    """
    Finds and loads the most recent file in a given folder 
    containing a specific keyword (e.g., 'vta' or 'weather').
    """
    files = [f for f in os.listdir(folder_path) if keyword in f and f.endswith(('.csv', '.json'))]
    if not files:
        raise FileNotFoundError(f"No {keyword} files found in {folder_path}.")
    
    latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
    print(f"Loading latest {keyword} file: {latest_file}")
    
    file_path = os.path.join(folder_path, latest_file)
    if latest_file.endswith(".json"):
        df = pd.read_json(file_path)
    else:
        df = pd.read_csv(file_path)
    return df

def clean_vta_data(df_vta):
    """
    Cleans the VTA dataset:
    - Removes missing or duplicate entries.
    - Converts timestamps to datetime format.
    - Keeps relevant columns for merging and analysis.
    """
    print("Cleaning VTA data...")
    df_vta = df_vta.drop_duplicates()
    df_vta = df_vta.dropna(subset=["timestamp"])
    
    if "timestamp" in df_vta.columns:
        df_vta["timestamp"] = pd.to_datetime(df_vta["timestamp"], unit="s", errors="coerce")
    
    # Keep only relevant columns if available
    keep_cols = ["trip_id", "route_id", "latitude", "longitude", "timestamp"]
    df_vta = df_vta[[col for col in keep_cols if col in df_vta.columns]]
    return df_vta

def clean_weather_data(df_weather):
    """
    Cleans the weather dataset:
    - Converts timestamps to datetime format.
    - Keeps useful weather features for analysis.
    """
    print("Cleaning weather data...")
    if "dt" in df_weather.columns:
        df_weather["timestamp"] = pd.to_datetime(df_weather["dt"], unit="s", errors="coerce")
    elif "timestamp" in df_weather.columns:
        df_weather["timestamp"] = pd.to_datetime(df_weather["timestamp"], errors="coerce")

    # Keep key weather variables if they exist
    keep_cols = ["timestamp", "temp", "humidity", "pressure", "wind_speed", "weather_main"]
    df_weather = df_weather[[col for col in keep_cols if col in df_weather.columns]]
    return df_weather

def merge_datasets(df_vta, df_weather):
    """
    Merges the VTA and weather datasets based on closest timestamps.
    Rounds timestamps to the nearest 10 minutes to make merging easier.
    """
    print("Merging VTA and weather datasets...")
    df_vta["timestamp_rounded"] = df_vta["timestamp"].dt.round("10min")
    df_weather["timestamp_rounded"] = df_weather["timestamp"].dt.round("10min")

    merged = pd.merge(df_vta, df_weather, on="timestamp_rounded", how="left", suffixes=("_vta", "_weather"))
    merged = merged.dropna(subset=["timestamp_vta"])  # drop invalid merges
    merged = merged.sort_values("timestamp_vta").reset_index(drop=True)
    print(f"Merged dataset created with {len(merged)} rows.")
    return merged

def save_processed_data(df):
    """
    Saves the cleaned and merged dataset to data/processed/combined_vta_weather.csv
    """
    filename = f"data/processed/combined_vta_weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved cleaned dataset to {filename}")

if __name__ == "__main__":
    try:
        print("Loading raw VTA and weather data...")
        df_vta = load_latest_file("data/raw", "vta")
        df_weather = load_latest_file("data/raw", "weather")

        df_vta = clean_vta_data(df_vta)
        df_weather = clean_weather_data(df_weather)
        df_combined = merge_datasets(df_vta, df_weather)

        save_processed_data(df_combined)
        print("Data cleaning and merging complete.")
    except Exception as e:
        print(f"Error during data processing: {e}")

