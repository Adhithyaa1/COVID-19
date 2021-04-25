import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html 
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import os as os

from webapp import app
import ctab1 
import ctab2 
import ctab3
import csidepanel 
import ctransforms

import sqlite3
import Dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

app.layout = csidepanel.layout

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return ctab1.layout
    elif tab == 'tab-2':
       return ctab2.layout
    elif tab == 'tab-3':
        return ctab3.layout


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    [Output('table-sorting-filtering', 'data'),
    Output('qty','children'),
    Output('dea','children')]
     , [Input('table-sorting-filtering', "page_current")
     , Input('table-sorting-filtering', "page_size")
     , Input('table-sorting-filtering', 'sort_by')
     , Input('table-sorting-filtering', 'filter_query')
     , Input('rating-95', 'value')
     , Input('price-slider', 'value')
     , Input('month-slider', 'value')
     , Input('day-slider', 'value') 
     , Input('location', 'value')
     ])
def update_table(page_current, page_size, sort_by, filter1, ratingcheck, prices ,month, day, location):
    filtering_expressions = filter1.split(' && ')
    dff = ctransforms.df
    
    low = prices[0]
    high = prices[1]

    jan=month[0]
    dec=month[1]
    
    mind=day[0]
    maxd=day[1]    
    
    dff1=[]
    
    if 'All' in location :
        dff=ctransforms.df
    else:
        for i in location:
            dff = ctransforms.df
            if location=={'label': 'All', 'value': 'All'}:
    
                dff=dff
        
            else:
                dff1.append(dff.loc[(dff['location']==i)])
        dff = pd.concat(dff1)
        
    dff = dff.loc[(dff['year'] >= low) & (dff['year'] <= high)]
    
    dff = dff.loc[(dff['month'] >= jan) & (dff['month'] <= dec)]

    dff = dff.loc[(dff['day'] >= mind) & (dff['day'] <= maxd)]
    
    
    dff=dff.drop(['year','month','day'], axis=1)

    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    page = page_current
    size = page_size
    
    
                 
    return dff.iloc[page * size: (page + 1) * size].to_dict('records'),dff['total_cases'].sum()/1000000,dff['total_deaths'].sum()/1000000

    
        
    
    
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='5000', debug = True)
