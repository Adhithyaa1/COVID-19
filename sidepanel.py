import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html 
import dash_bootstrap_components as dbc 
import dash_table
import pandas
from dash.dependencies import Input, Output

import webapp
import ctab1
import ctab2
import ctab3
import ctransforms

def BuildOptions(df, AddAll):  
    OptionList = [{'label': i, 'value': i} for i in df.unique()]
    if AddAll == 1:       
        OptionList.insert(0,{'label': 'All', 'value': 'All'})          
    return OptionList

df = ctransforms.df
min_p=df.year.min()
max_p=df.year.max()

min_m=df.month.min()
max_m=df.month.max()

min_d=df.day.min()
max_d=df.day.max()

qty=df.total_cases.sum()
dea=df.total_deaths.sum()

options_array1 = BuildOptions(df.location,1)

layout = html.Div([
    html.H1('COVID-19',style={'text-align':'center'})
    ,dbc.Row([dbc.Col(
        html.Div([
         html.H2('Filters')
        , html.Div(id='rating-95'
        )
        ,html.Div([html.H5('Year Slider')
            ,dcc.RangeSlider(id='price-slider'
                            ,min = min_p
                            ,max= max_p
                            , marks = { 2020:'2020',
                                       2021:'2021',
                                       }
                            , value = [2020,2021]
                            )
                        
                            ]),
            html.Div([html.H5('Month Slider')
            ,dcc.RangeSlider(id='month-slider'
                            ,min = min_m
                            ,max= max_m
                            , marks = { 1:'1',
                                        2:'2',
                                        3:'3',
                                        4: '4',
                                        5: '5',
                                        6: '6',
                                        7: '7',
                                        8: '8',
                                        9: '9',
                                        10: '10',
                                       11:'11',
                                       12:'12',
                                       }
                            , value = [1,12]
                            )
                             
                              ]),
            html.Div([html.H5('Day Slider')
            ,dcc.RangeSlider(id='day-slider'
                            ,min = min_d
                            ,max= max_d
                            , marks = { 1:'1',
                                        3:'3',
                                        5: '5',
                                        7: '7',
                                        9: '9',
                                       11:'11',
                                       13:'13',
                                       15:'15',
                                       17:'17',
                                       19:'19',
                                       21:'21',
                                       23:'23',
                                       25:'25',
                                       27:'27',
                                       29:'29',
                                       31:'31',
                                       }
                            , value = [1,31]
                            )        
                        
                            ])
        ,html.Div([html.H5('Country')
            ,dcc.Dropdown(id='location'
                            ,options=options_array1,
                            value='All',
                                multi=True
                            )],
                        className='two columns'
                            )
            ,html.Br()
            ,html.Div(html.H5("TOTAL CASES(Million)"))

            ,html.Div(
                                    id="qty",
                                    className="mini_container",
                                    style={"visibility": "visible"},
                                )
            ,html.Br()
            ,html.Div(html.H5("TOTAL DEATHS(Million)"))

            ,html.Div(
                                    id="dea",
                                    className="mini_container",
                                    style={"visibility": "visible"},
                                ),
                  
        ], style={'marginBottom': 50, 'marginTop': 25, 'marginLeft':15, 'marginRight':15})
    , width=3)

    ,dbc.Col(html.Div([
            dcc.Tabs(id="tabs", value='tab-1', style={'width':'100%'}, children=[
                    dcc.Tab(label='Data Table', value='tab-1'),
                    dcc.Tab(label='Cases Plot', value='tab-2'),
                    dcc.Tab(label='Deaths Plot', value='tab-3'),
                ])
            , html.Div(id='tabs-content')
        ]), width=9)])
    
    ])

