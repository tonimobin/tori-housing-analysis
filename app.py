from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import math
import dash_extensions as de
import dash_leaflet as dl
from urllib.request import urlopen
from dash_extensions.javascript import Namespace, arrow_function
import geopandas as gpd
import json

app = Dash(__name__)
app.title = "Housing analysis"

# Load the data, drop records with empty fields, convert num data to int and sort by price
df = pd.read_csv("full_data_cleaned_and_outliers_removed.csv", sep=",")
df.dropna(subset=["Price", "Rooms", "Size", "Type", "Year"], inplace=True)
# Ahvenanmaa has to be dropped, because the geojson for the map doesn't contain it and thus can't visualize it
df.drop(df[df["Location"] == "Ahvenanmaa"].index, inplace=True)
df = df.astype({"Price": "int", "Year": "int", "Size": "int"})
df = df.sort_values(by=["Price"])

# Translate house types & regions from Finnish to English
df["Type"] = df["Type"].str.replace("Kerrostalo", "Apartment").replace("Omakotitalo", "House").replace("Rivitalo", "Rowhouse").replace("Luhtitalo", "Loft")
df["Rooms"] = df["Rooms"].str.replace("1H", "1R").replace("2H", "2R").replace("3H", "3R").replace("4H", "4R").replace("5H", "5R").replace("6H", "6R")
# The regions are translated manually, because of the differences between tori and geojson naming conventions
df = df.replace({"Location" : {"Etelä-Karjala" : "South Karelia", "Etelä-Pohjanmaa" : "Southern Ostrobothnia", "Etelä-Savo" : "Southern Savonia", 
"Kainuu" : "Kainuu", "Kanta-Häme" : "Tavastia Proper", "Keski-Pohjanmaa" : "Central Ostrobothnia", "Keski-Suomi" : "Central Finland",
 "Kymenlaakso" : "Kymenlaakso", "Lappi" : "Lapland", "Pirkanmaa" : "Pirkanmaa", "Pohjanmaa" : "Ostrobothnia", "Pohjois-Karjala" : "North Karelia", 
 "Pohjois-Pohjanmaa" : "Northern Ostrobothnia", "Pohjois-Savo" : "Northern Savonia", "Päijät-Häme" : "Päijät-Häme", "Satakunta" : "Satakunta",
 "Uusimaa" : "Uusimaa", "Varsinais-Suomi" : "Finland Proper"}})
# Create a new column, "Price_M2", which calculates €/m² for every row
df["Price_M2"] = df.apply(lambda row: row.Price / row.Size, axis=1)


# Support variables for callback functions
housing_types = np.sort(df["Type"].unique())
locations = np.sort(df["Location"].unique())
rooms = np.sort(df["Rooms"].unique())

# Map
finland_url = "https://raw.githubusercontent.com/ufoe/d3js-geojson/master/Finland.json"
with urlopen("https://raw.githubusercontent.com/ufoe/d3js-geojson/master/Finland.json") as response:
    finland = json.load(response)

# Lottie
lottie_url = "https://assets9.lottiefiles.com/packages/lf20_v7lgcy3m.json"
lottie_options = dict(loop=False, autoplay=True)

# Dataset figures
ttl_median_size = math.floor(df.Size.mean())
ttl_median_euro_m2 = math.floor(df["Price_M2"].median())
ttl_median_year = math.floor(df.Year.median())
ttl_cheapest_listing = df.Price.min()
ttl_most_expensive_listing = df.Price.max()
ttl_median_price = df.Price.median()

# Support functions
def percentage(part, whole):
  percentage = math.floor(100 * float(part)/float(whole))
  percentage = percentage - 100
  if percentage < 0:
    return html.Div(className="perc-neg", children=f"{percentage} %")
  if percentage > 0:    
    return html.Div(className="perc-pos", children=f"+{percentage} %")
  if percentage == 0:
    return f"-"

def year_comparison(year):
    diff = year - ttl_median_year
    if diff > 0:
        return html.Div(className="year-test-pos", children=f"+{diff}")
    if diff < 0:
        return html.Div(className="year-test-neg", children=f"{diff}")
    if diff == 0:
        return f"-"

app.layout = html.Div(className="my-dash-app", children=[
    # Store
    dcc.Store(id="memory-output"),

    # Header
    html.Div(className="header row", children=[
        html.Div(id="lottie-wrapper", children=[de.Lottie(options=lottie_options,
                 width="75%", height="75%", url=lottie_url, className="header-lottie"), ]),
        html.Span(id="header-title", children=" Housing Analysis"),
    ]),

    # Options
    html.Div(className="flexbox-container row", children=[
        # Hoverable info panel
        html.Div(className="flexbox-item flexbox-item-1", children=[
            html.Div(className="info-tooltip", children=[
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
            html.Label(id="price-label", children="Price (€):"),
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
        html.Label(id="size-label", children="Size (m²):"),
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
        #     html.P("")
        # ]),
        html.Div(className="grid-item grid-item-3", children=[
            html.Div(id="listings-count", className="listcount")
        ]),
        html.Div(className="grid-item grid-item-4", children=[
            html.Div(className="grid-title", children="Median €/m² by region"),
            dcc.Graph(id="price-m2-median-by-loc")
        ]),
        html.Div(className="grid-item grid-item-5", children=[
            html.Div(className="map-container", children=[
                # dcc.Graph(id="count-map")
                html.Div(id="count-map")
            ])
        ]),
        html.Div(className="grid-item grid-item-6", children=[
            html.P("")
        ]),
        html.Div(className="grid-item grid-item-7", children=[
            html.Div(className="grid-title", children="Price distribution"),
            dcc.Graph(id="price-distrib")
        ]),
        html.Div(className="grid-item grid-item-8", children=[
            html.Div(className="grid-title", children="Distribution of types"),
            dcc.Graph(id="types-pie")
        ]),
        html.Div(className="grid-item grid-item-9", children=[
            html.Div(className="grid-title", children="Distribution of rooms"),
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
    if len(df) > 0:
        location_grp = df.groupby("Location")
        dff = location_grp["Price_M2"].median().round(0)
        dff = dff.reset_index()
        dff.columns = ["Location", "€/m²"]
        dff = dff.sort_values("€/m²", ascending=False)
        figure = px.bar(dff, x="€/m²", y="Location", orientation="h", labels={"Location": "", "€/m²": ""}, text="€/m²")
        figure.update_layout({"plot_bgcolor": "rgba(0,0,0,0)"}), 
        figure.update_traces(marker_color="#58B505", textposition="outside", cliponaxis=False, texttemplate='%{text} €')
        figure.update_xaxes(showticklabels=False)
        return figure
    else:
        figure = go.Figure(data=[])
        figure.update_layout({"plot_bgcolor": "rgba(0,0,0,0)"})
        figure.update_xaxes(visible=False)
        figure.update_yaxes(visible=False)
        return figure

# Create & update keyfigures
@app.callback(Output("key-figures", "children"), Input("memory-output", "data"))
def update_keyfig(data):
    if data is None:
        raise PreventUpdate
    df = pd.DataFrame(data)
    if len(df) > 0:
        median_size = math.floor(df.Size.mean())
        # median_euro_m2 = math.floor(df.Price.sum() / df.Size.sum())
        median_euro_m2 = math.floor(df["Price_M2"].median())
        median_year = math.floor(df.Year.median())
        cheapest_listing = df.Price.min()
        most_expensive_listing = df.Price.max()
        median_price = math.floor(df.Price.median())
        return [
            html.Div(className="keyfig-tooltip", children=[
                html.Div(className="info-text tooltip", children=[
                    html.Span(className="info-text-i", children="*"),
                    html.Span(className="tooltiptext", children="""
                    Percentages are compared to the complete dataset values.
                    """)])
            ]),
            html.Div(className="keyfig-row keyfig-row-1", children=[
                    html.Div(className="labels-item", children="Mean size"),
                    html.Div(className="labels-item", children="Median €/m²"),
                    html.Div(className="labels-item", children="Median year of construction"),
                    html.Div(className="values-item", children=f"{median_size} m²"),
                    html.Div(className="values-item", children="{:,} €".format(median_euro_m2).replace(",", " ")),
                    html.Div(className="values-item", children=f"{median_year}"),
                    html.Div(className="values-item keyfig-percent", children=[percentage(median_size, ttl_median_size)]),
                    html.Div(className="values-item keyfig-percent", children=[percentage(median_euro_m2, ttl_median_euro_m2)]),
                    html.Div(className="values-item keyfig-percent", children=[year_comparison(median_year)])
            ]),
            html.Div(className="keyfig-row keyfig-row-2", children=[
                    html.Div(className="labels-item", children="Cheapest listing"),
                    html.Div(className="labels-item", children="Most expensive"),
                    html.Div(className="labels-item", children="Median price"),
                    html.Div(className="values-item", children="{:,} €".format(cheapest_listing).replace(",", " ")),
                    html.Div(className="values-item", children="{:,} €".format(most_expensive_listing).replace(",", " ")),
                    html.Div(className="values-item", children="{:,} €".format(median_price).replace(",", " ")),
                    html.Div(className="values-item keyfig-percent", children=[percentage(cheapest_listing, ttl_cheapest_listing)]),
                    html.Div(className="values-item keyfig-percent", children=[percentage(most_expensive_listing, ttl_most_expensive_listing)]),
                    html.Div(className="values-item keyfig-percent", children=[percentage(median_price, ttl_median_price)])
            ])
        ]
    else:
        return [
            html.Div(
                html.P(className="empty-data-error", children="No listings with given options.")
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
            html.Div("No data available.")
        ]
    else:
        return [
            html.Div(className="listcount-title", children="Amount of listings"),
            html.Div(className="listcount-num", children=[
                html.Div(f"{len(df)}")
            ])
        ]

# Map callback
@app.callback(Output("count-map", "children"), Input("memory-output", "data"))
def update_map(data):
    if data is None:
        raise PreventUpdate
    df = pd.DataFrame(data)
    if len(df) > 0:
        loc_counts = df["Location"].value_counts().reset_index()
        loc_counts.columns = ["Location", "Count"]
        ns = Namespace("myNamespace", "mySubNamespace")
        hover_style = dict(weight=6, fillColor="#57cf36", fillOpacity=0.3)
        geo_df = gpd.read_file(finland_url)
        region_names = geo_df.copy(deep=True)
        region_names["tooltip"] = geo_df.name + "<br>" + f"Listings: {len(df)}" + "<br>" + f"Median €/m²: "
        geoj = dl.GeoJSON(data=json.loads(region_names.to_json()), hoverStyle=arrow_function(hover_style), options=dict(pointToLayer=ns("pointToLayer"), style=dict(color="#58B505")))
        return [
            html.Div(className="map-title", children="Location reference & data based on full dataset"),
            dl.Map([geoj, dl.TileLayer()], center=(61.5, 25), zoom=6, style={"height" : "310px"})
            
        ]
    else:
        return html.Div("Location reference & data based on full dataset")
# Update price distribution box plot
@app.callback(Output("price-distrib", "figure"), Input("memory-output", "data"))
def update_box_plot(data):
    if data is None:
        raise PreventUpdate
    df = pd.DataFrame(data)
    if len(df) > 0:
        prices = df["Price"]
        figure = go.Figure()
        figure.add_trace(go.Box(y = prices, marker_color="#58B505", boxpoints=False, name="Price"))
        figure.update_layout({"plot_bgcolor": "rgba(0,0,0,0)"})
        return figure
    else:
        figure = go.Figure(data=[])
        figure.update_layout({"plot_bgcolor": "rgba(0,0,0,0)"})
        figure.update_xaxes(visible=False)
        figure.update_yaxes(visible=False)
        return figure

# Update types pie chart
@app.callback(Output("types-pie", "figure"),
              Input("memory-output", "data"))
def update_types_pie(data):
    colors = ["#0B2027", "#40798C", "#70A9A1", "#CFD7C7", "#F6F1D1", "E9E0A6"]
    if data is None:
         raise PreventUpdate
    df = pd.DataFrame(data)
    if len(df) > 0:
        types = df["Type"].unique()
        type_count = df["Type"].value_counts(sort=False).array
        figure = go.Figure(data=[go.Pie(labels=types, values=type_count)], 
        layout=go.Layout(margin={"t" : 0, "b" : 0}, height=250))
        figure.update_traces(
            hoverinfo="value", 
            textinfo="label+percent", 
            marker=dict(colors = colors), 
            hole=0.5, 
            textposition="outside",
        )
        figure.update(layout_showlegend=False)
        return figure
    else:
        figure = go.Figure(data=[])
        figure.update_layout({"plot_bgcolor": "rgba(0,0,0,0)"})
        figure.update_xaxes(visible=False)
        figure.update_yaxes(visible=False)
        return figure

# Update rooms pie chart
@app.callback(Output("rooms-pie", "figure"),
              Input("memory-output", "data"))
def update_rooms_pie(data):
    color_map={"1H":"#0B2027","2H":"#40798C","3H":"#70A9A1","4H":"#CFD7C7","5H":"#F6F1D1","6H":"E9E0A6"},
    colors = ["#0B2027", "#40798C", "#70A9A1", "#CFD7C7", "#F6F1D1", "E9E0A6"]
    if data is None:
         raise PreventUpdate
    df = pd.DataFrame(data)
    if len(df) > 0:
        rooms = df["Rooms"].unique()
        room_count = df["Rooms"].value_counts(sort=False).array
        figure = go.Figure(data=[go.Pie(labels=rooms, values=room_count)], layout=go.Layout(margin={"t" : 0, "b" : 0}, height=250))
        figure.update_traces(
            hoverinfo="value", 
            textinfo="label+percent",
            marker=dict(colors = colors), 
            hole=0.5, 
            textposition="outside",
            
        )
        figure.update(layout_showlegend=False)
        return figure
    else:
        figure = go.Figure(data=[])
        figure.update_layout({"plot_bgcolor": "rgba(0,0,0,0)"})
        figure.update_xaxes(visible=False)
        figure.update_yaxes(visible=False)
        return figure
    
if __name__ == "__main__":
    app.run_server(debug=True)

