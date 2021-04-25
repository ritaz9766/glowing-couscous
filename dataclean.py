import pandas as pd
import plotly
import plotly.express as px
import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input,Output, State
from dash.exceptions import PreventUpdate
import matplotlib.pyplot as plt


df = pd.read_csv("games_flat_xml_2012-2018.csv") 


# convert temp column
df['temp'] = df['temp'].fillna(0)
df['temp'] = df['temp'].replace({"Indoor": "72","Indoors":"72","N/A/":"0"})
df['temp'] = df['temp'].to_list()
df['temp'] = [int(str(s)[:2]) for s in df['temp'] ]


##convert date column
df['date'] = pd.to_datetime(df['date'])


#convert weather to binary if rain or not
df['postseason']=  df.postseason.apply(lambda x :1 if x == 'Y' else '0')
# Y => 1, character(0) => 0
df['neutralgame']=  df.neutralgame.apply(lambda x :1 if x == 'Y' else '0')  # Y => 1, character(0) => 0
plt.scatter(df['neutralgame'], df['attend'])
plt.show()
#make weather binary: if rain then 1 else then 0

df['weatherb'] = 0

for x, i in enumerate(df['weather']):
    if i in ['Showers','94% hum. 30% rain', 'Rainy','Cloudy, Light Rain','rain','Light Rain',
            'Steady rain','Rain in the area.','Cloudy with rain','Nice, rain in area','showers, 90% humid.',
            'Cloudy, 25% Rain','lt. rain, 75% humid.','scattered', 'Light rain, Overcast','Cloudy rain possible',
            'Light rain,87% humid','light rain','Cloudy/Rain','Cloudy, Drizzly','cloudy, light rain','Rain in the area',
            'Overcast, light rain','Rain','Drizzly','Light rain','Chance of rain','74% humid., lt.rain','RAINY','40% chance of rain',
            'Cloudy, light rain','Cloudy & Rain','Intermittent Rain','Cloudy possible rain','Intermittent Showers']:

         
        df['weatherb'].iloc[x] = 1 


df['weatherb'].value_counts().head(30)
df['attend'].describe()


#merging 2 tables 
df1 = pd.read_csv("TV_Ratings_onesheet.csv")
df2 = pd.merge(df, df1, on="TeamIDsDate")

df2.to_csv("dataframe.csv")

