from os import sep
from tokenize import group
from turtle import color
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go

app = Dash(__name__)

# Load the data, drop records with empty fields, convert num data to int and sort by price
df = pd.read_csv('full_data_cleaned_and_outliers_removed.csv', sep=',')
df.dropna(subset=['Price', 'Rooms', 'Size', 'Type', 'Year'], inplace=True)
df = df.astype({"Price": 'int', "Year": 'int', "Size": 'int'})
df = df.sort_values(by=['Price'])

housing_types = np.sort(df['Type'].unique())
locations = np.sort(df['Location'].unique())
rooms = np.sort(df['Rooms'].unique())

colors = {
    "first-color": "#ffffcc",
    "second-color": "#c7e9b4",
    "third-color": "#7fcdbb",
    "fourth-color": "#41b6c4",
    "fifth-color": "#1d91c0",
    "sixth-color": "#225ea8",
    "seventh-color": "#0c2c84",
}
np.random.seed(50)
x_rand = np.random.randint(1, 61, 60)
y_rand = np.random.randint(1, 61, 60)
app.layout = html.Div([
    # Title
    html.H1(children='Tori.fi Housing Data Analysis',
            style={
                'textAlign': 'center',
                'color': colors['seventh-color']
            }),
    html.Div(children='Data scraped on 4th of April, 2022.',
             style={
                 'textAlign': 'left',
                 'color': colors['sixth-color']
             }),

    # Data & Options
    html.Div([

        # Data display
        html.Div(children=[
            dcc.Graph(
                id='scatter_chart',
                figure={
                    'data': [
                        go.Scatter(
                            x=df['Size'],
                            y=df['Price'],
                            mode='markers',
                        )
                    ],
                    'layout': go.Layout(
                        title='Price by Size plotting',
                        xaxis={'title': 'Size of the house'},
                        yaxis={'title': 'Price of the house'},
                    )
                }
            ),
            html.Div(id='location-output')
        ], style={'padding': 10, 'flex': 1}),

        # Options
        html.Div(children=[
            dcc.Dropdown(
                id='housing-type-dropdown',
                options=[{"label": x, "value": x} for x in housing_types],
                placeholder='Select housing type',
                multi=True
            ),
            html.Label('Location:'),
            dcc.Dropdown(
                id='location-dropdown',
                options=[{"label": x, "value": x} for x in locations],
                placeholder='Select location',
                multi=True
            ),
            html.Label('Price:'),
            dcc.RangeSlider(
                id='price-slider',
                min=100000,
                max=500000,
                step=5000,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Label('Year:'),
            dcc.RangeSlider(
                id='year-slider',
                min=df.Year.min(),
                max=df.Year.max(),
                step=1,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Label('Size:'),
            dcc.RangeSlider(
                id='size-slider',
                min=0,
                max=250,
                step=25,
                tooltip={"placement": "bottom", "always_visible": False}
            ),
            html.Label('Rooms'),
            dcc.Checklist(
                id="rooms-checklist",
                options=[{"label": x, "value": x} for x in rooms],
                inline=False,
                labelStyle={'display': 'block'},
                style={"width": 200, "overflow": "auto"}
            ),
        ], style={'padding': 10, 'flex': 1, 'align': "right"}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),
        # Key figures
        html.Div([
            html.H1("Key figures"),
            html.P("Average $/m²: "),
            html.P("Amount of listings: "),
            html.P("Average price: "),
        ])
])


@app.callback(Output('location-output', 'children'), Input('location-dropdown', 'value'))
def display_output(value):
    return f'You have selected "{value}"'


if __name__ == '__main__':
    app.run_server(debug=True)

