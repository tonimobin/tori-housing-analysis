from os import sep
from tokenize import group
from turtle import color
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import math

app = Dash(__name__)

# Load the data, drop records with empty fields, convert num data to int and sort by price
df = pd.read_csv("full_data_cleaned_and_outliers_removed.csv", sep=",")
df.dropna(subset=["Price", "Rooms", "Size", "Type", "Year"], inplace=True)
df = df.astype({"Price": "int", "Year": "int", "Size": "int"})
df = df.sort_values(by=["Price"])

housing_types = np.sort(df["Type"].unique())
locations = np.sort(df["Location"].unique())
rooms = np.sort(df["Rooms"].unique())

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
    
    html.Div([
        html.Span(id="title-p1", children="tori.fi"),
        html.Span(id="title-p2", children=" Housing Analysis"),
        html.Br(),
    ], style={"width": "100%", "display": "flex", "align-items": "center", "justify-content": "center"}),

    # Data & Options
    html.Div([

        # Data display
        html.Div(children=[
            dcc.Graph(
                id="scatter_chart",
                figure={
                    "data": [
                        go.Scatter(
                            x=df["Size"],
                            y=df["Price"],
                            mode="markers",
                        )
                    ],
                    "layout": go.Layout(
                        title="Price by Size plotting",
                        xaxis={"title": "Size of the house"},
                        yaxis={"title": "Price of the house"},
                    )
                }
            ),
            html.Div(id="location-output")
        ], style={"padding": 10, "flex": 1}),

        # Options
        html.Div(children=[
            html.Label("Type:"),
            dcc.Dropdown(
                id="housing-type-dropdown",
                options=[{"label": x, "value": x} for x in housing_types],
                placeholder="Select housing type",
                multi=True
            ),
            html.Label("Location:"),
            dcc.Dropdown(
                id="location-dropdown",
                options=[{"label": x, "value": x} for x in locations],
                placeholder="Select location",
                multi=True
            ),
            html.Label(id="price-label",children = "Price:"),
            dcc.RangeSlider(
                id="price-slider",
                min=df.Price.min(),
                max=df.Price.max(),
                step=5000,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": False}
            ),
            html.Label(id="year-label", children = "Year:"),
            dcc.RangeSlider(
                id="year-slider",
                min=df.Year.min(),
                max=df.Year.max(),
                value=[df.Year.min(), df.Year.max()],
                step=1,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": False}
            ),
            html.Label(id="size-label", children = "Size:"),
            dcc.RangeSlider(
                id="size-slider",
                min=df.Size.min(),
                max=df.Size.max(),
                step=1,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": False}
            ),
            html.Label("Rooms"),
            dcc.Checklist(
                id="rooms-checklist",
                options=[{"label": x, "value": x} for x in rooms],
                inline=False,
                labelStyle={"display": "block"},
                style={"width": 200, "overflow": "auto"}
            ),
        ], style={"padding": 10, "flex": 1, "align": "right"}),
    ], style={"display": "flex", "flex-direction": "row"}),
        # Key figures
        html.Div([
            html.H1("Key figures"),
            html.P("Mean €/m²: "),
            html.Div(id="mean-price-m2-output", children=f"{math.floor(df.Price.sum() / df.Size.sum())} €"),
            html.P("Median year of construction: "),
            html.Div(id="median-year-output"),
            html.P("Most popular housing type: "),
            html.Div(id="pop-housing-output", children=f"{df['Type'].value_counts().idxmax()}"),
            html.P("Cheapest: "),
            html.Div(id="cheapeast-output", children=f"{df['Price'].min()} €"),
            html.P("Most expensive: "),
            html.Div(id="most-expensive-output", children=f"{df['Price'].max()} €"),
            html.P("Mean price: "),
            html.Div(id="mean-price-output", children=f"{math.floor(df['Price'].mean())} €"),
        ])
])

@app.callback(Output("median-year-output", "children"), Input("year-slider", "value"))
def display_output(value):
    return f"{value}"

if __name__ == "__main__":
    app.run_server(debug=True)

