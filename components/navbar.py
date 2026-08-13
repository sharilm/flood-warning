from dash import html
import dash_bootstrap_components as dbc

def create_navbar(last_updated_time=""):
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.Span("🌊 ", style={"fontSize": "1.8rem", "marginRight": "10px"}),
                                        html.Span(
                                            "Pusat Amaran Banjir Malaysia",
                                            style={
                                                "fontSize": "1.4rem",
                                                "fontWeight": "800",
                                                "color": "#f8fafc",
                                                "letterSpacing": "-0.02em"
                                            }
                                        ),
                                        html.Span(
                                            "LIVE",
                                            className="badge bg-danger ms-2 align-middle",
                                            style={"fontSize": "0.65rem", "padding": "4px 8px", "borderRadius": "6px"}
                                        )
                                    ],
                                    className="d-flex align-items-center"
                                ),
                                html.Div(
                                    "Sistem Pemantauan Stesen Telemetri & Paras Air Real-Time (data.gov.my)",
                                    style={"fontSize": "0.8rem", "color": "#94a3b8", "marginTop": "2px"}
                                )
                            ],
                            xs=12, md=7
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Span(className="pulse-badge me-2"),
                                                html.Span(
                                                    f"Kemaskini: {last_updated_time}",
                                                    id="live-timestamp",
                                                    style={"fontSize": "0.825rem", "color": "#cbd5e1", "fontWeight": "600"}
                                                )
                                            ],
                                            className="d-flex align-items-center mb-1 mb-md-0 me-3"
                                        ),
                                        dbc.Button(
                                            [
                                                html.I(className="bi bi-arrow-repeat me-1"),
                                                "Refresh Data"
                                            ],
                                            id="btn-refresh",
                                            color="primary",
                                            size="sm",
                                            outline=True,
                                            style={"borderRadius": "8px", "fontWeight": "600"}
                                        )
                                    ],
                                    className="d-flex align-items-center justify-content-md-end flex-wrap mt-2 mt-md-0"
                                )
                            ],
                            xs=12, md=5
                        )
                    ],
                    className="w-100 align-items-center g-2"
                )
            ],
            fluid=True
        ),
        color="#1e293b",
        dark=True,
        className="py-2 mb-4 border-bottom border-secondary shadow-sm"
    )
