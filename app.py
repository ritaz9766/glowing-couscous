import random
import dash
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import datetime as dt

### clean data
df = pd.read_csv("dataframe.csv")
# drop NA
df.dropna(subset = ["VIEWERS"], inplace=True)
# drop outlier
df = df[df.TeamIDsDate!='UA@MIZZU10-13-2012']
# revise column weatherb
df.weatherb = np.where(df.weatherb == 1, 'Yes', 'No')
df.rename(columns={'weatherb': 'If rain'}, inplace=True)
# revise column duration
df['duration'] = df['duration'].apply(lambda x: int(x[0]) * 60 + int(x[-2:]))
df.rename(columns={'duration': 'Duration (min)'}, inplace=True)
# revise column nightgame
df.nightgame = np.where(df.nightgame == 'Y', 'Yes', 'No')
df.rename(columns={'nightgame': 'If night game'}, inplace=True)
# revise column date
df['date'] = pd.to_datetime(df['date'])
df['Weekday'] = df['date'].dt.day_name()
# rename columns temp, stadium, RATING, VIEWERS, attend
df.rename(columns={'temp': 'Tempurature (°F)', 
                   'stadium': 'Stadium',
                   'RATING': 'Rating',
                   'VIEWERS': 'TV viewers',
                   'attend': 'Attendees'}, inplace=True)


# create a list for graph1 dropdown
color_list = ['If rain', 'Tempurature (°F)', 'Duration (min)', 'If night game', 
             'Weekday', 'Rating', 'Stadium', 'Home Team', 'Visitor Team']
graph1_dropdownDict = [{'label': col, 'value': col} for col in color_list]
# create a list for numeric variables
num_list = ['Tempurature (°F)', 'Duration (min)', 'Rating']
# create a list for categorical variables
cat_list = ['If rain', 'If night game', 'Weekday', 'Stadium']


### app starts here
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Data report for football games"),
    html.Br(),
    
    # graph1: overview of viewers vs. attend, dropdown -> color
    html.P([
        html.H2('TV viewers vs. Stadium attendance'),
        html.Label('Choose a color category:'),
        dcc.Dropdown(
            id='graph1_color',
            options=graph1_dropdownDict,
            value = "If rain", 
            style={'width': '50%'})]),
    dcc.Graph(id='graph1'),
    html.Br(),
    html.Br(),
    html.Br(),  
    
    # graph2: scatter plot of viewers/attend vs. numeric variables, categorical -> color
    html.H2('TV viewers/Attendees vs. a numeric variable'), 
    html.P([
        html.Label('Choose x axis:'),
        dcc.RadioItems(
            id='graph2_x',
            options=[{'label': 'TV viewers', 'value': 'TV viewers'},
                     {'label': 'Attendees', 'value': 'Attendees'}],
            value = "TV viewers")]),
    html.P([
        html.Label('Choose y axis:'),
        dcc.RadioItems(
            id='graph2_y',
            options=[{'label': num_col, 'value': num_col} for num_col in num_list],
            value = "Tempurature (°F)")]),
    html.P([
        html.Label('Choose a color category:'),
        dcc.RadioItems(
            id='graph2_color',
            options=[{'label': cat_col, 'value': cat_col} for cat_col in cat_list],
            value = "If rain")]),
    html.Div(id='graph2_title', style={'font-weight': 'bold', 'textAlign': 'center'}),
    dcc.Graph(id='graph2',figure={}),
    html.Br(),
    html.Br(),
    html.Br(),
    
    # graph3: bar plot of viewers/attend by categorical variables, numeric -> color
    html.H2('TV viewers/Attendees by a categorical variable'),
    html.P([
        html.Label('Choose x axis:'),
        dcc.RadioItems(
            id='graph3_x',
            options=[{'label': cat_col, 'value': cat_col} for cat_col in cat_list],
            value = "If rain")]),
    html.P([
        html.Label('Choose y axis:'),
        dcc.RadioItems(
            id='graph3_y',
            options=[{'label': 'TV viewers', 'value': 'TV viewers'},
                     {'label': 'Attendees', 'value': 'Attendees'}],
            value = "TV viewers")]),
    html.P([
        html.Label('Choose a color category:'),
        dcc.RadioItems(
            id='graph3_color',
            options=[{'label': num_col, 'value': num_col} for num_col in num_list],
            value = "Tempurature (°F)")]),
    html.Div(id='graph3_title', style={'font-weight': 'bold', 'textAlign': 'center'}),
    dcc.Graph(id='graph3',figure={})
    
])

# graph1
@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='graph1_color', component_property='value')]
)
def update_graph1(color):
    fig = px.scatter(df, x="TV viewers", y="Attendees", 
                     color=color, hover_name="TeamIDsDate")
    
    return fig

# graph2
@app.callback(
    Output(component_id = 'graph2',component_property='figure'),
    [Input(component_id='graph2_x',component_property='value'),
     Input(component_id='graph2_y',component_property='value'),
     Input(component_id='graph2_color',component_property='value')]
)
def update_graph2(x, y, color):
    fig = px.scatter(df, x=x, y=y, color=color, hover_name="TeamIDsDate")

    return fig

@app.callback(
    Output('graph2_title', 'children'),
    [Input('graph2_x', 'value'),
     Input('graph2_y', 'value')]
)
def graph2_display(x, y):
    return f'{x} vs. {y}'

# graph3
@app.callback(
    Output(component_id = 'graph3',component_property='figure'),
    [Input(component_id='graph3_x',component_property='value'),
     Input(component_id='graph3_y',component_property='value'),
     Input(component_id='graph3_color',component_property='value')]
)
def update_graph2(x, y, color):
    fig = px.bar(df, x=x, y=y, color=color, hover_name="TeamIDsDate")

    return fig

@app.callback(
    Output('graph3_title', 'children'),
    [Input('graph3_x', 'value'),
     Input('graph3_y', 'value')]
)
def graph3_display(x, y):
    return f'{y} by {x}'


if __name__ =='__main__':
    app.run_server(debug=True, port=8054)