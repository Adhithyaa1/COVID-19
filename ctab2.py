"""Tab 2 — epidemic curves (smoothed incidence by country)."""

from dash import dcc, html
import dash_bootstrap_components as dbc

layout = html.Div(
    [
        html.P(
            "7-day smoothed new cases/deaths over time. "
            "When many countries are selected, the chart shows the top 8 by latest cumulative cases.",
            className="text-muted",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Metric"),
                        dcc.Dropdown(
                            id="curves-metric",
                            options=[
                                {"label": "New cases (smoothed)", "value": "new_cases_smoothed"},
                                {"label": "New deaths (smoothed)", "value": "new_deaths_smoothed"},
                                {
                                    "label": "New cases per million (smoothed)",
                                    "value": "new_cases_smoothed_per_million",
                                },
                                {
                                    "label": "New deaths per million (smoothed)",
                                    "value": "new_deaths_smoothed_per_million",
                                },
                            ],
                            value="new_cases_smoothed",
                            clearable=False,
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Label("Scale"),
                        dcc.RadioItems(
                            id="curves-scale",
                            options=[
                                {"label": " Linear", "value": "linear"},
                                {"label": " Log", "value": "log"},
                            ],
                            value="linear",
                            inline=True,
                        ),
                    ],
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dcc.Graph(id="curves-graph", style={"height": "620px"}),
    ]
)
