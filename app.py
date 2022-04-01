from os import sep
from tokenize import group
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)
df = pd.read_csv('housing.csv', sep=',')

# Drop records without pricing info
df.dropna(subset=['Price', 'Size', 'Type', 'Year'], inplace=True)
df = df.astype({"Price":'int', "Year":'int'}) 
df = df.sort_values(by=['Price'])

fig = px.bar(df, x="Title", y="Price", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Tori housing data'),

    html.Div(children='''
        Data!
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

