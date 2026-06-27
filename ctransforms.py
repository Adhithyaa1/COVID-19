import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd


from pathlib import Path

_DATA_PATH = Path(__file__).resolve().parent / "covidmaster2.csv"
df = pd.read_csv(_DATA_PATH)
df=df[df['location']!='World']
