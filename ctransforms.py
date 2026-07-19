"""Data loading and shared transforms for the COVID-19 analytics dashboard."""

from pathlib import Path

import pandas as pd

_DATA_PATH = Path(__file__).resolve().parent / "covidmaster2.csv"

_DROP_COLS = {"Unnamed: 54", "year", "month", "day"}

TABLE_COLUMNS = [
    "date",
    "location",
    "continent",
    "new_cases",
    "new_cases_smoothed",
    "total_cases",
    "new_deaths",
    "new_deaths_smoothed",
    "total_deaths",
    "total_cases_per_million",
    "total_deaths_per_million",
    "reproduction_rate",
    "stringency_index",
    "positive_rate",
    "population",
]

STATIC_COLS = [
    "location",
    "continent",
    "population",
    "population_density",
    "median_age",
    "aged_65_older",
    "aged_70_older",
    "gdp_per_capita",
    "extreme_poverty",
    "cardiovasc_death_rate",
    "diabetes_prevalence",
    "hospital_beds_per_thousand",
    "life_expectancy",
    "human_development_index",
]


def _load() -> pd.DataFrame:
    raw = pd.read_csv(_DATA_PATH)
    raw = raw[raw["location"] != "World"].copy()
    raw["date"] = pd.to_datetime(raw["date"])
    keep = [c for c in raw.columns if c not in _DROP_COLS]
    return raw[keep].sort_values(["location", "date"]).reset_index(drop=True)


df = _load()

DATE_MIN = df["date"].min()
DATE_MAX = df["date"].max()
CONTINENTS = sorted(df["continent"].dropna().unique().tolist())
LOCATIONS = sorted(df["location"].unique().tolist())


def filter_df(start_date=None, end_date=None, locations=None, continent=None) -> pd.DataFrame:
    """Apply shared sidebar filters. locations may be None, 'All', or a list."""
    out = df
    if start_date is not None:
        out = out[out["date"] >= pd.to_datetime(start_date)]
    if end_date is not None:
        out = out[out["date"] <= pd.to_datetime(end_date)]
    if continent and continent != "All":
        out = out[out["continent"] == continent]
    if locations and locations != "All":
        if isinstance(locations, str):
            locations = [locations]
        if "All" not in locations:
            out = out[out["location"].isin(locations)]
    return out


def latest_by_country(dff: pd.DataFrame) -> pd.DataFrame:
    """One row per country: last observation in the filtered window."""
    if dff.empty:
        return dff
    idx = dff.groupby("location")["date"].idxmax()
    return dff.loc[idx].copy()


def period_kpis(dff: pd.DataFrame) -> dict:
    """Correct period KPIs: sum of new_* and latest cumulatives per country."""
    if dff.empty:
        return {
            "countries": 0,
            "new_cases": 0.0,
            "new_deaths": 0.0,
            "latest_cases": 0.0,
            "latest_deaths": 0.0,
        }
    latest = latest_by_country(dff)
    return {
        "countries": int(latest["location"].nunique()),
        "new_cases": float(dff["new_cases"].fillna(0).sum()),
        "new_deaths": float(dff["new_deaths"].fillna(0).sum()),
        "latest_cases": float(latest["total_cases"].fillna(0).sum()),
        "latest_deaths": float(latest["total_deaths"].fillna(0).sum()),
    }


def top_locations_by_cases(dff: pd.DataFrame, n: int = 8) -> list:
    latest = latest_by_country(dff)
    if latest.empty:
        return []
    return (
        latest.nlargest(n, "total_cases")["location"].tolist()
        if "total_cases" in latest
        else latest["location"].head(n).tolist()
    )


def country_snapshot(dff: pd.DataFrame) -> pd.DataFrame:
    """Country-level snapshot for rankings / socioeconomic analysis."""
    latest = latest_by_country(dff)
    if latest.empty:
        return latest

    period = dff.groupby("location", as_index=False).agg(
        period_new_cases=("new_cases", "sum"),
        period_new_deaths=("new_deaths", "sum"),
        peak_new_cases=("new_cases_smoothed", "max"),
    )

    peak_rows = []
    for loc, g in dff.groupby("location"):
        if g["new_cases_smoothed"].notna().any():
            i = g["new_cases_smoothed"].idxmax()
            peak_rows.append({"location": loc, "peak_cases_date": g.loc[i, "date"]})
        else:
            peak_rows.append({"location": loc, "peak_cases_date": pd.NaT})
    peaks = pd.DataFrame(peak_rows)

    snap = latest.merge(period, on="location", how="left")
    snap = snap.merge(peaks, on="location", how="left")
    snap["cfr"] = snap["total_deaths"] / snap["total_cases"].replace(0, pd.NA)
    return snap
