import pandas as pd
import requests
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DataLoader")

API_URL = "https://api.data.gov.my/flood-warning/"

def get_status_color(wl_indicator, rf_indicator=None):
    """Return appropriate hex color for a given status."""
    if wl_indicator == "DANGER":
        return "#ef4444"  # Red
    elif wl_indicator == "WARNING":
        return "#f97316"  # Orange
    elif wl_indicator == "ALERT":
        return "#eab308"  # Yellow
    elif wl_indicator == "NORMAL":
        return "#10b981"  # Emerald Green
    elif wl_indicator == "ERROR":
        return "#64748b"  # Slate Gray
    elif rf_indicator and rf_indicator != "NO_RAINFALL":
        return "#3b82f6"  # Blue for rain active
    else:
        return "#64748b"  # Muted Gray

def fetch_flood_warning_data():
    """Fetch flood warning data from data.gov.my API and return clean DataFrame & metadata."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()
        raw_data = response.json()
        
        if not raw_data:
            logger.warning("Empty data returned from API")
            return pd.DataFrame(), timestamp, False
            
        df = pd.DataFrame(raw_data)
        
        # Ensure numerical types for numeric fields
        num_cols = [
            'latitude', 'longitude', 
            'water_level_current', 'water_level_normal_level', 
            'water_level_alert_level', 'water_level_warning_level', 'water_level_danger_level',
            'water_level_increment', 'rainfall_clean', 'rainfall_latest_1hr', 'rainfall_total_today'
        ]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Fill missing text fields
        df['state'] = df['state'].fillna('TIDAK DIKETAHUI').str.strip()
        df['district'] = df['district'].fillna('TIDAK DIKETAHUI').str.strip()
        df['station_name'] = df['station_name'].fillna('Tanpa Nama')
        df['sub_basin'] = df['sub_basin'].fillna('-')
        df['main_basin'] = df['main_basin'].fillna('-')
        df['water_level_indicator'] = df['water_level_indicator'].fillna('N/A')
        df['rainfall_indicator'] = df['rainfall_indicator'].fillna('N/A')
        df['station_type'] = df['station_type'].fillna('LAIN-LAIN')
        
        # Calculate water level % of danger level if both exist
        df['danger_ratio'] = df.apply(
            lambda r: (r['water_level_current'] / r['water_level_danger_level'] * 100) 
            if pd.notnull(r['water_level_current']) and pd.notnull(r['water_level_danger_level']) and r['water_level_danger_level'] > 0 
            else 0, 
            axis=1
        )
        
        # Map status rank for easy sorting
        rank_map = {'DANGER': 1, 'WARNING': 2, 'ALERT': 3, 'NORMAL': 4, 'ERROR': 5, 'N/A': 6}
        df['status_rank'] = df['water_level_indicator'].map(lambda x: rank_map.get(x, 6))
        
        # Map colors
        df['marker_color'] = df.apply(
            lambda r: get_status_color(r['water_level_indicator'], r['rainfall_indicator']), 
            axis=1
        )
        
        # Display label
        df['full_label'] = df['station_name'] + " (" + df['district'] + ", " + df['state'] + ")"
        
        logger.info(f"Successfully loaded {len(df)} stations at {timestamp}")
        return df, timestamp, True

    except Exception as e:
        logger.error(f"Error fetching API data: {e}")
        return pd.DataFrame(), timestamp, False

if __name__ == "__main__":
    df, ts, success = fetch_flood_warning_data()
    print(f"Fetch success: {success}, Rows: {len(df)}, Timestamp: {ts}")
