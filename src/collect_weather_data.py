"""
collect_weather_data.py
-----------------------
Author: Tony Ngo

Description:
    This script connects to the OpenWeatherMap API to collect current weather data 
    for San Jose, California. It stores the data locally for use in transit delay 
    prediction models.

This program:
    Connects to the OpenWeatherMap API using your personal API key.
    Collects the latest weather data for San Jose, CA.
    Saves the data into the "data/raw" folder as a CSV file for later analysis.

    The collected weather data will later be combined with VTA transit data 
    to analyze how weather conditions affect transit delays.
"""

import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Create data directory if it doesn’t exist
os.makedirs("data/raw", exist_ok=True)

# OpenWeatherMap API endpoint for current weather
# Documentation: https://openweathermap.org/current
CITY_NAME = "San Jose"
API_URL = (
    f"https://api.openweathermap.org/data/2.5/weather?"
    f"q={CITY_NAME}&appid={WEATHER_API_KEY}&units=metric"
)

def fetch_weather_data():
    """
    Fetches current weather data for San Jose from the OpenWeatherMap API.
    Returns a dictionary or None if the request fails.
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("Successfully fetched weather data from OpenWeatherMap.")
        return data

    except requests.exceptions.RequestException as e:
        print(f"Network/API error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def parse_weather_data(data):
    """
    Extracts useful information from the API response and converts it to a DataFrame.
    """
    if data is None:
        return None

    # Extract key weather data
    weather_info = {
        "city": data.get("name"),
        "timestamp": datetime.now(),
        "temp": data["main"].get("temp") if "main" in data else None,
        "feels_like": data["main"].get("feels_like") if "main" in data else None,
        "humidity": data["main"].get("humidity") if "main" in data else None,
        "pressure": data["main"].get("pressure") if "main" in data else None,
        "wind_speed": data["wind"].get("speed") if "wind" in data else None,
        "weather_main": data["weather"][0].get("main") if "weather" in data and len(data["weather"]) > 0 else None,
        "weather_description": data["weather"][0].get("description") if "weather" in data and len(data["weather"]) > 0 else None
    }

    df = pd.DataFrame([weather_info])
    return df

def save_weather_data(df):
    """
    Saves the weather DataFrame to a CSV file in the data/raw folder.
    """
    if df is not None and not df.empty:
        filename = f"data/raw/weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        print(f"Weather data saved to {filename}")
    else:
        print("No data to save (empty or invalid response).")

if __name__ == "__main__":
    print("Collecting real-time weather data for San Jose, CA...")
    data = fetch_weather_data()
    df = parse_weather_data(data)
    save_weather_data(df)
    print("Weather data collection complete.")
