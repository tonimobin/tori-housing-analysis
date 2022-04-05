from os import sep
from tokenize import group
from turtle import color
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go

app = Dash(__name__)

# Load the data, drop records with empty fields, convert num data to int and sort by price
df = pd.read_csv('housing.csv', sep=',')
df.dropna(subset=['Price', 'Rooms' ,'Size', 'Type', 'Year'], inplace=True)
df = df.astype({"Price":'int', "Year":'int', "Size":'int'}) 
df = df.sort_values(by=['Price'])

# fig = px.bar(df, x="Title", y="Price", barmode="group")

colors = {
    "first-color" : "#ffffcc",
    "second-color" : "#c7e9b4",
    "third-color" : "#7fcdbb",
    "fourth-color" : "#41b6c4",
    "fifth-color" : "#1d91c0",
    "sixth-color" : "#225ea8",
    "seventh-color" : "#0c2c84",
}
np.random.seed(50)
x_rand = np.random.randint(1, 61, 60)
y_rand = np.random.randint(1, 61, 60)
app.layout = html.Div([

    html.H1(children = 'Tori.fi Housing Data Analysis',
            style = {
                'textAlign' : 'center',
                'color' : colors['seventh-color']
            }),
    html.Div(children = 'Data scraped on 4th of April, 2022.',
            style = {
                'textAlign' : 'left',
                'color' : colors['sixth-color']
            }),
    dcc.Dropdown(
        id = 'first-dropdown',
        options = [
            {'label' : 'Row House', 'value': '1'},
            {'label' : 'Block of Flats', 'value': '2'},
            {'label' : 'Detached House', 'value': '3'},
            {'label' : 'Balcony Access Block', 'value': '4'},
        ],
        value = 'NYC',
        placeholder='Housing type'
    ),
    dcc.Graph(
        id='scatter_chart',
        figure = {
            'data' : [
                go.Scatter(
                    x = df['Size'],
                    y = df['Price'],
                    mode = 'markers',
                )
            ],
            'layout': go.Layout(
                title = 'Price by Size plotting',
                xaxis = {'title' : 'Size of the house'},
                yaxis = {'title' : 'Price of the house'},
            )
        }
    ),
])
        

if __name__ == '__main__':
    app.run_server(debug=True)

