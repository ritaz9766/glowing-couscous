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
df.dropna(subset = ["VIEWERS"], inplace=True)
fig2= px.scatter(df,x= "VIEWERS",y="attend")




app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("data report for football games"),
    html.Br(),
    #first graph is just viewers aganist attend
    html.H1("overview"),
    dcc.Graph(figure=fig2),
    html.Br(),
    html.Br(),
    html.Br(),
    #second graph would be colunms agaist people who watched the game ON tv
    html.H3("TV viewers"),
    dcc.Dropdown(
        id = 'color1',
        options =[ 
            {'label': "game rating", 'value': "RATING"},
            {'label': "Home Team", 'value': "Home Team"},
            {'label': "Visit Team", 'value': "VisTeamID"},
            {'label': "Network", 'value': "Network"},
            {'label': "Score Home", 'value': "score_home"},
            ],
        value = "RATING",
        placeholder = "color by"
    ),
    dcc.Graph(id = 'outputgraph1',figure={}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H3("attendees"),
    dcc.Dropdown(
        id = 'graph2',
        options =[ 
            {'label': "game rating", 'value': "RATING"},
            {'label': "Home Team", 'value': "Home Team"},
            {'label': "Visit Team", 'value': "VisTeamID"},
            {'label': "If rain", 'value': "weatherb"},
            {'label': "Stadium", 'value': "stadium"},
            {'label': "Tempurature", 'value': "temp"}
            ],
        value = "RATING",
        placeholder = "aganist"
    ),
    dcc.Graph(id = 'outputgraph2',figure={}),
])

@app.callback(
    Output(component_id = 'outputgraph1',component_property='figure'),
    Output(component_id = 'outputgraph2',component_property='figure'),
    [Input(component_id='color1',component_property='value'),
    Input(component_id='graph2',component_property='value')]
)
def updategraph(color1value,yax):
    fig = px.scatter(df,x="VIEWERS",y="RATING",color=color1value)
    fig2 = px.scatter(df,x="attend",y=yax,color="RATING",hover_name="TeamIDsDate")
    return fig,fig2


if __name__ =='__main__':
    app.run_server(debug=True, port=8054)