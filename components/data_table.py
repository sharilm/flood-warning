from dash import dash_table, html
import dash_bootstrap_components as dbc

def create_data_table(df):
    if df.empty:
        display_df_records = []
    else:
        # Prepare display columns
        display_df = df[[
            'station_id', 'station_name', 'station_code', 'district', 'state',
            'water_level_indicator', 'water_level_current', 
            'water_level_normal_level', 'water_level_alert_level', 'water_level_warning_level', 'water_level_danger_level',
            'rainfall_latest_1hr', 'rainfall_total_today', 'water_level_update_datetime'
        ]].copy()
        
        display_df_records = display_df.to_dict('records')

    columns = [
        {"name": "Status", "id": "water_level_indicator"},
        {"name": "Nama Stesen", "id": "station_name"},
        {"name": "Kod", "id": "station_code"},
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
            'backgroundColor': '#0f172a',
            'color': '#94a3b8',
            'fontWeight': 'bold',
            'fontSize': '0.78rem',
            'textTransform': 'uppercase',
            'borderBottom': '2px solid #334155',
            'padding': '10px'
        },
        style_cell={
            'backgroundColor': '#1e293b',
            'color': '#f8fafc',
            'borderBottom': '1px solid #334155',
            'borderLeft': 'none',
            'borderRight': 'none',
            'fontSize': '0.83rem',
            'fontFamily': 'Plus Jakarta Sans, sans-serif',
            'padding': '8px 12px',
            'textAlign': 'left'
        },
        style_data_conditional=style_data_conditional
    )

    return html.Div(
        [
            html.Div(
                [
                    html.Span("📋 Senarai Penuh Stesen Telemetri", className="card-header-title me-2"),
                    html.Span(" (Gunakan carian/susunan pada tajuk kolum)", style={"fontSize": "0.75rem", "color": "#94a3b8"})
                ],
                className="mb-3"
            ),
            table
        ]
    )
