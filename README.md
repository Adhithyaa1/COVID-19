# COVID-19 Analytics Lab

Interactive Dash dashboard for exploratory analysis of early-pandemic COVID-19 data
(Our World in Data–style country-day panel, Jan 2020 – Jan 2021).

## What it demonstrates

| Tab | Analysis |
|-----|----------|
| **Data Explorer** | Filterable/sortable daily observations with methodologically correct KPIs |
| **Epidemic Curves** | Multi-country smoothed incidence (absolute & per million, linear/log) |
| **Country Rankings** | Latest-in-window rankings, CFR, peak timing — not sums of cumulatives |
| **Policy & Transmission** | Stringency vs lagged cases, R(t), cross-country policy scatter |
| **Socioeconomic Lens** | GDP / HDI / age / hospital beds vs mortality with Pearson correlation |

Shared filters: date range, continent, multi-country select.

## Run locally

```bash
pip install -r requirements.txt
python dash_callbacks.py
```

## Deploy

- **Vercel:** `wsgi.py` exports the Flask server (`pyproject.toml` entrypoint `wsgi:app`)
- **Heroku:** `Procfile` → `gunicorn wsgi:app`

## Data notes

- Source file: `covidmaster2.csv` (~59k rows, ~190 countries after dropping `World`)
- KPIs: period **new** cases/deaths = sum of daily `new_*`; latest totals = last cumulative per country in range
- Policy and socioeconomic views are **observational** — reporting capacity and testing confound many relationships
