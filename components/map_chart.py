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
        zoom_level = 7.0
    else:
        center_lat = 4.2105
        center_lon = 108.9758 if len(map_df[map_df['state'].str.contains('SABAH|SARAWAK', na=False)]) > 0 else 101.9758
        zoom_level = 5.3

    hover_text = []
    marker_sizes = []
    marker_opacities = []

    for idx, row in map_df.iterrows():
        wl_str = f"{row['water_level_current']:.2f} m" if pd.notnull(row['water_level_current']) else "N/A"
        wl_danger = f"{row['water_level_danger_level']:.2f} m" if pd.notnull(row['water_level_danger_level']) else "N/A"
        rf_1h = f"{row['rainfall_latest_1hr']:.1f} mm" if pd.notnull(row['rainfall_latest_1hr']) else "0.0 mm"
        rf_today = f"{row['rainfall_total_today']:.1f} mm" if pd.notnull(row['rainfall_total_today']) else "0.0 mm"
        
        status_badge = row['water_level_indicator'] if row['water_level_indicator'] != 'N/A' else row['rainfall_indicator']
        update_time = row['water_level_update_datetime'] or row['rainfall_update_datetime'] or 'N/A'

        txt = (
            f"<div style='font-family: Plus Jakarta Sans, sans-serif; min-width: 230px; line-height: 1.4;'>"
            f"<div style='font-weight: 800; font-size: 0.95rem; color: #f8fafc; margin-bottom: 2px;'>"
            f"{row['station_name']}</div>"
            f"<div style='font-size: 0.75rem; color: #94a3b8; margin-bottom: 8px;'>"
            f"KOD: <span style='font-family: Roboto Mono, monospace; color: #38bdf8;'>{row['station_code']}</span> | {row['district']}, {row['state']}</div>"
            f"<div style='background: #080e1c; border: 1px solid #1e2d4a; padding: 6px 10px; border-radius: 6px; font-size: 0.78rem;'>"
            f"<table style='width: 100%; border-collapse: collapse;'>"
            f"<tr><td style='color: #94a3b8;'>Status Telemetri:</td><td style='text-align: right; font-weight: 700; font-family: Roboto Mono; color: #f8fafc;'>{status_badge}</td></tr>"
            f"<tr><td style='color: #94a3b8;'>Paras Semasa:</td><td style='text-align: right; font-weight: 700; font-family: Roboto Mono; color: #38bdf8;'>{wl_str}</td></tr>"
            f"<tr><td style='color: #94a3b8;'>Aras Bahaya:</td><td style='text-align: right; font-weight: 700; font-family: Roboto Mono; color: #ef4444;'>{wl_danger}</td></tr>"
            f"<tr><td style='color: #94a3b8;'>Hujan (1j / Hari):</td><td style='text-align: right; font-family: Roboto Mono; color: #60a5fa;'>{rf_1h} / {rf_today}</td></tr>"
            f"</table>"
            f"</div>"
            f"<div style='font-size: 0.7rem; color: #64748b; margin-top: 6px; text-align: right; font-family: Roboto Mono;'>"
            f"Masa: {update_time}</div>"
            f"</div>"
        )
        hover_text.append(txt)

        if selected_station_id and str(row['station_id']) == str(selected_station_id):
            marker_sizes.append(24)
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
                    opacity=0.9
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
            font=dict(color="#f8fafc", size=11, family="Plus Jakarta Sans"),
            bgcolor="rgba(15, 23, 42, 0.9)",
            bordercolor="#1e2d4a",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="#0f172a",
            font_size=12,
            font_family="Plus Jakarta Sans",
            bordercolor="#1e2d4a"
        )
    )

    return fig
