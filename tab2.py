import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_table
from webapp import app
import ctransforms

df = ctransforms.df

layout = html.Div(
            id='table-paging-with-graph-container',
            className="five columns"
        )

@app.callback(Output('table-paging-with-graph-container', "children"),
[Input('rating-95', 'value')
, Input('price-slider', 'value')
, Input('month-slider', 'value')
, Input('day-slider', 'value')
, Input('location', 'value')  
])

def update_graph(ratingcheck, prices ,month, day, location):
    dff = df
     
    low = prices[0]
    high = prices[1]

    jan=month[0]
    dec=month[1]
    
    mind=day[0]
    maxd=day[1]
    
        
    dff1=[]
    
    if 'All' in location:
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

    trace1 = go.Scattergl(x = dff['date']
                        , y = dff['total_cases']
                        , text=dff['location']  
                        , mode='markers'
                        , opacity=0.7
                        , marker={
                                'size': 8
                                , 'line': {'width': 0.5, 'color': 'white'}
                                }
                        , name='total_cases vs date'
                        , hoverinfo='x+y+text'
                    )
    return html.Div([
        dcc.Graph(
            id='rating-price'
            , figure={
                'data': [trace1
                    # dict(
                    #     x=df['price'],
                    #     y=df['rating'],
                    #     #text=df[df['continent'] == i]['country'],
                    #     mode='markers',
                    #     opacity=0.7,
                    #     marker={
                    #         'size': 8,
                    #         'line': {'width': 0.5, 'color': 'white'}
                    #     },
                    #     name='Price v Rating'
                    #) 
                ],
                'layout': dict(
                    xaxis={'title': 'date'},
                    yaxis={'title': 'total_cases'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            }
        )
    ])
