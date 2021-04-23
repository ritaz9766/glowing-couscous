import pandas as pd
import plotly
import plotly.express as px
import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input,Output, State
from dash.exceptions import PreventUpdate
import matplotlib.pyplot as plt




SA = pd.read_csv("games_flat_xml_2012-2018.csv")      

SA['postseason']=  SA.postseason.apply(lambda x :1 if x == 'Y' else '0')
# Y => 1, character(0) => 0
SA['neutralgame']=  SA.neutralgame.apply(lambda x :1 if x == 'Y' else '0')  # Y => 1, character(0) => 0

# convert duration to minutes
SA['duration'] = SA['duration'].apply(lambda x: int(x[0]) * 60 + int(x[-2:]))

plt.scatter(SA['neutralgame'], SA['attend'])
plt.show()


#make weather binary: if rain then 1 else then 0
x=0
for i in SA['weather'] :
    if i in ['Showers','94% hum. 30% rain', 'Rainy','Cloudy, Light Rain','rain','Light Rain','Steady rain','Rain in the area.','Cloudy with rain','Nice, rain in area','showers, 90% humid.','Cloudy, 25% Rain','lt. rain, 75% humid.','scattered', 'Light rain, Overcast','Cloudy rain possible','Light rain,87% humid','light rain','Cloudy/Rain','Cloudy, Drizzly','cloudy, light rain','Rain in the area','Overcast, light rain','Rain','Drizzly','Light rain','Chance of rain','74% humid., lt.rain','RAINY','40% chance of rain','Cloudy, light rain','Cloudy & Rain','Intermittent Rain','Cloudy possible rain','Intermittent Showers']:
        SA['weatherb'].iloc[x] = 1 
     else: 
        SA['weatherb'].iloc[x] = 0
    x=x+1
  
SA['weather'].value_counts().head(30)