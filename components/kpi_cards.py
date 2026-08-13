from dash import html
import dash_bootstrap_components as dbc

def create_kpi_cards(df):
    if df.empty:
        total = danger = warning = alert = normal = 0
    else:
        total = len(df)
        danger = len(df[df['water_level_indicator'] == 'DANGER'])
        warning = len(df[df['water_level_indicator'] == 'WARNING'])
        alert = len(df[df['water_level_indicator'] == 'ALERT'])
        normal = len(df[df['water_level_indicator'] == 'NORMAL'])

    cards = [
        ("Jumlah Stesen", str(total), "Stesen Telemetri Aktif", "total", "#3b82f6"),
        ("Paras Bahaya", str(danger), "DANGER - Tindakan Segera", "danger", "#ef4444"),
        ("Paras Amaran", str(warning), "WARNING - Bersiap Sedia", "warning", "#f97316"),
        ("Paras Waspada", str(alert), "ALERT - Kawalan Dipantau", "alert", "#eab308"),
        ("Paras Normal", str(normal), "NORMAL - Dalam Kawalan", "normal", "#10b981"),
    ]

    cols = []
    for title, val, sub, card_type, color in cards:
        col = dbc.Col(
            html.Div(
                [
                    html.Div(title, className="metric-lbl"),
                    html.Div(val, className="metric-val", style={"color": color}),
                    html.Div(sub, className="metric-sub")
                ],
                className=f"metric-card {card_type} h-100"
            ),
            xs=12, sm=6, md=4, lg=2, className="mb-3 mb-lg-0"
        )
        cols.append(col)

    return dbc.Row(cols, className="g-3 mb-4 justify-content-center")
