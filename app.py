import dash
from dash import html, dcc, Output, Input, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import logging

from data_loader import fetch_flood_warning_data
from components.navbar import create_navbar
from components.kpi_cards import create_kpi_cards
from components.map_chart import create_map_chart
from components.analytics_charts import (
    create_top_danger_chart,
    create_station_threshold_chart,
    create_rainfall_state_chart
)
from components.data_table import create_data_table

logging.basicConfig(level=logging.INFO)

# Initialize Dash App with Darkly theme & Bootstrap icons
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.SLATE,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css"
    ],
    title="Pusat Amaran Banjir Malaysia | MY Flood Dashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
server = app.server

# Global in-memory cache for data
initial_df, initial_ts, _ = fetch_flood_warning_data()

app.layout = dbc.Container(
    [
        # Store components for state management
        dcc.Store(id='raw-data-store'),
        dcc.Store(id='selected-station-store'),
        dcc.Interval(id='interval-refresh', interval=10*60*1000, n_intervals=0), # 10 min refresh

        # Navbar
        html.Div(id='navbar-container', children=create_navbar(initial_ts)),

        # Filter Control Panel
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("📍 Negeri", className="form-label text-muted small fw-bold mb-1"),
                                    dcc.Dropdown(
                                        id='filter-state',
                                        options=[{'label': 'Semua Negeri', 'value': 'ALL'}] + [
                                            {'label': s, 'value': s} for s in sorted(initial_df['state'].unique()) if s
                                        ],
                                        value='ALL',
                                        clearable=False,
                                        className="dash-dropdown"
                                    )
                                ],
                                xs=12, sm=6, md=3, className="mb-2 mb-md-0"
                            ),
                            dbc.Col(
                                [
                                    html.Label("🏙️ Daerah", className="form-label text-muted small fw-bold mb-1"),
                                    dcc.Dropdown(
                                        id='filter-district',
                                        options=[{'label': 'Semua Daerah', 'value': 'ALL'}],
                                        value='ALL',
                                        clearable=False,
                                        className="dash-dropdown"
                                    )
                                ],
                                xs=12, sm=6, md=3, className="mb-2 mb-md-0"
                            ),
                            dbc.Col(
                                [
                                    html.Label("🚨 Status Paras Air", className="form-label text-muted small fw-bold mb-1"),
                                    dcc.Dropdown(
                                        id='filter-status',
                                        options=[
                                            {'label': 'Semua Status', 'value': 'ALL'},
                                            {'label': '🔴 BAHAYA (Danger)', 'value': 'DANGER'},
                                            {'label': '🟠 AMARAN (Warning)', 'value': 'WARNING'},
                                            {'label': '🟡 WASPADA (Alert)', 'value': 'ALERT'},
                                            {'label': '🟢 NORMAL', 'value': 'NORMAL'},
                                            {'label': '⚪ ERROR / OFF', 'value': 'ERROR'}
                                        ],
                                        value='ALL',
                                        clearable=False,
                                        className="dash-dropdown"
                                    )
                                ],
                                xs=12, sm=6, md=3, className="mb-2 mb-md-0"
                            ),
                            dbc.Col(
                                [
                                    html.Label("🔍 Carian Stesen / Kod", className="form-label text-muted small fw-bold mb-1"),
                                    dbc.Input(
                                        id='filter-search',
                                        type='text',
                                        placeholder='Taip nama stesen / sungai...',
                                        style={"backgroundColor": "#0f172a", "borderColor": "#334155", "color": "#f8fafc"}
                                    )
                                ],
                                xs=12, sm=6, md=3
                            )
                        ],
                        className="align-items-end g-2"
                    )
                ]
            ),
            className="dash-card mb-4"
        ),

        # KPI Summary Cards
        html.Div(id='kpi-container', children=create_kpi_cards(initial_df)),

        # Main Geospatial Map & Detail Analytics Section
        dbc.Row(
            [
                # Left Column: Map
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.Div(
                                    [
                                        html.Span("🗺️ Peta Lokasi Stesen Telemetri (Malaysia)", className="card-header-title"),
                                        html.Span("Klik penanda stesen untuk melihat maklumat terperinci", className="text-muted small ms-2 d-none d-md-inline")
                                    ],
                                    className="d-flex justify-content-between align-items-center"
                                ),
                                style={"backgroundColor": "#0f172a", "borderColor": "#334155"}
                            ),
                            dbc.CardBody(
                                dcc.Graph(
                                    id='map-chart',
                                    figure=create_map_chart(initial_df),
                                    style={"height": "580px"},
                                    config={"displayModeBar": False}
                                ),
                                className="p-0"
                            )
                        ],
                        className="dash-card h-100"
                    ),
                    xs=12, lg=7, className="mb-4 mb-lg-0"
                ),

                # Right Column: Analytics Charts
                dbc.Col(
                    [
                        # Selected Station Gauge / Threshold Chart
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "📊 Status Ambang Paras Air Stesen Terpilih",
                                    className="card-header-title",
                                    style={"backgroundColor": "#0f172a", "borderColor": "#334155"}
                                ),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id='gauge-chart',
                                        figure=create_station_threshold_chart(initial_df),
                                        style={"height": "260px"},
                                        config={"displayModeBar": False}
                                    ),
                                    className="p-1"
                                )
                            ],
                            className="dash-card mb-4"
                        ),

                        # Top Danger Bar Chart
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "⚠️ 10 Stesen Paling Hampir Aras Bahaya",
                                    className="card-header-title",
                                    style={"backgroundColor": "#0f172a", "borderColor": "#334155"}
                                ),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id='top-danger-chart',
                                        figure=create_top_danger_chart(initial_df),
                                        style={"height": "270px"},
                                        config={"displayModeBar": False}
                                    ),
                                    className="p-1"
                                )
                            ],
                            className="dash-card"
                        )
                    ],
                    xs=12, lg=5
                )
            ],
            className="mb-4 g-3"
        ),

        # Secondary Analytics Section: Rainfall Chart
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "🌧️ Rekod Hujan Paling Tinggi Mengikut Negeri (Hari Ini)",
                                className="card-header-title",
                                style={"backgroundColor": "#0f172a", "borderColor": "#334155"}
                            ),
                            dbc.CardBody(
                                dcc.Graph(
                                    id='rainfall-chart',
                                    figure=create_rainfall_state_chart(initial_df),
                                    style={"height": "280px"},
                                    config={"displayModeBar": False}
                                )
                            )
                        ],
                        className="dash-card mb-4"
                    ),
                    width=12
                )
            ]
        ),

        # Data Table Section
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            html.Div(
                                id='table-container',
                                children=create_data_table(initial_df)
                            )
                        ),
                        className="dash-card mb-5"
                    ),
                    width=12
                )
            ]
        ),

        # Footer
        html.Footer(
            dbc.Container(
                html.Div(
                    [
                        html.Span("Pusat Amaran Banjir Malaysia © 2026. Data bersumberkan "),
                        html.A("api.data.gov.my", href="https://api.data.gov.my/flood-warning/", target="_blank", style={"color": "#3b82f6"}),
                        html.Span(" | Dibina menggunakan Dash Python & Plotly.")
                    ],
                    className="text-center text-muted small py-3"
                )
            )
        )
    ],
    fluid=True,
    className="px-3 px-md-4 py-2"
)


# Callback 1: Data Refresh & Store Update
@app.callback(
    [Output('raw-data-store', 'data'),
     Output('navbar-container', 'children')],
    [Input('btn-refresh', 'n_clicks'),
     Input('interval-refresh', 'n_intervals')]
)
def refresh_api_data(n_clicks, n_intervals):
    df, timestamp, success = fetch_flood_warning_data()
    nav = create_navbar(timestamp)
    records = df.to_dict('records') if not df.empty else []
    return records, nav


# Callback 2: Update District options when State changes
@app.callback(
    Output('filter-district', 'options'),
    [Input('filter-state', 'value'),
     Input('raw-data-store', 'data')]
)
def update_district_options(selected_state, stored_data):
    if not stored_data:
        return [{'label': 'Semua Daerah', 'value': 'ALL'}]
    
    df = pd.DataFrame(stored_data)
    if selected_state and selected_state != 'ALL':
        df = df[df['state'] == selected_state]
    
    districts = sorted([d for d in df['district'].unique() if d])
    options = [{'label': 'Semua Daerah', 'value': 'ALL'}] + [{'label': d, 'value': d} for d in districts]
    return options


# Callback 3: Map Click station selection
@app.callback(
    Output('selected-station-store', 'data'),
    [Input('map-chart', 'clickData')]
)
def handle_map_click(click_data):
    if click_data and 'points' in click_data and len(click_data['points']) > 0:
        point = click_data['points'][0]
        if 'customdata' in point:
            return point['customdata']
    return None


# Callback 4: Filter Data and Update Views (KPIs, Map, Charts, Table)
@app.callback(
    [Output('kpi-container', 'children'),
     Output('map-chart', 'figure'),
     Output('gauge-chart', 'figure'),
     Output('top-danger-chart', 'figure'),
     Output('rainfall-chart', 'figure'),
     Output('table-container', 'children')],
    [Input('raw-data-store', 'data'),
     Input('filter-state', 'value'),
     Input('filter-district', 'value'),
     Input('filter-status', 'value'),
     Input('filter-search', 'value'),
     Input('selected-station-store', 'data')]
)
def update_dashboard_views(stored_data, state, district, status, search, selected_station_id):
    if not stored_data:
        df = pd.DataFrame()
    else:
        df = pd.DataFrame(stored_data)

    filtered_df = df.copy()

    # Apply Filters
    if not filtered_df.empty:
        if state and state != 'ALL':
            filtered_df = filtered_df[filtered_df['state'] == state]
        
        if district and district != 'ALL':
            filtered_df = filtered_df[filtered_df['district'] == district]
            
        if status and status != 'ALL':
            filtered_df = filtered_df[filtered_df['water_level_indicator'] == status]
            
        if search and search.strip():
            query = search.strip().lower()
            filtered_df = filtered_df[
                filtered_df['station_name'].str.lower().str.contains(query, na=False) |
                filtered_df['station_code'].str.lower().str.contains(query, na=False) |
                filtered_df['district'].str.lower().str.contains(query, na=False) |
                filtered_df['sub_basin'].str.lower().str.contains(query, na=False)
            ]

    # Generate Updated Components
    kpi_view = create_kpi_cards(filtered_df)
    map_view = create_map_chart(filtered_df, selected_station_id=selected_station_id)
    gauge_view = create_station_threshold_chart(df if filtered_df.empty else filtered_df, station_id=selected_station_id)
    top_danger_view = create_top_danger_chart(filtered_df)
    rainfall_view = create_rainfall_state_chart(filtered_df)
    table_view = create_data_table(filtered_df)

    return kpi_view, map_view, gauge_view, top_danger_view, rainfall_view, table_view


if __name__ == '__main__':
    print("🚀 Starting MY Flood Warning Dashboard server on http://127.0.0.1:8050 ...")
    app.run_server(debug=True, host='0.0.0.0', port=8050)
