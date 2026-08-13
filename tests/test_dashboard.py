import pytest
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_loader import fetch_flood_warning_data, get_status_color
from components.kpi_cards import create_kpi_cards
from components.map_chart import create_map_chart
from components.analytics_charts import (
    create_top_danger_chart,
    create_station_threshold_chart,
    create_rainfall_state_chart
)
from components.data_table import create_data_table

def test_get_status_color():
    assert get_status_color('DANGER') == '#ef4444'
    assert get_status_color('WARNING') == '#f97316'
    assert get_status_color('ALERT') == '#eab308'
    assert get_status_color('NORMAL') == '#10b981'
    assert get_status_color('ERROR') == '#64748b'

def test_fetch_flood_warning_data(requests_mock):
    mock_data = [{
        'station_id': '101',
        'station_name': 'Test Station',
        'station_code': 'TST01',
        'district': 'Kuala Lumpur',
        'state': 'WILAYAH PERSEKUTUAN KUALA LUMPUR',
        'latitude': '3.1390',
        'longitude': '101.6869',
        'water_level_current': '2.5',
        'water_level_danger_level': '3.0',
        'water_level_indicator': 'WARNING'
    }]
    requests_mock.get('https://api.data.gov.my/flood-warning/', json=mock_data)

    df, timestamp, success = fetch_flood_warning_data()
    assert success is True
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'station_id' in df.columns
    assert 'water_level_indicator' in df.columns
    assert 'latitude' in df.columns
    assert 'longitude' in df.columns

def test_components_layout_rendering():
    # Mock sample DataFrame
    sample_df = pd.DataFrame([{
        'station_id': '101',
        'station_name': 'Test Station',
        'station_code': 'TST01',
        'district': 'Kuala Lumpur',
        'state': 'WILAYAH PERSEKUTUAN KUALA LUMPUR',
        'sub_basin': 'Sg. Klang',
        'main_basin': 'Sungai Klang',
        'latitude': 3.1390,
        'longitude': 101.6869,
        'water_level_current': 2.5,
        'water_level_normal_level': 1.0,
        'water_level_alert_level': 2.0,
        'water_level_warning_level': 2.3,
        'water_level_danger_level': 3.0,
        'water_level_indicator': 'WARNING',
        'rainfall_latest_1hr': 5.0,
        'rainfall_total_today': 20.0,
        'rainfall_indicator': 'LIGHT',
        'water_level_update_datetime': '2026-08-13 12:00:00',
        'rainfall_update_datetime': '2026-08-13 12:00:00',
        'marker_color': '#f97316',
        'danger_ratio': 83.3,
        'full_label': 'Test Station (Kuala Lumpur, WILAYAH PERSEKUTUAN KUALA LUMPUR)'
    }])

    kpi = create_kpi_cards(sample_df)
    assert kpi is not None

    map_fig = create_map_chart(sample_df)
    assert map_fig is not None

    top_danger_fig = create_top_danger_chart(sample_df)
    assert top_danger_fig is not None

    gauge_fig = create_station_threshold_chart(sample_df, station_id='101')
    assert gauge_fig is not None

    rainfall_fig = create_rainfall_state_chart(sample_df)
    assert rainfall_fig is not None

    dt = create_data_table(sample_df)
    assert dt is not None
