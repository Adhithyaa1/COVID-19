"""Tab 4 — policy stringency vs outcomes and reproduction rate."""

from dash import dcc, html
import dash_bootstrap_components as dbc

import ctransforms

layout = html.Div(
    [
        html.P(
            "Explore how policy stringency and estimated R(t) relate to epidemic intensity. "
            "Lag shifts cases forward relative to stringency (days). Correlation ≠ causation — "
            "stringency often rises after outbreaks intensify.",
            className="text-muted",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Focus country (for dual-axis & R(t))"),
                        dcc.Dropdown(
                            id="policy-country",
                            options=[{"label": loc, "value": loc} for loc in ctransforms.LOCATIONS],
                            value="United States",
                            clearable=False,
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Label("Stringency → cases lag (days)"),
                        dcc.Slider(
                            id="policy-lag",
                            min=0,
                            max=28,
                            step=7,
                            value=14,
                            marks={0: "0", 7: "7", 14: "14", 21: "21", 28: "28"},
                        ),
                    ],
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="policy-dual-axis", style={"height": "420px"}), width=6),
                dbc.Col(dcc.Graph(id="policy-rt", style={"height": "420px"}), width=6),
            ]
        ),
        html.Hr(),
        html.H6("Cross-country: mean stringency vs period mortality"),
        html.P(
            "Each point is a country. Mean stringency in the date range vs deaths per million "
            "(latest in range). Sparse stringency coverage for some countries.",
            className="small text-muted",
        ),
        dcc.Graph(id="policy-scatter", style={"height": "480px"}),
    ]
)
