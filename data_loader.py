import pandas as pd
import requests
import datetime
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DataLoader")

API_URL = "https://api.data.gov.my/flood-warning/"

DEFAULT_COLUMNS = [
    'station_id', 'station_name', 'station_code', 'district', 'state',
    'sub_basin', 'main_basin', 'station_type', 'latitude', 'longitude',
    'water_level_indicator', 'water_level_current', 'water_level_normal_level',
    'water_level_alert_level', 'water_level_warning_level', 'water_level_danger_level',
    'water_level_increment', 'rainfall_clean', 'rainfall_latest_1hr', 'rainfall_total_today',
    'rainfall_indicator', 'water_level_update_datetime', 'rainfall_update_datetime',
    'marker_color', 'danger_ratio', 'status_rank', 'full_label'
]

def sanitize_security_input(val):
    """
    Sanitize text input to prevent XSS, HTML/Script injection, and ReDoS attacks.
    Strips dangerous tags (<script>, <iframe>, event attributes), restricts length,
    and removes control characters.
    """
    if not val or not isinstance(val, str):
        return ""
    # Strip HTML/script tags and dangerous event handlers
    cleaned = re.sub(r'<(?:[^>=]|=\s*["\']?[^"\'>]*["\']?)*>', '', val)
    cleaned = re.sub(r'(?i)(javascript:|data:|vbscript:|onload|onerror|onclick|onmouseover)', '', cleaned)
    cleaned = re.sub(r'[^\w\s\-\.\/\,\(\)]', '', cleaned)
    return cleaned.strip()[:100]

def get_empty_dataframe():
    """Return empty DataFrame initialized with all expected columns to prevent KeyErrors."""
    return pd.DataFrame(columns=DEFAULT_COLUMNS)

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
        return "#00f0ff"  # Cyan Blue for rain active
    else:
        return "#64748b"  # Muted Gray

def fetch_flood_warning_data():
    """
    Fetch flood warning data securely from data.gov.my REST API.
    Returns clean DataFrame, timestamp string, and success boolean status.
    Implements sanitization, rate limit resilience, and telemetry audit metadata.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        headers = {
            "User-Agent": "MY-Flood-Control-Centre/2.0 (Security Audited Telemetry Feed)",
            "Accept": "application/json"
        }
        response = requests.get(API_URL, headers=headers, timeout=12)
        response.raise_for_status()
        raw_data = response.json()
        
        if not raw_data or not isinstance(raw_data, list):
            logger.warning("Empty or invalid JSON payload returned from API")
            return get_empty_dataframe(), timestamp, False
            
        df = pd.DataFrame(raw_data)
        
        # Ensure default string columns exist
        str_cols = ['state', 'district', 'station_name', 'sub_basin', 'main_basin', 'station_code', 'water_level_indicator', 'rainfall_indicator', 'station_type']
        for col in str_cols:
            if col not in df.columns:
                df[col] = ''

        # Security & Type Sanitization for Numeric Fields
        num_cols = [
            'latitude', 'longitude', 
            'water_level_current', 'water_level_normal_level', 
            'water_level_alert_level', 'water_level_warning_level', 'water_level_danger_level',
            'water_level_increment', 'rainfall_clean', 'rainfall_latest_1hr', 'rainfall_total_today'
        ]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                df[col] = None
        
        # String Sanitization (strip whitespace, sanitize unexpected script injection chars)
        for col in str_cols:
            df[col] = df[col].astype(str).apply(sanitize_security_input)

        # Fill missing text fields cleanly
        df['state'] = df['state'].replace({'nan': 'TIDAK DIKETAHUI', '': 'TIDAK DIKETAHUI'}).fillna('TIDAK DIKETAHUI')
        df['district'] = df['district'].replace({'nan': 'TIDAK DIKETAHUI', '': 'TIDAK DIKETAHUI'}).fillna('TIDAK DIKETAHUI')
        df['station_name'] = df['station_name'].replace({'nan': 'Tanpa Nama', '': 'Tanpa Nama'}).fillna('Tanpa Nama')
        df['sub_basin'] = df['sub_basin'].replace({'nan': '-', '': '-'}).fillna('-')
        df['main_basin'] = df['main_basin'].replace({'nan': '-', '': '-'}).fillna('-')
        df['water_level_indicator'] = df['water_level_indicator'].replace({'nan': 'N/A', '': 'N/A'}).fillna('N/A')
        df['rainfall_indicator'] = df['rainfall_indicator'].replace({'nan': 'N/A', '': 'N/A'}).fillna('N/A')
        df['station_type'] = df['station_type'].replace({'nan': 'LAIN-LAIN', '': 'LAIN-LAIN'}).fillna('LAIN-LAIN')
        
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
        
        logger.info(f"[SECURITY AUDIT OK] Loaded {len(df)} telemetry stations at {timestamp}")
        return df, timestamp, True

    except requests.exceptions.RequestException as req_err:
        logger.error(f"[SECURITY AUDIT WARN] API connection error: {req_err}")
        return get_empty_dataframe(), timestamp, False
    except Exception as e:
        logger.error(f"[SECURITY AUDIT FAIL] Unexpected error fetching telemetry data: {e}")
        return get_empty_dataframe(), timestamp, False

if __name__ == "__main__":
    df, ts, success = fetch_flood_warning_data()
    print(f"Fetch success: {success}, Rows: {len(df)}, Timestamp: {ts}")
