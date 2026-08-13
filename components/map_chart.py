import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_map_chart(df, selected_station_id=None):
    if df.empty:
        # Fallback empty map centered on Malaysia
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style="carto-darkmatter",
                center=dict(lat=4.2105, lon=101.9758),
                zoom=5.5
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            font=dict(color="#f8fafc")
        )
        return fig

    # Filter out rows with invalid coordinates
    map_df = df[df['latitude'].notnull() & df['longitude'].notnull()].copy()
    
    # Calculate map center dynamically if filtered, else default to Malaysia center
    if len(map_df) > 0 and len(map_df) < len(df):
        center_lat = map_df['latitude'].mean()
        center_lon = map_df['longitude'].mean()
        zoom_level = 7
    else:
        center_lat = 4.2105
        center_lon = 108.9758 if len(map_df[map_df['state'].str.contains('SABAH|SARAWAK', na=False)]) > 0 else 101.9758
        zoom_level = 5.2

    # Map hover text preparation
    hover_text = []
    marker_sizes = []
    marker_opacities = []

    for idx, row in map_df.iterrows():
        wl_str = f"{row['water_level_current']:.2f} m" if pd.notnull(row['water_level_current']) else "N/A"
        wl_danger = f"{row['water_level_danger_level']:.2f} m" if pd.notnull(row['water_level_danger_level']) else "N/A"
        rf_1h = f"{row['rainfall_latest_1hr']:.1f} mm" if pd.notnull(row['rainfall_latest_1hr']) else "N/A"
        rf_today = f"{row['rainfall_total_today']:.1f} mm" if pd.notnull(row['rainfall_total_today']) else "N/A"
        
        status_badge = row['water_level_indicator'] if row['water_level_indicator'] != 'N/A' else row['rainfall_indicator']

        txt = (
            f"<b>{row['station_name']}</b> ({row['station_code']})<br>"
            f"📍 {row['district']}, {row['state']}<br>"
            f"🌊 <b>Status Paras Air:</b> {status_badge}<br>"
            f"💧 <b>Paras Semasa:</b> {wl_str} (Bahaya: {wl_danger})<br>"
            f"🌧️ <b>Hujan (1 Jam / Hari Ini):</b> {rf_1h} / {rf_today}<br>"
            f"🕒 <b>Kemaskini:</b> {row['water_level_update_datetime'] or row['rainfall_update_datetime'] or 'N/A'}"
        )
        hover_text.append(txt)

        # Highlight danger/warning/selected markers with larger size
        if selected_station_id and str(row['station_id']) == str(selected_station_id):
            marker_sizes.append(22)
            marker_opacities.append(1.0)
        elif row['water_level_indicator'] == 'DANGER':
            marker_sizes.append(16)
            marker_opacities.append(0.95)
        elif row['water_level_indicator'] in ['WARNING', 'ALERT']:
            marker_sizes.append(13)
            marker_opacities.append(0.9)
        else:
            marker_sizes.append(9)
            marker_opacities.append(0.75)

    map_df['hover_text'] = hover_text
    map_df['marker_size'] = marker_sizes
    map_df['marker_opacity'] = marker_opacities

    fig = go.Figure()

    # Add traces grouped by water_level_indicator for a clean map legend
    indicator_order = ['DANGER', 'WARNING', 'ALERT', 'NORMAL', 'ERROR', 'N/A']
    color_map = {
        'DANGER': '#ef4444',
        'WARNING': '#f97316',
        'ALERT': '#eab308',
        'NORMAL': '#10b981',
        'ERROR': '#64748b',
        'N/A': '#475569'
    }

    for ind in indicator_order:
        sub_df = map_df[map_df['water_level_indicator'] == ind]
        if sub_df.empty:
            continue

        fig.add_trace(
            go.Scattermapbox(
                lat=sub_df['latitude'],
                lon=sub_df['longitude'],
                mode='markers',
                marker=dict(
                    size=sub_df['marker_size'],
                    color=color_map.get(ind, '#64748b'),
                    opacity=0.85
                ),
                text=sub_df['hover_text'],
                hoverinfo='text',
                name=f"Status: {ind}",
                customdata=sub_df['station_id']
            )
        )

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=zoom_level
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.02,
            xanchor="left",
            x=0.02,
            font=dict(color="#f8fafc", size=11),
            bgcolor="rgba(30, 41, 59, 0.85)",
            bordercolor="#334155",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="#1e293b",
            font_size=12,
            font_family="Plus Jakarta Sans",
            bordercolor="#334155"
        )
    )

    return fig
