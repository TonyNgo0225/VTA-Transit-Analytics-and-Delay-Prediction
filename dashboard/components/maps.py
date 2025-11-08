"""
maps.py
-------
Author: Tony Ngo

Description:
    This module provides interactive map functions for the VTA Transit
    Analytics Dashboard. It visualizes vehicle locations using latitude 
    and longitude data from the VTA API.

This program:
    - Plots VTA bus and light rail positions on an interactive map.
    - Supports optional filtering by route or vehicle type.
    - Can be displayed in the Streamlit app using the streamlit-folium library.
"""

import folium
from streamlit_folium import st_folium

def generate_vta_map(df, map_center=(37.3337, -121.8907), zoom_start=12, route_filter=None):
    """
    Generates an interactive map showing VTA vehicle positions.

    Parameters:
        df (pd.DataFrame): DataFrame containing VTA vehicle data with
                           'latitude', 'longitude', and optionally 'route_id'.
        map_center (tuple): Center of the map (latitude, longitude).
        zoom_start (int): Initial zoom level.
        route_filter (str): Optional route ID to filter vehicles by route.

    Returns:
        folium.Map: Folium map object with markers for each vehicle.
    """
    if df is None or df.empty:
        raise ValueError("No data available for map visualization.")

    # Filter by route if selec

