import random
import dash
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import pandas as pd

df = pd.read_csv("dataframe.csv")
# drop NA
df.dropna(subset = ["VIEWERS"], inplace=True)
# drop outlier
df = df[df.TeamIDsDate!='UA@MIZZU10-13-2012']


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Data report for football games"),
    html.Br(),
    # graph1: dropdown options -> viewers vs. attend
    html.Div(
        dcc.Dropdown(
            id='dropdown',
            options=[ 
                {'label': "If rain", 'value': "weatherb"},
                {'label': "Tempurature", 'value': "temp"},
                {'label': "Stadium", 'value': "stadium"},
                {'label': "Home Team", 'value': "Home Team"},
                {'label': "Visitor Team", 'value': "Visitor Team"}
                ],
            value = "weatherb"
        ),
        style={'width': '50%'}
    ),
    dcc.Graph(id='graph1'),
    html.Br(),
    html.Br(),
    html.Br(),  
    # graph2: radio options -> viewers vs. rating
    dcc.RadioItems(
        id='radio',
        options=[ 
            {'label': "Network", 'value': "Network"},
            {'label': "Home Team", 'value': "Home Team"},
            {'label': "Visitor Team", 'value': "Visitor Team"}
            ],
        value = "Network"
    ),
    dcc.Graph(id='graph2',figure={}),
    html.Br(),
    html.Br(),
    html.Br()
])


@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='dropdown', component_property='value')]
)
def update_graph1(dropdownValue):
    fig = px.scatter(df, x="VIEWERS", y="attend", 
                     color=dropdownValue, hover_name="TeamIDsDate")
    
    return fig


@app.callback(
    Output(component_id = 'graph2',component_property='figure'),
    [Input(component_id='radio',component_property='value')]
)
def update_graph2(radioValue):
    fig = px.scatter(df, x="VIEWERS", y="RATING", 
                     color=radioValue, hover_name="TeamIDsDate")

    return fig


if __name__ =='__main__':
    app.run_server(debug=True, port=8054)