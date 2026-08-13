from dash import dash_table, html
import dash_bootstrap_components as dbc

def create_data_table(df):
    if df.empty:
        display_df_records = []
    else:
        display_df = df[[
            'station_id', 'station_name', 'station_code', 'district', 'state',
            'water_level_indicator', 'water_level_current', 
            'water_level_normal_level', 'water_level_alert_level', 'water_level_warning_level', 'water_level_danger_level',
            'rainfall_latest_1hr', 'rainfall_total_today', 'water_level_update_datetime'
        ]].copy()
        
        display_df_records = display_df.to_dict('records')

    columns = [
        {"name": "Status", "id": "water_level_indicator"},
        {"name": "Nama Stesen Telemetri", "id": "station_name"},
        {"name": "Kod Stesen", "id": "station_code"},
        {"name": "Daerah", "id": "district"},
        {"name": "Negeri", "id": "state"},
        {"name": "Paras Semasa (m)", "id": "water_level_current", "type": "numeric", "format": {"specifier": ".2f"}},
        {"name": "Normal (m)", "id": "water_level_normal_level", "type": "numeric", "format": {"specifier": ".2f"}},
        {"name": "Waspada (m)", "id": "water_level_alert_level", "type": "numeric", "format": {"specifier": ".2f"}},
        {"name": "Amaran (m)", "id": "water_level_warning_level", "type": "numeric", "format": {"specifier": ".2f"}},
        {"name": "Bahaya (m)", "id": "water_level_danger_level", "type": "numeric", "format": {"specifier": ".2f"}},
        {"name": "Hujan 1j (mm)", "id": "rainfall_latest_1hr", "type": "numeric", "format": {"specifier": ".1f"}},
        {"name": "Hujan Hari Ini (mm)", "id": "rainfall_total_today", "type": "numeric", "format": {"specifier": ".1f"}},
        {"name": "Kemaskini", "id": "water_level_update_datetime"}
    ]

    style_data_conditional = [
        {
            'if': {'filter_query': '{water_level_indicator} = "DANGER"'},
            'backgroundColor': 'rgba(239, 68, 68, 0.2)',
            'color': '#fca5a5',
            'fontWeight': 'bold'
        },
        {
            'if': {'filter_query': '{water_level_indicator} = "WARNING"'},
            'backgroundColor': 'rgba(249, 115, 22, 0.2)',
            'color': '#fdba74',
            'fontWeight': 'bold'
        },
        {
            'if': {'filter_query': '{water_level_indicator} = "ALERT"'},
            'backgroundColor': 'rgba(234, 179, 8, 0.2)',
            'color': '#fde047',
            'fontWeight': 'bold'
        },
        {
            'if': {'filter_query': '{water_level_indicator} = "NORMAL"'},
            'backgroundColor': 'rgba(16, 185, 129, 0.1)',
            'color': '#6ee7b7'
        },
        {
            'if': {'column_id': 'station_code'},
            'fontFamily': 'Roboto Mono, monospace',
            'color': '#38bdf8'
        },
        {
            'if': {'column_id': 'water_level_current'},
            'fontFamily': 'Roboto Mono, monospace',
            'fontWeight': 'bold'
        },
        {
            'if': {'column_id': 'water_level_danger_level'},
            'fontFamily': 'Roboto Mono, monospace',
            'color': '#fca5a5'
        },
        {
            'if': {'column_id': 'water_level_update_datetime'},
            'fontFamily': 'Roboto Mono, monospace',
            'color': '#94a3b8',
            'fontSize': '0.78rem'
        }
    ]

    table = dash_table.DataTable(
        id='flood-data-table',
        columns=columns,
        data=display_df_records,
        page_size=12,
        page_action='native',
        sort_action='native',
        filter_action='native',
        export_format='csv',
        export_headers='display',
        style_table={'overflowX': 'auto', 'minWidth': '100%'},
        style_header={
            'backgroundColor': '#060a14',
            'color': '#94a3b8',
            'fontFamily': 'Plus Jakarta Sans, sans-serif',
            'fontWeight': '700',
            'fontSize': '0.75rem',
            'textTransform': 'uppercase',
            'letterSpacing': '0.04em',
            'borderBottom': '2px solid #1e2d4a',
            'padding': '10px 12px'
        },
        style_cell={
            'backgroundColor': '#131d33',
            'color': '#f8fafc',
            'borderBottom': '1px solid #1e2d4a',
            'borderLeft': 'none',
            'borderRight': 'none',
            'fontSize': '0.825rem',
            'fontFamily': 'Plus Jakarta Sans, sans-serif',
            'padding': '9px 12px',
            'textAlign': 'left'
        },
        style_data_conditional=style_data_conditional
    )

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.I(className="bi bi-table me-2 text-primary"),
                            html.Span("MATRIKS & REKOD AUDIT TELEMETRI STESEN", className="card-header-title")
                        ],
                        className="d-flex align-items-center"
                    ),
                    html.Div(
                        [
                            html.I(className="bi bi-shield-check text-success me-1"),
                            html.Span("Integriti Rekod Terpelihara (Gunakan carian/susunan pada tajuk kolum)", style={"fontSize": "0.75rem", "color": "#94a3b8"})
                        ],
                        className="d-flex align-items-center"
                    )
                ],
                className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3"
            ),
            table
        ]
    )
