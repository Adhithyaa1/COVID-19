"""Wire layouts and callbacks for the COVID-19 analytics dashboard."""

from dash import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from webapp import app
import csidepanel
import ctab1
import ctab2
import ctab3
import ctab4
import ctab5
import ctransforms

app.layout = csidepanel.layout

FILTER_INPUTS = [
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
    Input("location", "value"),
    Input("continent", "value"),
]

OPERATORS = [
    ["ge ", ">="],
    ["le ", "<="],
    ["lt ", "<"],
    ["gt ", ">"],
    ["ne ", "!="],
    ["eq ", "="],
    ["contains "],
    ["datestartswith "],
]


def _fmt(n: float) -> str:
    if abs(n) >= 1_000_000:
        return f"{n / 1_000_000:,.2f}M"
    if abs(n) >= 1_000:
        return f"{n / 1_000:,.1f}K"
    return f"{n:,.0f}"


def split_filter_part(filter_part: str):
    for operator_type in OPERATORS:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find("{") + 1 : name_part.rfind("}")]
                value_part = value_part.strip()
                if not value_part:
                    return [None] * 3
                v0 = value_part[0]
                if v0 == value_part[-1] and v0 in ("'", '"', "`"):
                    value = value_part[1:-1].replace("\\" + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part
                return name, operator_type[0].strip(), value
    return [None] * 3


def apply_table_query(dff: pd.DataFrame, filter_query: str) -> pd.DataFrame:
    if not filter_query:
        return dff
    for filter_part in filter_query.split(" && "):
        col_name, operator, filter_value = split_filter_part(filter_part)
        if col_name is None or col_name not in dff.columns:
            continue
        if operator in ("eq", "ne", "lt", "le", "gt", "ge"):
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == "contains":
            dff = dff.loc[dff[col_name].astype(str).str.contains(str(filter_value), na=False)]
        elif operator == "datestartswith":
            dff = dff.loc[dff[col_name].astype(str).str.startswith(str(filter_value))]
    return dff


@app.callback(Output("tabs-content", "children"), Input("tabs", "value"))
def render_content(tab):
    return {
        "tab-1": ctab1.layout,
        "tab-2": ctab2.layout,
        "tab-3": ctab3.layout,
        "tab-4": ctab4.layout,
        "tab-5": ctab5.layout,
    }.get(tab, ctab1.layout)


@app.callback(
    Output("kpi-countries", "children"),
    Output("kpi-new-cases", "children"),
    Output("kpi-new-deaths", "children"),
    Output("kpi-latest-cases", "children"),
    Output("kpi-latest-deaths", "children"),
    *FILTER_INPUTS,
)
def update_kpis(start_date, end_date, location, continent):
    dff = ctransforms.filter_df(start_date, end_date, location, continent)
    k = ctransforms.period_kpis(dff)
    return (
        str(k["countries"]),
        _fmt(k["new_cases"]),
        _fmt(k["new_deaths"]),
        _fmt(k["latest_cases"]),
        _fmt(k["latest_deaths"]),
    )


@app.callback(
    Output("table-sorting-filtering", "data"),
    Input("table-sorting-filtering", "page_current"),
    Input("table-sorting-filtering", "page_size"),
    Input("table-sorting-filtering", "sort_by"),
    Input("table-sorting-filtering", "filter_query"),
    *FILTER_INPUTS,
)
def update_table(page_current, page_size, sort_by, filter_query, start_date, end_date, location, continent):
    dff = ctransforms.filter_df(start_date, end_date, location, continent)
    cols = [c for c in ctransforms.TABLE_COLUMNS if c in dff.columns]
    dff = dff[cols].copy()
    dff["date"] = dff["date"].dt.strftime("%Y-%m-%d")
    dff = apply_table_query(dff, filter_query or "")

    if sort_by:
        dff = dff.sort_values(
            [c["column_id"] for c in sort_by],
            ascending=[c["direction"] == "asc" for c in sort_by],
        )

    page_current = page_current or 0
    page_size = page_size or 50
    return dff.iloc[page_current * page_size : (page_current + 1) * page_size].to_dict("records")


@app.callback(
    Output("curves-graph", "figure"),
    Input("curves-metric", "value"),
    Input("curves-scale", "value"),
    *FILTER_INPUTS,
)
def update_curves(metric, scale, start_date, end_date, location, continent):
    dff = ctransforms.filter_df(start_date, end_date, location, continent)
    empty = go.Figure()
    empty.update_layout(title="No data for current filters", template="plotly_white")
    if dff.empty or metric not in dff.columns:
        return empty

    locs = location if isinstance(location, list) else [location]
    if not locs or "All" in locs:
        keep = ctransforms.top_locations_by_cases(dff, n=8)
        dff = dff[dff["location"].isin(keep)]
        subtitle = "Top 8 countries by latest cumulative cases"
    else:
        if len(locs) > 12:
            keep = ctransforms.top_locations_by_cases(dff[dff["location"].isin(locs)], n=12)
            dff = dff[dff["location"].isin(keep)]
            subtitle = "Showing 12 of selected countries (by latest cases)"
        else:
            subtitle = "Selected countries"

    fig = px.line(
        dff,
        x="date",
        y=metric,
        color="location",
        labels={"date": "Date", metric: metric.replace("_", " ").title(), "location": "Country"},
        title=f"Epidemic curves — {metric.replace('_', ' ')}",
    )
    fig.update_layout(
        template="plotly_white",
        yaxis_type=scale,
        legend_title_text="Country",
        hovermode="x unified",
        margin=dict(t=60),
        annotations=[
            dict(
                text=subtitle,
                xref="paper",
                yref="paper",
                x=0,
                y=1.08,
                showarrow=False,
                font=dict(size=12, color="#666"),
            )
        ],
    )
    return fig


@app.callback(
    Output("rank-graph", "figure"),
    Input("rank-metric", "value"),
    Input("rank-top-n", "value"),
    *FILTER_INPUTS,
)
def update_rankings(metric, top_n, start_date, end_date, location, continent):
    dff = ctransforms.filter_df(start_date, end_date, location, continent)
    snap = ctransforms.country_snapshot(dff)
    empty = go.Figure()
    empty.update_layout(title="No data for current filters", template="plotly_white")
    if snap.empty or metric not in snap.columns:
        return empty

    plot_df = snap.dropna(subset=[metric]).nlargest(int(top_n or 20), metric)
    fig = px.bar(
        plot_df.sort_values(metric),
        x=metric,
        y="location",
        color="continent",
        orientation="h",
        labels={metric: metric.replace("_", " ").title(), "location": "Country"},
        title=f"Top countries by {metric.replace('_', ' ')}",
        hover_data={
            "total_cases": ":,.0f",
            "total_deaths": ":,.0f",
            "peak_cases_date": True,
            "cfr": ":.3f",
        },
    )
    fig.update_layout(template="plotly_white", height=620, margin=dict(l=120, t=50), yaxis_title="")
    return fig


@app.callback(
    Output("policy-dual-axis", "figure"),
    Output("policy-rt", "figure"),
    Output("policy-scatter", "figure"),
    Input("policy-country", "value"),
    Input("policy-lag", "value"),
    *FILTER_INPUTS,
)
def update_policy(policy_country, lag, start_date, end_date, location, continent):
    dff = ctransforms.filter_df(start_date, end_date, location, continent)
    empty = go.Figure()
    empty.update_layout(template="plotly_white", title="No data")

    country = dff[dff["location"] == policy_country].sort_values("date")
    if country.empty:
        country = ctransforms.filter_df(start_date, end_date, [policy_country], None).sort_values("date")

    # Dual axis: stringency vs lagged smoothed cases
    dual = make_subplots(specs=[[{"secondary_y": True}]])
    if not country.empty:
        c = country.copy()
        lag = int(lag or 0)
        c["cases_lagged"] = c["new_cases_smoothed"].shift(-lag) if lag else c["new_cases_smoothed"]
        dual.add_trace(
            go.Scatter(x=c["date"], y=c["stringency_index"], name="Stringency", line=dict(color="#2c7bb6")),
            secondary_y=False,
        )
        dual.add_trace(
            go.Scatter(
                x=c["date"],
                y=c["cases_lagged"],
                name=f"Smoothed cases (lag {lag}d)",
                line=dict(color="#d7191c"),
            ),
            secondary_y=True,
        )
        dual.update_layout(
            title=f"{policy_country}: stringency vs smoothed cases",
            template="plotly_white",
            legend=dict(orientation="h", y=1.12),
            margin=dict(t=70),
        )
        dual.update_yaxes(title_text="Stringency index", secondary_y=False)
        dual.update_yaxes(title_text="New cases (smoothed)", secondary_y=True)
    else:
        dual = empty

    # R(t)
    rt = go.Figure()
    if not country.empty and country["reproduction_rate"].notna().any():
        rt.add_trace(
            go.Scatter(
                x=country["date"],
                y=country["reproduction_rate"],
                mode="lines",
                name="R(t)",
                line=dict(color="#7b3294"),
            )
        )
        rt.add_hline(y=1.0, line_dash="dash", line_color="gray", annotation_text="R = 1")
        rt.update_layout(
            title=f"{policy_country}: reproduction rate R(t)",
            template="plotly_white",
            yaxis_title="R(t)",
            margin=dict(t=50),
        )
    else:
        rt.update_layout(title="R(t) unavailable for selection", template="plotly_white")

    # Cross-country scatter
    snap = ctransforms.country_snapshot(dff)
    if snap.empty:
        scatter = empty
    else:
        means = (
            dff.groupby("location", as_index=False)["stringency_index"]
            .mean()
            .rename(columns={"stringency_index": "mean_stringency"})
        )
        plot_df = snap.merge(means, on="location", how="left").dropna(
            subset=["mean_stringency", "total_deaths_per_million"]
        )
        scatter = px.scatter(
            plot_df,
            x="mean_stringency",
            y="total_deaths_per_million",
            color="continent",
            hover_name="location",
            size="population",
            size_max=40,
            labels={
                "mean_stringency": "Mean stringency (in range)",
                "total_deaths_per_million": "Deaths per million (latest)",
            },
            title="Mean stringency vs deaths per million",
        )
        scatter.update_layout(template="plotly_white", margin=dict(t=50))

    return dual, rt, scatter


@app.callback(
    Output("socio-scatter", "figure"),
    Output("socio-corr", "children"),
    Input("socio-x", "value"),
    Input("socio-y", "value"),
    Input("socio-color", "value"),
    *FILTER_INPUTS,
)
def update_socio(x_col, y_col, color_by, start_date, end_date, location, continent):
    dff = ctransforms.filter_df(start_date, end_date, location, continent)
    snap = ctransforms.country_snapshot(dff)
    empty = go.Figure()
    empty.update_layout(title="No data for current filters", template="plotly_white")

    if snap.empty or x_col not in snap.columns or y_col not in snap.columns:
        return empty, ""

    plot_df = snap.dropna(subset=[x_col, y_col]).copy()
    if plot_df.empty:
        return empty, "Insufficient non-null data for the selected axes."

    color = color_by if color_by != "none" else None
    fig = px.scatter(
        plot_df,
        x=x_col,
        y=y_col,
        color=color,
        hover_name="location",
        size="population",
        size_max=42,
        labels={
            x_col: x_col.replace("_", " ").title(),
            y_col: y_col.replace("_", " ").title(),
        },
        title="Socioeconomic attributes vs COVID outcomes",
    )
    corr = plot_df[x_col].corr(plot_df[y_col])
    n = len(plot_df)
    note = (
        f"Pearson r = {corr:.3f} across {n} countries with non-null values "
        f"(observational; reporting bias and testing capacity are confounders)."
    )
    fig.update_layout(template="plotly_white", height=560, margin=dict(t=50))
    return fig, note


if __name__ == "__main__":
    app.run_server(debug=True)
