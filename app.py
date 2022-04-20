from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import math

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
meta_tags=[{"name" : "viewport", "content" : "width=device-width, initial-scale=1.0"}])

# Load the data, drop records with empty fields, convert num data to int and sort by price
df = pd.read_csv("full_data_cleaned_and_outliers_removed.csv", sep=",")
df.dropna(subset=["Price", "Rooms", "Size", "Type", "Year"], inplace=True)
df = df.astype({"Price": "int", "Year": "int", "Size": "int"})
df = df.sort_values(by=["Price"])

# Create a new column, "Price_M2", which calculates €/m² for every row
df["Price_M2"] = df.apply(lambda row: row.Price / row.Size, axis=1)

housing_types = np.sort(df["Type"].unique())
locations = np.sort(df["Location"].unique())
rooms = np.sort(df["Rooms"].unique())

app.layout = dbc.Container([
    # Store
    dcc.Store(id="memory-output"),

    # Title
    dbc.Row([
        dbc.Col(
            html.Div([
            html.Span(id="title-p1", children="tori.fi"),
            html.Span(id="title-p2", children=" Housing Analysis"),
            html.Br(),
        ], style={"width": "100%", "display": "flex", "alignItems": "center", "justifyContent": "center"}),
        )
    ]),
    # Main data-graph and query options
    dbc.Row([
        # data-graph
        dbc.Col(
            html.Div(children=[
                dcc.Graph(
                    id="scatter-chart"
                )]),
                width={"size": 9}
        ),
        # query options
        dbc.Col(
            html.Div(children=[
                html.Label("Type:"),
                dcc.Dropdown(
                    id="housing-type-dropdown",
                    options=[{"label": x, "value": x} for x in housing_types],
                    placeholder="Select housing type",
                    multi=True,
                ),
                html.Label("Location:"),
                dcc.Dropdown(
                    id="location-dropdown",
                    options=[{"label": x, "value": x} for x in locations],
                    placeholder="Select location",
                    multi=True
                ),
                html.Label(id="price-label", children="Price:"),
                dcc.RangeSlider(
                    id="price-slider",
                    min=df.Price.min(),
                    max=df.Price.max(),
                    value=[df.Price.min(), df.Price.max()],
                    step=5000,
                    marks=None,
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
                html.Label(id="year-label", children="Year:"),
                dcc.RangeSlider(
                    id="year-slider",
                    min=df.Year.min(),
                    max=df.Year.max(),
                    value=[df.Year.min(), df.Year.max()],
                    step=1,
                    marks=None,
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
                html.Label(id="size-label", children="Size:"),
                dcc.RangeSlider(
                    id="size-slider",
                    min=df.Size.min(),
                    max=df.Size.max(),
                    value=[df.Size.min(), df.Size.max()],
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
                    style={"width": 200, "overflow": "auto"},
                    labelClassName="mr-1"
                ),
            ]),
            width={"size": 3}
        ),
    ], justify="around"),
    # Key figures
    dbc.Row([
        dbc.Col(
            html.Div(id="key-figures"),
        )
    ]),

    # Pie charts
    dbc.Row([
        html.H4("Distributions of listings by room"),
        dbc.Col(
            dcc.Graph(id="rooms-pie"), width="4"
        ),
        html.H4("Distributions of listings by type"),
        dbc.Col(    
            dcc.Graph(id="types-pie"), width="4"
        )
    ], justify="between"),
], fluid=True)
    
# Handle updates to data when user makes different queries
@app.callback(
    Output("memory-output", "data"),
    Input('housing-type-dropdown', 'value'),
    Input('location-dropdown', 'value'),
    Input('price-slider', 'value'),
    Input('year-slider', 'value'),
    Input('size-slider', 'value'),
    Input('rooms-checklist', 'value'))
def filter_data(housing_type_dropdown, location_dropdown, price_slider, year_slider,
                size_slider, rooms_checklist):

    # Filter data by slider values
    dff = df[df['Year'].between(year_slider[0], year_slider[1], inclusive="both")]
    dff = dff[dff['Price'].between(price_slider[0], price_slider[1], inclusive="both")]
    dff = dff[dff['Size'].between(size_slider[0], size_slider[1], inclusive="both")]

    # Filter data by checklist selections
    if rooms_checklist:
        dff = dff[dff["Rooms"].isin(rooms_checklist)]

    # Filter data by dropdown selections
    if housing_type_dropdown:
        dff = dff[dff["Type"].isin(housing_type_dropdown)]
    if location_dropdown:
        dff = dff[dff["Location"].isin(location_dropdown)]

    return dff.to_dict("records")

# Update scatter chart
@app.callback(Output("scatter-chart", "figure"), Input("memory-output", "data"))
def update_scatter(data):
    if data is None:
        raise PreventUpdate
    df = pd.DataFrame(data)
    try:
        figure = {
                "data": [
                    go.Scatter(
                        x=df["Size"],
                        y=df["Price"],
                        mode="markers",
                        marker=dict(
                            color='#F38912',
                            size=4,
                            opacity=0.6,
                            # line=dict(
                            #     color='Black',
                            #     width=1
                            # )
                        ),
                    )],
                "layout": go.Layout(
                    title="Available listings",
                    xaxis={"title": "Size m²"},
                    yaxis={"title": "Price €"},
                )
            }
    # If no listings are found with given features, return a message informing the user.
    except(KeyError):
        figure = {
            "layout": {
                "xaxis": {
                    "visible": "false"
                },
                "yaxis": {
                    "visible": "false"
                },
                "annotations": [
                    {
                        "text": "No available listings with given features.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": "false",
                        "font": {
                                "size": 28
                        }
                    }
                ]
            }
        }
        return figure
    return figure

# Update key figures
@app.callback(Output("key-figures", "children"),
              Input("memory-output", "data"))
def update_keyfigs(data):
    if data is None:
         raise PreventUpdate
    df = pd.DataFrame(data)
    if len(df) > 0:
        return [
            html.Div(
                children=[
                    html.H1("Key figures"),
                    html.P(f"Amount of listings: {len(df)}"),
                    html.P(f"Mean €/m²: {math.floor(df.Price.sum() / df.Size.sum())}€"),
                    html.P(f"Median year of construction: {math.floor(df.Year.median())}"),
                    html.P(f"Cheapest listing: {df.Price.min()}€"),
                    html.P(f"Most expensive listing: {df.Price.max()}€"),
                    html.P(f"Mean price of the listings: {math.floor(df.Price.mean())}€")
                ]
            )
        ]
    else:
        return [
            html.Div(
                html.P("-")
            )
        ]

# Update rooms pie chart (to:do prevent empty dataset error for this & type)
@app.callback(Output("rooms-pie", "figure"),
              Input("memory-output", "data"))
def update_rooms_pie(data):
    colors = ["#0B2027", "#40798C", "#70A9A1", "#CFD7C7", "#F6F1D1", "E9E0A6"]
    if data is None:
         raise PreventUpdate
    df = pd.DataFrame(data)
    rooms = df["Rooms"].unique()
    room_count = df["Rooms"].value_counts(sort=False).array
    figure = go.Figure(data=[go.Pie(labels=rooms, values=room_count)])
    figure.update_traces(hoverinfo="value+percent", textinfo="label", marker=dict(colors = colors))
    return figure

# Update types pie chart
@app.callback(Output("types-pie", "figure"),
              Input("memory-output", "data"))
def update_types_pie(data):
    colors = ["#0B2027", "#40798C", "#70A9A1", "#CFD7C7", "#F6F1D1", "E9E0A6"]
    if data is None:
         raise PreventUpdate
    df = pd.DataFrame(data)
    types = df["Type"].unique()
    type_count = df["Type"].value_counts(sort=False).array
    figure = go.Figure(data=[go.Pie(labels=types, values=type_count)])
    figure.update_traces(hoverinfo="value+percent", textinfo="label", marker=dict(colors = colors))
    return figure
if __name__ == "__main__":
    app.run_server(debug=True)

