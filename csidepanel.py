"""App shell: sidebar filters + tabbed analytics workspace."""

from dash import dcc, html
import dash_bootstrap_components as dbc

import ctransforms

location_options = [{"label": "All countries", "value": "All"}] + [
    {"label": loc, "value": loc} for loc in ctransforms.LOCATIONS
]
continent_options = [{"label": "All continents", "value": "All"}] + [
    {"label": c, "value": c} for c in ctransforms.CONTINENTS
]


def _kpi_card(title: str, kpi_id: str) -> html.Div:
    return html.Div(
        [
            html.Div(title, className="text-muted small"),
            html.H4(id=kpi_id, className="mb-0 mt-1"),
        ],
        className="border rounded p-2 mb-2 bg-light",
    )


layout = dbc.Container(
    [
        html.H2("COVID-19 Analytics Lab", className="text-center my-3"),
        html.P(
            "Exploratory analysis of early-pandemic outcomes (Jan 2020 – Jan 2021). "
            "Filters apply across all tabs.",
            className="text-center text-muted mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Filters"),
                        html.Label("Date range", className="fw-semibold mt-2"),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=ctransforms.DATE_MIN,
                            max_date_allowed=ctransforms.DATE_MAX,
                            start_date=ctransforms.DATE_MIN,
                            end_date=ctransforms.DATE_MAX,
                            display_format="YYYY-MM-DD",
                            className="mb-2",
                        ),
                        html.Label("Continent", className="fw-semibold mt-3"),
                        dcc.Dropdown(
                            id="continent",
                            options=continent_options,
                            value="All",
                            clearable=False,
                            className="mb-2",
                        ),
                        html.Label("Country", className="fw-semibold mt-2"),
                        dcc.Dropdown(
                            id="location",
                            options=location_options,
                            value=["All"],
                            multi=True,
                            className="mb-3",
                        ),
                        html.Hr(),
                        html.H6("Period KPIs"),
                        html.P(
                            "New cases/deaths = sum of daily new_*. "
                            "Latest totals = last cumulative observation per country in range.",
                            className="small text-muted",
                        ),
                        _kpi_card("Countries in view", "kpi-countries"),
                        _kpi_card("New cases (period)", "kpi-new-cases"),
                        _kpi_card("New deaths (period)", "kpi-new-deaths"),
                        _kpi_card("Latest cumulative cases", "kpi-latest-cases"),
                        _kpi_card("Latest cumulative deaths", "kpi-latest-deaths"),
                    ],
                    width=3,
                    className="pe-3",
                ),
                dbc.Col(
                    [
                        dcc.Tabs(
                            id="tabs",
                            value="tab-1",
                            children=[
                                dcc.Tab(label="Data Explorer", value="tab-1"),
                                dcc.Tab(label="Epidemic Curves", value="tab-2"),
                                dcc.Tab(label="Country Rankings", value="tab-3"),
                                dcc.Tab(label="Policy & Transmission", value="tab-4"),
                                dcc.Tab(label="Socioeconomic Lens", value="tab-5"),
                            ],
                        ),
                        html.Div(id="tabs-content", className="mt-3"),
                    ],
                    width=9,
                ),
            ]
        ),
    ],
    fluid=True,
)
