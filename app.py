from os import sep
from tokenize import group
from turtle import color
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
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

# Create a new column, "Price_M2", which calculates €/m² for every row
df["Price_M2"] = df.apply(lambda row: row.Price / row.Size, axis=1)

housing_types = np.sort(df["Type"].unique())
locations = np.sort(df["Location"].unique())
rooms = np.sort(df["Rooms"].unique())

app.layout = html.Div([
    # Store
    dcc.Store(id="memory-output"),

    # Title
    html.Div([
        html.Span(id="title-p1", children="tori.fi"),
        html.Span(id="title-p2", children=" Housing Analysis"),
        html.Br(),
    ], style={"width": "100%", "display": "flex", "alignItems": "center", "justifyContent": "center"}),

    # Data & Options
    html.Div([

        # Data display
        html.Div(children=[
            dcc.Graph(
                id="scatter-chart",
        )], style={"padding": 10, "flex": 1}),

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
                value=[df.Price.min(), df.Price.max()],
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
                style={"width": 200, "overflow": "auto"}
            ),
        ], style={"padding": 10, "flex": 1, "align": "right"}),
    ], style={"display": "flex", "flexDirection": "row"}),
        # Key figures
        html.Div([
            html.H1("Key figures"),
            html.P("Amount of listings: "),
            html.Div(id="amount-listings"),
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
                    )],
                "layout": go.Layout(
                    title="Available listings",
                    xaxis={"title": "Size"},
                    yaxis={"title": "Price"},
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
    # filtered_df = df.copy()
    # if rooms_checklist or housing_type_dropdown:
    #     if rooms_checklist:
    #         filtered_df = df[df["Rooms"].isin(rooms_checklist)]
    #     if housing_type_dropdown:
    #         filtered_df = filtered_df[filtered_df["Type"].isin(housing_type_dropdown)]
    #     return filtered_df.to_dict('records')
    # else:
    #     return df.to_dict('records')

# Callbacks related to key figures panel (and the only data panel for now)
# @app.callback(
#     Output("mean-price-output", "children"),
#     Output("most-expensive-output", "children"),
#     Output("cheapeast-output", "children"),
#     Output("pop-housing-output", "children"),
#     Output("median-year-output", "children"),
#     Output("mean-price-m2-output", "children"),
#     Output('amount-listings', 'children'),
#     Output('scatter-chart', 'figure'),
#     Input('housing-type-dropdown', 'value'),
#     Input('location-dropdown', 'value'),
#     Input('price-slider', 'value'),
#     Input('year-slider', 'value'),
#     Input('size-slider', 'value'),
#     Input('rooms-checklist', 'value'))
# def update_graph(housing_type_dropdown, location_dropdown,
#                  price_slider, year_slider,
#                  size_slider, rooms_checklist):

#     # Filter data by slider values
#     dff = df[df['Year'].between(year_slider[0], year_slider[1], inclusive="both")]
#     dff = dff[dff['Price'].between(price_slider[0], price_slider[1], inclusive="both")]
#     dff = dff[dff['Size'].between(size_slider[0], size_slider[1], inclusive="both")]

#     # Filter data by checklist selections
#     if rooms_checklist:
#         dff = dff[dff["Rooms"].isin(rooms_checklist)]

#     # Filter data by dropdown selections
#     if housing_type_dropdown:
#         dff = dff[dff["Type"].isin(housing_type_dropdown)]
#     if location_dropdown:
#         dff = dff[dff["Location"].isin(location_dropdown)]
#     figure={
#         "data": [
#             go.Scatter(
#                 x=dff["Size"],
#                 y=dff["Price"],
#                 mode="markers",
#             )],
#                 "layout": go.Layout(
#                     title="Price by Size plotting",
#                     xaxis={"title": "Size of the house"},
#                     yaxis={"title": "Price of the house"},
#                 )
#             }

#     # Key figures
#     dff_len = str(len(dff))
#     # Mean price (faulty equation, re-do by creating new column to df)
#     #mean_price_m2 = math.floor(dff.Price.sum() / dff.Size.sum())
#     mean_price_m2 = math.floor(dff["Price_M2"].mean())
#     med_year = math.floor(dff["Year"].median())
#     pop_housing = dff['Type'].value_counts().idxmax()
#     cheapest = dff['Price'].min()
#     most_expensive = dff["Price"].max()
#     mean_price = math.floor(dff["Price"].mean())

#     return mean_price, most_expensive, cheapest, pop_housing, med_year, mean_price_m2, dff_len, figure

if __name__ == "__main__":
    app.run_server(debug=True)

