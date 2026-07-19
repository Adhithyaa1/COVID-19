"""Tab 3 — country rankings with correct aggregations."""

from dash import dcc, html
import dash_bootstrap_components as dbc

layout = html.Div(
    [
        html.P(
            "Cross-country comparison using the last observation in the selected date range "
            "(not a sum of cumulative totals). Case fatality uses total_deaths / total_cases.",
            className="text-muted",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Rank by"),
                        dcc.Dropdown(
                            id="rank-metric",
                            options=[
                                {"label": "Total cases (latest)", "value": "total_cases"},
                                {"label": "Total deaths (latest)", "value": "total_deaths"},
                                {
                                    "label": "Cases per million (latest)",
                                    "value": "total_cases_per_million",
                                },
                                {
                                    "label": "Deaths per million (latest)",
                                    "value": "total_deaths_per_million",
                                },
                                {"label": "Case fatality ratio (CFR)", "value": "cfr"},
                                {
                                    "label": "Peak smoothed daily cases (in range)",
                                    "value": "peak_new_cases",
                                },
                                {
                                    "label": "New cases in period",
                                    "value": "period_new_cases",
                                },
                                {
                                    "label": "New deaths in period",
                                    "value": "period_new_deaths",
                                },
                            ],
                            value="total_deaths_per_million",
                            clearable=False,
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Label("Show top N"),
                        dcc.Slider(
                            id="rank-top-n",
                            min=5,
                            max=40,
                            step=5,
                            value=20,
                            marks={5: "5", 10: "10", 20: "20", 30: "30", 40: "40"},
                        ),
                    ],
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dcc.Graph(id="rank-graph", style={"height": "620px"}),
    ]
)
