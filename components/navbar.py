from dash import html
import dash_bootstrap_components as dbc
import urllib.parse

def create_malaysia_flag_img():
    """Return crisp SVG image for Jalur Gemilang (Malaysian Flag)."""
    svg_raw = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="14" viewBox="0 0 28 14">'
        '<rect width="28" height="14" fill="#cc0000"/>'
        '<rect y="1" width="28" height="1" fill="#ffffff"/>'
        '<rect y="3" width="28" height="1" fill="#ffffff"/>'
        '<rect y="5" width="28" height="1" fill="#ffffff"/>'
        '<rect y="7" width="28" height="1" fill="#ffffff"/>'
        '<rect y="9" width="28" height="1" fill="#ffffff"/>'
        '<rect y="11" width="28" height="1" fill="#ffffff"/>'
        '<rect y="13" width="28" height="1" fill="#ffffff"/>'
        '<rect width="14" height="8" fill="#000066"/>'
        '<circle cx="6.5" cy="4" r="2.5" fill="#ffcc00"/>'
        '<circle cx="7.3" cy="4" r="2.1" fill="#000066"/>'
        '<polygon points="8.8,4 9.5,4.6 9.2,3.7 9.9,3.1 9.0,3.1 8.8,2.2 8.5,3.1 7.6,3.1 8.3,3.7 8.0,4.6" fill="#ffcc00"/>'
        '</svg>'
    )
    encoded_svg = urllib.parse.quote(svg_raw)
    data_uri = f"data:image/svg+xml;charset=utf-8,{encoded_svg}"

    return html.Img(
        src=data_uri,
        width=34,
        height=22,
        alt="Malaysia Flag Jalur Gemilang",
        style={"borderRadius": "3px", "boxShadow": "0 1px 4px rgba(0,0,0,0.4)", "border": "1px solid #334155"}
    )

def create_navbar(last_updated_time=""):
    return html.Div(
        [
            # NADMA Government Top Banner
            html.Div(
                dbc.Container(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                create_malaysia_flag_img(),
                                                html.Span("MALAYSIA DISASTER MANAGEMENT TELEMETRY", className="fw-bold text-light ms-2", style={"fontSize": "0.725rem"})
                                            ],
                                            className="flag-malaysia-badge me-2"
                                        ),
                                        html.Span(
                                            [
                                                html.I(className="bi bi-shield-check text-success me-1"),
                                                "JABATAN PERDANA MENTERI | REST API RASMI (data.gov.my)"
                                            ],
                                            className="security-tag nadma"
                                        ),
                                    ],
                                    className="d-flex align-items-center flex-wrap gap-2"
                                ),
                                xs=12, md=7
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Span(
                                            [
                                                html.I(className="bi bi-activity text-warning me-1"),
                                                "MOD OPERASI: BILIK GERAKAN AKTIF 24/7"
                                            ],
                                            className="security-tag gold"
                                        ),
                                    ],
                                    className="d-flex align-items-center justify-content-md-end mt-1 mt-md-0"
                                ),
                                xs=12, md=5
                            )
                        ],
                        className="align-items-center g-1"
                    ),
                    fluid=True
                ),
                className="security-banner mb-2"
            ),

            # Main NADMA Command Center Header Bar
            dbc.Navbar(
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                # Title Section
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="bi bi-shield-fill-check text-primary fs-2 me-3 align-middle",
                                                        style={"color": "#0284c7"}
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Span(
                                                                        "PUSAT KAWALAN BENCANA NEGARA (NDCC)",
                                                                        style={
                                                                            "fontSize": "1.25rem",
                                                                            "fontWeight": "800",
                                                                            "color": "#f8fafc",
                                                                            "letterSpacing": "0.02em"
                                                                        }
                                                                    ),
                                                                    html.Span(
                                                                        [
                                                                            html.Span(className="led-indicator led-green me-1 align-middle"),
                                                                            "TELEMETRI LIVE"
                                                                        ],
                                                                        className="badge-tactical badge-normal-tactical ms-2 align-middle"
                                                                    )
                                                                ],
                                                                className="d-flex align-items-center flex-wrap"
                                                            ),
                                                            html.Div(
                                                                "AGENSI PENGURUSAN BENCANA NEGARA (NADMA) | JABATAN PENGAIRAN DAN SALIRAN (JPS)",
                                                                style={"fontSize": "0.78rem", "color": "#94a3b8", "marginTop": "2px"}
                                                            )
                                                        ]
                                                    )
                                                ],
                                                className="d-flex align-items-center"
                                            )
                                        ]
                                    ),
                                    xs=12, lg=7
                                ),
                                # Actions & Timestamp Section
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Span("Kemaskini Telemetri:", className="text-muted small me-1 d-none d-sm-inline"),
                                                            html.Span(
                                                                f"{last_updated_time if last_updated_time else 'LIVE'}",
                                                                id="live-timestamp",
                                                                className="font-mono",
                                                                style={"fontSize": "0.85rem", "color": "#38bdf8", "fontWeight": "600"}
                                                            )
                                                        ],
                                                        className="d-flex align-items-center me-3"
                                                    ),
                                                    dbc.Button(
                                                        [
                                                            html.I(className="bi bi-arrow-repeat me-1"),
                                                            "Kemaskini Data"
                                                        ],
                                                        id="btn-refresh",
                                                        color="primary",
                                                        size="sm",
                                                        className="fw-bold",
                                                        style={"borderRadius": "6px", "fontSize": "0.8rem", "backgroundColor": "#0284c7", "borderColor": "#0284c7"}
                                                    )
                                                ],
                                                className="d-flex align-items-center justify-content-lg-end flex-wrap gap-2 mt-2 mt-lg-0"
                                            )
                                        ]
                                    ),
                                    xs=12, lg=5
                                )
                            ],
                            className="w-100 align-items-center g-2"
                        )
                    ],
                    fluid=True
                ),
                color="#0f172a",
                dark=True,
                className="py-2 border-bottom border-secondary shadow-sm"
            )
        ],
        className="mb-3"
    )
