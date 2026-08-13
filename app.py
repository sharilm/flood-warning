import dash
from dash import html, dcc, Output, Input, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import logging
import re

from data_loader import fetch_flood_warning_data, sanitize_security_input
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
    title="Pusat Kawalan Bencana Negara (NDCC) | NADMA Malaysia",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
server = app.server

# ==============================================================================
# SECURITY SOP MIDDLEWARE - OWASP STANDARD HTTP SECURITY HEADERS
# ==============================================================================
@server.after_request
def apply_security_sop_headers(response):
    """
    Enforce OWASP standard security headers on every HTTP response to defend
    against XSS, Clickjacking, MIME-sniffing, SSL stripping & MITM attacks.
    """
    csp_policy = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
        "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net data:; "
        "img-src 'self' data: https://*.cartocdn.com https://*.tile.openstreetmap.org https://api.mapbox.com; "
        "connect-src 'self' https://api.data.gov.my https://*.cartocdn.com; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self';"
    )
    response.headers['Content-Security-Policy'] = csp_policy
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=(), payment=(), usb=()'
    response.headers['Server'] = 'MY-NDCC-Secure-Gateway/2.0'
    response.headers['X-Powered-By'] = 'NADMA-Security-Layer'
    return response

# Global initial data fetch
initial_df, initial_ts, _ = fetch_flood_warning_data()

def create_alert_ticker(df):
    """Generate dynamic tactical alert banner based on active critical stations."""
    if df.empty:
        return html.Div(
            [
                html.I(className="bi bi-shield-exclamation me-2 fs-5 text-warning"),
                html.Span("Sistem sedang memuatkan data telemetri terkini...")
            ],
            className="ticker-banner normal mb-3"
        )
    
    danger_df = df[df['water_level_indicator'] == 'DANGER']
    warning_df = df[df['water_level_indicator'] == 'WARNING']
    
    if not danger_df.empty:
        danger_count = len(danger_df)
        states_affected = ", ".join(sorted(danger_df['state'].unique())[:3])
        return html.Div(
            [
                html.Span(className="led-indicator led-red me-1"),
                html.I(className="bi bi-exclamation-triangle-fill fs-5 text-danger me-2"),
                html.Div(
                    [
                        html.Span(f"PERHATIAN OPERASI: {danger_count} STESEN MENGESAN PARAS BAHAYA! ", className="fw-bold text-uppercase me-1"),
                        html.Span(f"Tindakan evakuasi & kawalan di negeri: {states_affected}.", className="small opacity-90")
                    ]
                )
            ],
            className="ticker-banner danger mb-3"
        )
    elif not warning_df.empty:
        warning_count = len(warning_df)
        return html.Div(
            [
                html.Span(className="led-indicator led-orange me-1"),
                html.I(className="bi bi-exclamation-circle-fill fs-5 text-warning me-2"),
                html.Div(
                    [
                        html.Span(f"STATUS SIAP SAGA: {warning_count} Stesen Pada Aras Amaran. ", className="fw-bold text-uppercase me-1"),
                        html.Span("Sistem bilik gerakan disaster command bersedia 24 jam.", className="small opacity-90")
                    ]
                )
            ],
            className="ticker-banner warning mb-3"
        )
    else:
        return html.Div(
            [
                html.Span(className="led-indicator led-green me-1"),
                html.I(className="bi bi-shield-check fs-5 text-success me-2"),
                html.Div(
                    [
                        html.Span("STATUS OPERASI NORMAL: ", className="fw-bold me-1"),
                        html.Span("Semua stesen telemetri berada dalam lingkungan paras kawalan selamat.", className="small opacity-90")
                    ]
                )
            ],
            className="ticker-banner normal mb-3"
        )

app.layout = dbc.Container(
    [
        # Store components for state management
        dcc.Store(id='raw-data-store'),
        dcc.Store(id='selected-station-store'),
        dcc.Interval(id='interval-refresh', interval=10*60*1000, n_intervals=0), # 10 min auto refresh

        # Navbar & Security Status Header
        html.Div(id='navbar-container', children=create_navbar(initial_ts)),

        # Operational Alert Ticker Banner
        html.Div(id='alert-ticker-container', children=create_alert_ticker(initial_df)),

        # mmand Control Filter Panel
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            # Filter State
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            html.I(className="bi bi-geo-alt-fill me-1 text-primary"),
                                            html.Label("Negeri", className="form-label-tactical mb-0")
                                        ],
                                        className="d-flex align-items-center mb-1"
                                    ),
                                    dcc.Dropdown(
                                        id='filter-state',
                                        options=[{'label': 'Semua Negeri (Kebangsaan)', 'value': 'ALL'}] + (
                                            [{'label': s, 'value': s} for s in sorted(initial_df['state'].unique()) if s]
                                            if not initial_df.empty and 'state' in initial_df.columns else []
                                        ),
                                        value='ALL',
                                        clearable=False,
                                        className="dash-dropdown"
                                    )
                                ],
                                xs=12, sm=6, md=3, className="mb-2 mb-md-0"
                            ),
                            # Filter District
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            html.I(className="bi bi-building me-1 text-info"),
                                            html.Label("Daerah", className="form-label-tactical mb-0")
                                        ],
                                        className="d-flex align-items-center mb-1"
                                    ),
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
                            # Filter Status
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            html.I(className="bi bi-sliders me-1 text-warning"),
                                            html.Label("Status Ambang Air", className="form-label-tactical mb-0")
                                        ],
                                        className="d-flex align-items-center mb-1"
                                    ),
                                    dcc.Dropdown(
                                        id='filter-status',
                                        options=[
                                            {'label': 'Semua Status Telemetri', 'value': 'ALL'},
                                            {'label': '🔴 DANGER (Bahaya)', 'value': 'DANGER'},
                                            {'label': '🟠 WARNING (Amaran)', 'value': 'WARNING'},
                                            {'label': '🟡 ALERT (Waspada)', 'value': 'ALERT'},
                                            {'label': '🟢 NORMAL (Selamat)', 'value': 'NORMAL'},
                                            {'label': '⚪ ERROR / Ralat', 'value': 'ERROR'}
                                        ],
                                        value='ALL',
                                        clearable=False,
                                        className="dash-dropdown"
                                    )
                                ],
                                xs=12, sm=6, md=3, className="mb-2 mb-md-0"
                            ),
                            # Search Box
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            html.I(className="bi bi-search me-1 text-info"),
                                            html.Label("Carian Stesen / Sungai", className="form-label-tactical mb-0")
                                        ],
                                        className="d-flex align-items-center mb-1"
                                    ),
                                    dbc.Input(
                                        id='filter-search',
                                        type='text',
                                        placeholder='Taip nama stesen / sungai...',
                                        maxLength=60,
                                        style={"backgroundColor": "#080e1c", "borderColor": "#1e2d4a", "color": "#f8fafc", "borderRadius": "6px"}
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
                                        html.Div(
                                            [
                                                html.I(className="bi bi-geo-alt-fill text-danger me-2"),
                                                html.Span("PETA TABURAN STESEN TELEMETRI KRITIKAL", className="card-header-title")
                                            ],
                                            className="d-flex align-items-center"
                                        ),
                                        html.Div(
                                            [
                                                html.I(className="bi bi-hand-index-thumb text-info me-1"),
                                                html.Span("Klik penanda stesen pada peta untuk perincian", className="text-muted small d-none d-md-inline")
                                            ],
                                            className="d-flex align-items-center"
                                        )
                                    ],
                                    className="d-flex justify-content-between align-items-center"
                                ),
                                style={"backgroundColor": "#060a14", "borderColor": "#1e2d4a"}
                            ),
                            dbc.CardBody(
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id='map-chart',
                                            figure=create_map_chart(initial_df),
                                            style={"height": "580px"},
                                            config={"displayModeBar": False}
                                        )
                                    ],
                                    style={"position": "relative"}
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
                                    html.Div(
                                        [
                                            html.I(className="bi bi-speedometer2 text-warning me-2"),
                                            html.Span("STATUS AMBANG PARAS AIR STESEN TERPILIH", className="card-header-title")
                                        ],
                                        className="d-flex align-items-center"
                                    ),
                                    style={"backgroundColor": "#060a14", "borderColor": "#1e2d4a"}
                                ),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id='gauge-chart',
                                        figure=create_station_threshold_chart(initial_df),
                                        style={"height": "250px"},
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
                                    html.Div(
                                        [
                                            html.I(className="bi bi-graph-up-arrow text-danger me-2"),
                                            html.Span("TOP 10 STESEN MENGESAN PARAS KRITIKAL", className="card-header-title")
                                        ],
                                        className="d-flex align-items-center"
                                    ),
                                    style={"backgroundColor": "#060a14", "borderColor": "#1e2d4a"}
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
                                html.Div(
                                    [
                                        html.I(className="bi bi-cloud-rain-heavy-fill text-info me-2"),
                                        html.Span("INTENSITI HUJAN TERINGGI MENGIKUT NEGERI (HARI INI)", className="card-header-title")
                                    ],
                                    className="d-flex align-items-center"
                                ),
                                style={"backgroundColor": "#060a14", "borderColor": "#1e2d4a"}
                            ),
                            dbc.CardBody(
                                dcc.Graph(
                                    id='rainfall-chart',
                                    figure=create_rainfall_state_chart(initial_df),
                                    style={"height": "270px"},
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

        # vernment Footer
        html.Footer(
            dbc.Container(
                html.Div(
                    [
                        html.Div(
                            [
                                html.I(className="bi bi-shield-fill-check text-primary me-2"),
                                html.Span("PUSAT KAWALAN BENCANA NEGARA (NDCC) MALAYSIA © 2026", className="fw-bold")
                            ],
                            className="mb-1"
                        ),
                        html.Div(
                            [
                                html.Span("AGENSI PENGURUSAN BENCANA NEGARA (NADMA) & JABATAN PENGAIRAN DAN SALIRAN (JPS) | Sumber Data REST API: "),
                                html.A("api.data.gov.my/flood-warning", href="https://api.data.gov.my/flood-warning/", target="_blank", className="text-info text-decoration-none fw-semibold"),
                            ],
                            className="text-muted small"
                        )
                    ],
                    className="text-center py-4 border-top border-secondary opacity-85"
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


# Callback 4: Filter Data and Update Views (KPIs, Ticker, Map, Charts, Table)
@app.callback(
    [Output('alert-ticker-container', 'children'),
     Output('kpi-container', 'children'),
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

    # Apply Filters with Input Sanitization for Security
    if not filtered_df.empty:
        if state and state != 'ALL':
            filtered_df = filtered_df[filtered_df['state'] == state]
        
        if district and district != 'ALL':
            filtered_df = filtered_df[filtered_df['district'] == district]
            
        if status and status != 'ALL':
            filtered_df = filtered_df[filtered_df['water_level_indicator'] == status]
            
        if search and search.strip():
            clean_search = re.sub(r'[^\w\s\-\.\/]', '', search.strip()).lower()
            if clean_search:
                filtered_df = filtered_df[
                    filtered_df['station_name'].str.lower().str.contains(clean_search, na=False) |
                    filtered_df['station_code'].str.lower().str.contains(clean_search, na=False) |
                    filtered_df['district'].str.lower().str.contains(clean_search, na=False) |
                    filtered_df['sub_basin'].str.lower().str.contains(clean_search, na=False)
                ]

    # Generate Updated Components
    ticker_view = create_alert_ticker(filtered_df)
    kpi_view = create_kpi_cards(filtered_df)
    map_view = create_map_chart(filtered_df, selected_station_id=selected_station_id)
    gauge_view = create_station_threshold_chart(df if filtered_df.empty else filtered_df, station_id=selected_station_id)
    top_danger_view = create_top_danger_chart(filtered_df)
    rainfall_view = create_rainfall_state_chart(filtered_df)
    table_view = create_data_table(filtered_df)

    return ticker_view, kpi_view, map_view, gauge_view, top_danger_view, rainfall_view, table_view


if __name__ == '__main__':
    print("🚀 NADMA Malaysia Command Server starting on http://127.0.0.1:8050 ...")
    app.run_server(debug=True, host='0.0.0.0', port=8050)
