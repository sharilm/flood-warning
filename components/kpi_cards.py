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

    def calc_pct(val):
        return f"{(val / total * 100):.1f}%" if total > 0 else "0%"

    cards = [
        (
            "JUMLAH STESEN", 
            str(total), 
            "Stesen Telemetri Aktif", 
            "total", 
            "#0284c7", 
            "bi-broadcast"
        ),
        (
            "PARAS BAHAYA", 
            str(danger), 
            f"{calc_pct(danger)} | Evakuasi / Tindakan Segera", 
            "danger", 
            "#ef4444", 
            "bi-exclamation-triangle-fill"
        ),
        (
            "PARAS AMARAN", 
            str(warning), 
            f"{calc_pct(warning)} | Bersiap Sedia Operasi", 
            "warning", 
            "#f97316", 
            "bi-exclamation-circle-fill"
        ),
        (
            "PARAS WASPADA", 
            str(alert), 
            f"{calc_pct(alert)} | Dipantau Rapi 24/7", 
            "alert", 
            "#eab308", 
            "bi-bell-fill"
        ),
        (
            "PARAS NORMAL", 
            str(normal), 
            f"{calc_pct(normal)} | Lingkungan Selamat", 
            "normal", 
            "#10b981", 
            "bi-shield-check"
        ),
    ]

    cols = []
    for title, val, sub, card_type, color, icon_cls in cards:
        col = dbc.Col(
            html.Div(
                [
                    html.Div(
                        [
                            html.I(className=f"bi {icon_cls} me-1", style={"color": color}),
                            html.Span(title)
                        ],
                        className="metric-lbl d-flex align-items-center"
                    ),
                    html.Div(val, className="metric-val my-1", style={"color": color}),
                    html.Div(
                        [
                            html.I(className="bi bi-activity text-muted me-1", style={"fontSize": "0.7rem"}),
                            html.Span(sub)
                        ],
                        className="metric-sub"
                    )
                ],
                className=f"metric-card {card_type} h-100"
            ),
            xs=12, sm=6, md=4, lg=2, className="mb-3 mb-lg-0"
        )
        cols.append(col)

    return dbc.Row(cols, className="g-3 mb-4 justify-content-center")
