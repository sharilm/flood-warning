import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_top_danger_chart(df):
    """Bar chart showing stations with highest water level relative to danger threshold."""
    if df.empty:
        fig = go.Figure()
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig

    # Filter stations with valid current & danger levels
    valid_df = df[df['water_level_current'].notnull() & df['water_level_danger_level'].notnull()].copy()
    if valid_df.empty:
        valid_df = df[df['water_level_current'].notnull()].copy()
        valid_df['water_level_danger_level'] = 0

    # Sort by danger ratio or water level
    valid_df = valid_df.sort_values(by=['danger_ratio', 'water_level_current'], ascending=False).head(10)
    valid_df['short_name'] = valid_df['station_name'].str.slice(0, 20) + " (" + valid_df['state'].str.slice(0, 10) + ")"

    fig = go.Figure()

    # Current Water Level Bar
    fig.add_trace(
        go.Bar(
            y=valid_df['short_name'],
            x=valid_df['water_level_current'],
            name='Paras Semasa (m)',
            orientation='h',
            marker=dict(
                color=valid_df['marker_color'],
                line=dict(color='#334155', width=1)
            ),
            hovertemplate="<b>%{y}</b><br>Paras Semasa: %{x:.2f} m<extra></extra>"
        )
    )

    # Danger Level Marker Lines
    fig.add_trace(
        go.Scatter(
            y=valid_df['short_name'],
            x=valid_df['water_level_danger_level'],
            name='Aras Bahaya (m)',
            mode='markers',
            marker=dict(color='#ef4444', symbol='line-ns', size=16, line_width=3),
            hovertemplate="<b>Aras Bahaya:</b> %{x:.2f} m<extra></extra>"
        )
    )

    fig.update_layout(
        title=dict(
            text="Top 10 Stesen Dekat / Melepasi Aras Bahaya",
            font=dict(color="#f8fafc", size=14, family="Plus Jakarta Sans")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=20, t=40, b=20),
        xaxis=dict(
            title=dict(text="Paras Air (Metres)", font=dict(color="#94a3b8", size=11)),
            tickfont=dict(color="#cbd5e1"),
            gridcolor="#334155"
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(color="#cbd5e1", size=11),
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#94a3b8", size=10)
        ),
        height=320
    )
    return fig


def create_station_threshold_chart(df, station_id=None):
    """Bullet / Gauge Chart for a single selected station showing levels vs thresholds."""
    if df.empty:
        return go.Figure()

    if station_id:
        st_row = df[df['station_id'].astype(str) == str(station_id)]
    else:
        # Default to highest danger station or first station
        danger_st = df[df['water_level_indicator'] == 'DANGER']
        st_row = danger_st.iloc[[0]] if not danger_st.empty else df.iloc[[0]]

    if st_row.empty:
        return go.Figure()

    row = st_row.iloc[0]
    st_name = row['station_name']
    district = row['district']
    state = row['state']
    curr = row['water_level_current'] or 0.0
    normal = row['water_level_normal_level'] or 0.0
    alert = row['water_level_alert_level'] or 0.0
    warning = row['water_level_warning_level'] or 0.0
    danger = row['water_level_danger_level'] or 0.0
    indicator = row['water_level_indicator']

    max_range = max(curr, danger, warning, alert, normal, 1.0) * 1.25

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=curr,
            number={'suffix': " m", 'font': {'color': "#f8fafc", 'size': 28}},
            title={'text': f"<b>{st_name}</b><br><span style='font-size:0.8em;color:#94a3b8;'>{district}, {state} | Status: {indicator}</span>", 'font': {'color': "#f8fafc", 'size': 13}},
            gauge={
                'axis': {'range': [0, max_range], 'tickwidth': 1, 'tickcolor': "#94a3b8", 'tickfont': {'color': "#94a3b8"}},
                'bar': {'color': row['marker_color'], 'thickness': 0.4},
                'bgcolor': "#1e293b",
                'borderwidth': 1,
                'bordercolor': "#334155",
                'steps': [
                    {'range': [0, normal], 'color': '#064e3b'},
                    {'range': [normal, alert], 'color': '#713f12'},
                    {'range': [alert, warning], 'color': '#7c2d12'},
                    {'range': [warning, max_range], 'color': '#7f1d1d'}
                ],
                'threshold': {
                    'line': {'color': "#ef4444", 'width': 4},
                    'thickness': 0.75,
                    'value': danger
                }
            }
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=60, b=10),
        height=320
    )
    return fig


def create_rainfall_state_chart(df):
    """Bar chart summarizing total today's rainfall by state."""
    if df.empty or 'rainfall_total_today' not in df.columns:
        return go.Figure()

    rf_df = df[df['rainfall_total_today'].notnull() & (df['rainfall_total_today'] > 0)].copy()
    if rf_df.empty:
        # Dummy empty state chart
        fig = go.Figure()
        fig.add_annotation(text="Tiada rekod hujan aktif hari ini", showarrow=False, font=dict(color="#94a3b8", size=14))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=320)
        return fig

    state_rf = rf_df.groupby('state')['rainfall_total_today'].agg(['max', 'mean', 'count']).reset_index()
    state_rf = state_rf.sort_values(by='max', ascending=True).tail(10)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=state_rf['state'],
            x=state_rf['max'],
            name='Maks Hujan Hari Ini (mm)',
            orientation='h',
            marker=dict(color='#3b82f6', line=dict(color='#1d4ed8', width=1)),
            hovertemplate="<b>%{y}</b><br>Hujan Maksimum: %{x:.1f} mm<extra></extra>"
        )
    )

    fig.update_layout(
        title=dict(
            text="Top 10 Negeri Rekod Hujan Paling Tinggi (mm)",
            font=dict(color="#f8fafc", size=14, family="Plus Jakarta Sans")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=20, t=40, b=20),
        xaxis=dict(
            title=dict(text="Jumlah Hujan (mm)", font=dict(color="#94a3b8", size=11)),
            tickfont=dict(color="#cbd5e1"),
            gridcolor="#334155"
        ),
        yaxis=dict(
            tickfont=dict(color="#cbd5e1", size=11),
            showgrid=False
        ),
        height=320
    )
    return fig
