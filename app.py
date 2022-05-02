from turtle import width
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import math
import dash_extensions as de
from urllib.request import urlopen
import json

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
app = Dash(__name__)
app.title = "Housing analysis"
# Load the data, drop records with empty fields, convert num data to int and sort by price
df = pd.read_csv("full_data_cleaned_and_outliers_removed.csv", sep=",")
df.dropna(subset=["Price", "Rooms", "Size", "Type", "Year"], inplace=True)
df = df.astype({"Price": "int", "Year": "int", "Size": "int"})
df = df.sort_values(by=["Price"])

# Create a new column, "Price_M2", which calculates €/m² for every row
df["Price_M2"] = df.apply(lambda row: row.Price / row.Size, axis=1)

# Support variables for callback functions
housing_types = np.sort(df["Type"].unique())
locations = np.sort(df["Location"].unique())
rooms = np.sort(df["Rooms"].unique())

# Map
with urlopen("https://raw.githubusercontent.com/ufoe/d3js-geojson/master/Finland.json") as response:
    finland = json.load(response)

# Lottie
#lottie_url = "https://assets9.lottiefiles.com/private_files/lf30_p5tali1o.json"
lottie_url = "https://assets9.lottiefiles.com/packages/lf20_v7lgcy3m.json"
lottie_options = dict(loop=False, autoplay=True)

app.layout = html.Div(className="my-dash-app", children=[
    # Store
    dcc.Store(id="memory-output"),

    # Header
    html.Div(className="header row", children=[
        html.Div(id="lottie-wrapper", children=[de.Lottie(options=lottie_options,
                 width="75%", height="75%", url=lottie_url, className="header-lottie"), ]),
        #html.Span(id="title-p1", children="tori.fi"),
        html.Span(id="header-title", children=" Housing Analysis"),
    ]),

    # Options
    html.Div(className="flexbox-container row", children=[
        # Hoverable info panel
        html.Div(className="flexbox-item flexbox-item-1", children=[
            html.Div(className="inner", children=[
                html.Div(className="info-text tooltip", children=[
                    html.Span(className="info-text-i", children="i"),
                    html.Span(className="tooltiptext", children="""This application contains data from over 5000 housing listings from a Finnish peer-to-peer marketplace, Tori.fi. You can query the data with various options and the resulting data will be visualized below!""")])
            ])
        ]),
        html.Div(className="flexbox-item flexbox-item-2", children=[
        html.Label(children="Type:"),
            dcc.Dropdown(
                id="housing-type-dropdown",
                options=[{"label": x, "value": x} for x in housing_types],
                placeholder="House type",
                multi=True,
            ),
        ]),
        html.Div(className="flexbox-item flexbox-item-3", children=[
            html.Label("Location:"),
            dcc.Dropdown(
                id="location-dropdown",
                options=[{"label": x, "value": x} for x in locations],
                placeholder="Region",
                multi=True
            ),
        ]),
        html.Div(className="flexbox-item flexbox-item-4", children=[
            html.Label(id="price-label", children="Price:"),
            dcc.RangeSlider(
                id="price-slider",
                className="dbc",
                min=df.Price.min(),
                max=df.Price.max(),
                value=[df.Price.min(), df.Price.max()],
                step=5000,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
            ),
        ]),
        html.Div(className="flexbox-item flexbox-item-5", children=[
            html.Label(id="year-label", children="Year:"),
            dcc.RangeSlider(
                id="year-slider",
                className="dbc",
                min=df.Year.min(),
                max=df.Year.max(),
                value=[df.Year.min(), df.Year.max()],
                step=1,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ]),
        html.Div(className="flexbox-item flexbox-item-6", children=[
        html.Label(id="size-label", children="Size:"),
            dcc.RangeSlider(
                id="size-slider",
                className="dbc",
                min=df.Size.min(),
                max=df.Size.max(),
                value=[df.Size.min(), df.Size.max()],
                step=1,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ]),
        html.Div(className="flexbox-item flexbox-item-7", children=[
            html.Label("Rooms"),
            # dcc.Checklist(
            #     id="rooms-checklist",
            #     #className="dbc",
            #     options=[{"label": "" + x, "value": x} for x in rooms],
            #     #inline=False,
            #     #labelStyle={"display": "block"},
            #     #style={"overflow": "auto"},
            #     #labelClassName="mr-1"
            # ),
            dcc.Dropdown(
                id="rooms-dropdown",
                options=[{"label": x, "value": x} for x in rooms],
                placeholder="Room count",
                multi=True
            )
        ]),
    ]),
    html.Hr(className=""),
    html.Div(className="grid-container", children=[
        html.Div(className="grid-item grid-item-1", children=[
            html.Div(id="key-figures", className="keyfig-container")
        ]),
        # html.Div(className="grid-item grid-item-2", children=[
        #     html.P("Testi")
        # ]),
        html.Div(className="grid-item grid-item-3", children=[
            html.Div(id="listings-count", className="listcount")
        ]),
        html.Div(className="grid-item grid-item-4", children=[
            html.Span(className="median-em", children="Median €/m² by region"),
            dcc.Graph(id="price-m2-median-by-loc")
        ]),
        html.Div(className="grid-item grid-item-5", children=[
            html.Div(className="map-container", children=[
                dcc.Graph(id="count-map")
            ])
        ]),
        html.Div(className="grid-item grid-item-6", children=[
            html.P("Testi")
        ]),
        html.Div(className="grid-item grid-item-7", children=[

        ]),
        html.Div(className="grid-item grid-item-8", children=[
            html.Span("Distribution of types"),
            dcc.Graph(id="types-pie")
        ]),
        html.Div(className="grid-item grid-item-9", children=[
            html.Span("Distribution of rooms"),
            dcc.Graph(id="rooms-pie")
        ]),
    ]),
    html.Footer(className="footer row", children=[
        html.A(href="https://github.com/tonimobin/tori-housing-data-scrape-script", target="_blank", children=[
            html.Img(className="footer-icon footer-icon-gh", src=app.get_asset_url("github-logo-small.png")),
        ]),
        html.A(href="https://studies.helsinki.fi/courses/cur/hy-opt-cur-2122-f77f1644-2bfe-4693-a6bb-47596553c0c4/Interactive_Data_Visualization_Lectures",
        target="_blank", children=[
            html.Img(className="footer-icon footer-icon-hy", src=app.get_asset_url("hy-logo-small.png")),
        ]),
        html.A(href="https://www.tori.fi/",
        target="_blank", children=[
            html.Img(className="footer-icon footer-icon-hy", src=app.get_asset_url("tori-logo-small.png")),
        ]),
        #html.Img(className="footer-icon footer-icon-gh", src=app.get_asset_url("GitHub-Mark-32px.png")),
        #html.Span(""),
    ])
])
# app.layout = dbc.Container([
#     # Store
#     dcc.Store(id="memory-output"),
#     # Title
#     dbc.Row([
#         dbc.Col(
#             html.Div([
#             html.Span(id="title-p1", children="tori.fi"),
#             html.Span(id="title-p2", children=" Housing Analysis"),
#             html.Br(),
#         ], style={"width": "100%", "display": "flex", "alignItems": "start", "justifyContent": "start"}),
#         )
#     ]),
#     # Main data-graph and query options
#     dbc.Row([
#         # data-graph
#         dbc.Col(
#             html.Div(children=[
#                 # dcc.Graph(
#                 #     id="scatter-chart", className="dbc"
#                 # )]),
#                 ]),
#                 width={"size": 8}
#         ),
#         # query options
#         dbc.Col(
#             html.Div(children=[
#                 html.Label("Type:"),
#                 dcc.Dropdown(
#                     id="housing-type-dropdown",
#                     options=[{"label": x, "value": x} for x in housing_types],
#                     placeholder="Select housing type",
#                     multi=True,
#                 ),
#                 html.Label("Location:"),
#                 dcc.Dropdown(
#                     id="location-dropdown",
#                     options=[{"label": x, "value": x} for x in locations],
#                     placeholder="Select location",
#                     multi=True
#                 ),
#                 html.Label(id="price-label", children="Price:"),
#                 dcc.RangeSlider(
#                     id="price-slider",
#                     className="dbc",
#                     min=df.Price.min(),
#                     max=df.Price.max(),
#                     value=[df.Price.min(), df.Price.max()],
#                     step=5000,
#                     marks=None,
#                     tooltip={"placement": "bottom", "always_visible": False}
#                 ),
#                 html.Label(id="year-label", children="Year:"),
#                 dcc.RangeSlider(
#                     id="year-slider",
#                     className="dbc",
#                     min=df.Year.min(),
#                     max=df.Year.max(),
#                     value=[df.Year.min(), df.Year.max()],
#                     step=1,
#                     marks=None,
#                     tooltip={"placement": "bottom", "always_visible": False}
#                 ),
#                 html.Label(id="size-label", children="Size:"),
#                 dcc.RangeSlider(
#                     id="size-slider",
#                     className="dbc",
#                     min=df.Size.min(),
#                     max=df.Size.max(),
#                     value=[df.Size.min(), df.Size.max()],
#                     step=1,
#                     marks=None,
#                     tooltip={"placement": "bottom", "always_visible": False}
#                 ),
#                 html.Label("Rooms"),
#                 dcc.Checklist(
#                     id="rooms-checklist",
#                     className="dbc",
#                     options=[{"label": " " + x, "value": x} for x in rooms],
#                     inline=False,
#                     labelStyle={"display": "block"},
#                     style={"width": 200, "overflow": "auto"},
#                     labelClassName="mr-1"
#                 ),
#             ], className="graph__container"),
#             width={"size": 3, "offset": 1}
#         ),
#     ], justify="around"),
#     # *** Animation demo ***
#     html.Div(id="test-div", className="test-div", **{"data-target": 999}, children="Animated number demo: "),
#     # Key figures
#     dbc.Row([
#         dbc.Col(children=[
#             html.Div(id="key-figures"),
#         ])
#     ]),

#     # Pie charts
#     dbc.Row([
#         html.H4("Distributions of listings by room and type"),
#         dbc.Col(
#             dcc.Graph(id="rooms-pie"), width="4"
#         ),
#         dbc.Col(    
#             dcc.Graph(id="types-pie"), width="4"
#         )
#     ], justify="start"),
#     dbc.Row([
#         dbc.Col(
#             dcc.Graph(id="avg-prices-by-size", className="dbc"), width=4
#             #html.Div(id="pandas-testing")
#         ),
#         dbc.Col(
#             dcc.Graph(id="price-m2-median-by-loc", className="dbc"), width=4
#         )
#     ]),
#     html.H1("******************* TEST ZONE ********************"),
#     html.Div(id="test-chart", children=[
#         dcc.Graph(id="scatter-chart")
#     ])
# ], fluid=True, className="dbc")

# Handle updates to data when user makes different queries
@app.callback(
    Output("memory-output", "data"),
    Input('housing-type-dropdown', 'value'),
    Input('location-dropdown', 'value'),
    Input('price-slider', 'value'),
    Input('year-slider', 'value'),
    Input('size-slider', 'value'),
    Input('rooms-dropdown', 'value'))
def filter_data(housing_type_dropdown, location_dropdown, price_slider, year_slider,
                size_slider, rooms_dropdown):

    # Filter data by slider values
    dff = df[df['Year'].between(year_slider[0], year_slider[1], inclusive="both")]
    dff = dff[dff['Price'].between(price_slider[0], price_slider[1], inclusive="both")]
    dff = dff[dff['Size'].between(size_slider[0], size_slider[1], inclusive="both")]

    # Filter data by checklist selections
    if rooms_dropdown:
        dff = dff[dff["Rooms"].isin(rooms_dropdown)]

    # Filter data by dropdown selections
    if housing_type_dropdown:
        dff = dff[dff["Type"].isin(housing_type_dropdown)]
    if location_dropdown:
        dff = dff[dff["Location"].isin(location_dropdown)]

    return dff.to_dict("records")

# # Update median price by size (horizontal bar chart)
@app.callback(Output("price-m2-median-by-loc", "figure"), Input("memory-output", "data"))
def update_price_horizontal(data):
    if data is None:
        raise PreventUpdate
    df = pd.DataFrame(data)
    # dff = df["Location"].value_counts().reset_index()
    # dff.columns = ["Location", "Counts"]
    location_grp = df.groupby("Location")
    dff = location_grp["Price_M2"].median().round(0)
    dff = dff.reset_index()
    dff.columns = ["Location", "€/m²"]
    dff = dff.sort_values("€/m²", ascending=False)
    figure = px.bar(dff, x="€/m²", y="Location", orientation="h", labels={"Location": "", "€/m²": ""}, text="€/m²")
    figure.update_layout({"plot_bgcolor": "rgba(0,0,0,0)"}), 
    # title= {"text": "Median €/m² by location", "x": 0.01, "xanchor": "left", "font_family": "Fira Code", "font_size": 18})
    figure.update_traces(marker_color="#3B6E80", textposition="outside", cliponaxis=False)
    return figure

# # Update count of listings by location (horizontal bar chart)
# @app.callback(Output("avg-prices-by-size", "figure"), Input("memory-output", "data"))
# def update_count_horizontal(data):
#     if data is None:
#         raise PreventUpdate
#     df = pd.DataFrame(data)
#     dff = df["Location"].value_counts().reset_index()
#     dff.columns = ["Location", "Counts"]
#     figure = px.bar(dff, x="Counts", y="Location", orientation="h", labels={"Location": "", "Counts": ""})
#     figure.update_layout({"plot_bgcolor": "rgba(0,0,0,0)"}), 
#     title= {"text": "", "x": 0.01, "xanchor": "left", "font_family": "Fira Code", "font_size": 18})
#     figure.update_traces(marker_color="#679F96")
#     return figure

# # Update scatter chart
# @app.callback(Output("scatter-chart", "figure"), Input("memory-output", "data"))
# def update_scatter(data):
#     if data is None:
#         raise PreventUpdate
#     df = pd.DataFrame(data)
#     try:
#         figure = {
#                 "data": [
#                     go.Scatter(
#                         x=df["Size"],
#                         y=df["Price"],
#                         mode="markers",
#                         marker=dict(
#                             color="#76A1EF",
#                             size=4,
#                             opacity=0.8,
#                             # line=dict(color='Black', width=1)
#                         ),
#                     )],
#                 "layout": go.Layout(
#                     title= {"text": "Available listings", "x": 0.01, "xanchor": "left", "font_family": "Fira Code", "font_size": 26},
#                     xaxis={"title": "Size m²", "showgrid" : False},
#                     yaxis={"title": "Price €", "showgrid" : False},
#                 )
#             }
#     # If no listings are found with given features, return a message informing the user.
#     except(KeyError):
#         figure = {
#             "layout": {"xaxis": { "visible": "false"},
#                 "yaxis": { "visible": "false" },
#                 "annotations": [
#                     {"text": "No available listings with given features.", "xref": "paper", "yref": "paper",
#                         "showarrow": "false", "font": { "size": 28 }
#                     }
#                 ]
#             }
#         }
#         return figure
#     return figure

# Create & update keyfigures
@app.callback(Output("key-figures", "children"), Input("memory-output", "data"))
def update_keyfig(data):
    if data is None:
        raise PreventUpdate
    df = pd.DataFrame(data)
    if len(df) > 0:
        return [
            html.Div(className="keyfig-row keyfig-row-1", children=[
                    html.Div(className="labels-item", children="Mean size"),
                    html.Div(className="labels-item", children="Mean €/m²"),
                    html.Div(className="labels-item", children="Median year of construction"),
                    html.Div(className="values-item", children=f"{math.floor(df.Size.mean())} m²"),
                    html.Div(className="values-item", children="{:,} €".format(math.floor(df.Price.sum() / df.Size.sum())).replace(",", " ")),
                    html.Div(className="values-item", children=f"{math.floor(df.Year.median())}")
            ]),
            html.Div(className="keyfig-row keyfig-row-2", children=[
                    html.Div(className="labels-item", children="Cheapest listing"),
                    html.Div(className="labels-item", children="Most expensive"),
                    html.Div(className="labels-item", children="Mean price"),
                    html.Div(className="values-item", children="{:,} €".format(df.Price.min()).replace(",", " ")),
                    html.Div(className="values-item", children="{:,} €".format(df.Price.max()).replace(",", " ")),
                    html.Div(className="values-item", children="{:,} €".format(math.floor(df.Price.mean())).replace(",", " ")),
            ])
        ]
    else:
        return [
            html.Div(
                html.P("No listings with given options.")
            )
        ]

# Update listings counts
@app.callback(Output("listings-count", "children"), Input("memory-output", "data"))
def update_listings_count(data):
    if data is None:
        raise PreventUpdate
    df = pd.DataFrame(data)
    if len(df) < 0:
        return [
            html.Div("ainaki 432424")
        ]
    else:
        return [
            html.Div(className="listcount-title", children=
"Amount of listings"
            ),
            html.Div(className="listcount-num", children=[
                html.Div(f"{len(df)}")
            ])
        ]

# Map callback
@app.callback(Output("count-map", "figure"), Input("memory-output", "data"))
def update_map(data):
    if data is None:
        raise PreventUpdate
    df = pd.DataFrame(data)
    # create a new df with location and count of listings in the location
    loc_counts = df["Location"].value_counts().reset_index()
    loc_counts.columns = ["Location", "Count"]
    locations = ["Helsinki", "Lappi"]
    figure = px.choropleth(loc_counts, geojson=finland, locations="Location", color="Count", color_continuous_scale="Greens", range_color=(0,12), scope="europe")
    figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return figure
# # Update key figures
# @app.callback(Output("key-figures", "children"),
#               Input("memory-output", "data"))
# def update_keyfigs(data):
#     if data is None:
#         raise PreventUpdate
#     df = pd.DataFrame(data)
#     if len(df) > 0:
#         return [
#             html.H4(id="key-figs-title", children="Key figures"),
#             html.Div(id="key-figs", children=[
#                 dbc.Row([
#                     dbc.Row([
#                         dbc.Col(html.P(id="key-fig", children="Amount of listings", className="text-center"), width=2),
#                         dbc.Col(html.P(id="key-fig", children="Mean €/m²", className="text-center"), width=2),
#                         dbc.Col(html.P(id="key-fig", children="Median year of construction", className="text-center"), width=2)
#                     ], justify="start"),
#                     dbc.Row([
#                         dbc.Col(html.P(f"{len(df)}", className="text-center"), width=2),
#                         dbc.Col(html.P(children="{:,} €".format(math.floor(df.Price.sum() / df.Size.sum())).replace(",", " "), className="text-center"), width=2),
#                         dbc.Col(html.P(f"{math.floor(df.Year.median())}", className="text-center"), width=2)
#                     ], justify="start"),
#                 ], justify="start"),
#                 dbc.Row([
#                     dbc.Row([
#                         dbc.Col(html.P(id="key-fig", children="Cheapeast listing", className="text-center"), width=2),
#                         dbc.Col(html.P(id="key-fig", children="Most expensive", className="text-center"), width=2),
#                         dbc.Col(html.P(id="key-fig", children="Mean price", className="text-center"), width=2)
#                     ]),
#                     dbc.Row([
#                         dbc.Col(html.P(children="{:,} €".format(df.Price.min()).replace(",", " "), className="text-center"), width=2),
#                         dbc.Col(html.P(children="{:,} €".format(df.Price.max()).replace(",", " "), className="text-center"), width=2),
#                         dbc.Col(html.P(children="{:,} €".format(math.floor(df.Price.mean())).replace(",", " "), className="text-center"), width=2)
#                     ]),
#                 ], justify="start")
#             ]),
#         ]
#     else:
#         return [
#             html.Div(
#                 html.P("-")
#             )
#         ]


#Update rooms pie chart (to:do prevent empty dataset error for this & type)
@app.callback(Output("rooms-pie", "figure"),
              Input("memory-output", "data"))
def update_rooms_pie(data):
    color_map={"1H":"#0B2027","2H":"#40798C","3H":"#70A9A1","4H":"#CFD7C7","5H":"#F6F1D1","6H":"E9E0A6"},
    colors = ["#0B2027", "#40798C", "#70A9A1", "#CFD7C7", "#F6F1D1", "E9E0A6"]
    if data is None:
         raise PreventUpdate
    df = pd.DataFrame(data)
    rooms = df["Rooms"].unique()
    room_count = df["Rooms"].value_counts(sort=False).array
    figure = go.Figure(data=[go.Pie(labels=rooms, values=room_count)], layout=go.Layout(margin={"t" : 0, "b" : 0}, height=200))
    figure.update_traces(
        hoverinfo="value", 
        textinfo="label+percent",
        marker=dict(colors = colors), 
        hole=0.5, 
        textposition="outside",
        
    )
    figure.update(layout_showlegend=False)
    return figure
    

# # Update types pie chart
@app.callback(Output("types-pie", "figure"),
              Input("memory-output", "data"))
def update_types_pie(data):
    colors = ["#0B2027", "#40798C", "#70A9A1", "#CFD7C7", "#F6F1D1", "E9E0A6"]
    if data is None:
         raise PreventUpdate
    df = pd.DataFrame(data)
    types = df["Type"].unique()
    type_count = df["Type"].value_counts(sort=False).array
    figure = go.Figure(data=[go.Pie(labels=types, values=type_count)], 
    layout=go.Layout(margin={"t" : 0, "b" : 0}, height=200))
    figure.update_traces(
        hoverinfo="value", 
        textinfo="label+percent", 
        marker=dict(colors = colors), 
        hole=0.5, 
        textposition="outside",
    )
    figure.update(layout_showlegend=False)
    return figure
if __name__ == "__main__":
    app.run_server(debug=True)

