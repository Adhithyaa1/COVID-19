"""Tab 5 — socioeconomic / demographic correlates of COVID outcomes."""

from dash import dcc, html
import dash_bootstrap_components as dbc

import ctransforms

X_OPTIONS = [
    {"label": "GDP per capita", "value": "gdp_per_capita"},
    {"label": "Human Development Index", "value": "human_development_index"},
    {"label": "Median age", "value": "median_age"},
    {"label": "% aged 65+", "value": "aged_65_older"},
    {"label": "Hospital beds / 1,000", "value": "hospital_beds_per_thousand"},
    {"label": "Population density", "value": "population_density"},
    {"label": "Life expectancy", "value": "life_expectancy"},
    {"label": "Diabetes prevalence", "value": "diabetes_prevalence"},
    {"label": "Cardiovasc. death rate", "value": "cardiovasc_death_rate"},
]

Y_OPTIONS = [
    {"label": "Deaths per million (latest)", "value": "total_deaths_per_million"},
    {"label": "Cases per million (latest)", "value": "total_cases_per_million"},
    {"label": "Case fatality ratio", "value": "cfr"},
    {"label": "Period new deaths", "value": "period_new_deaths"},
]

layout = html.Div(
    [
        html.P(
            "Country-level snapshot at the end of the selected window. "
            "Use this to probe whether demographic and development indicators co-vary with "
            "reported COVID burden. Observational only — reporting capacity confounds many relationships.",
            className="text-muted",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("X axis (country attribute)"),
                        dcc.Dropdown(
                            id="socio-x",
                            options=X_OPTIONS,
                            value="human_development_index",
                            clearable=False,
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.Label("Y axis (COVID outcome)"),
                        dcc.Dropdown(
                            id="socio-y",
                            options=Y_OPTIONS,
                            value="total_deaths_per_million",
                            clearable=False,
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.Label("Color by"),
                        dcc.Dropdown(
                            id="socio-color",
                            options=[
                                {"label": "Continent", "value": "continent"},
                                {"label": "None", "value": "none"},
                            ],
                            value="continent",
                            clearable=False,
                        ),
                    ],
                    width=4,
                ),
            ],
            className="mb-3",
        ),
        dcc.Graph(id="socio-scatter", style={"height": "560px"}),
        html.Div(id="socio-corr", className="mt-2 text-muted"),
        html.P(
            f"Static attributes are repeated daily in the source panel "
            f"({len(ctransforms.STATIC_COLS)} fields). Snapshot uses the latest row per country.",
            className="small text-muted mt-3",
        ),
    ]
)
