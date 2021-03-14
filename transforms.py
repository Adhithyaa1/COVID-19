import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd


df = pd.read_csv(r'C:/Users/adhi3/OneDrive/Desktop//covidmaster2.csv')
df=df[df['location']!='World']
