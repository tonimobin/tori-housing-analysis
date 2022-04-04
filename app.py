from os import sep
from tokenize import group
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)
df = pd.read_csv('housing.csv', sep=',')

# Drop records without pricing info
df.dropna(subset=['Price', 'Rooms' ,'Size', 'Type', 'Year'], inplace=True)
df = df.astype({"Price":'int', "Year":'int', "Size":'int'}) 
df = df.sort_values(by=['Price'])

print(df)
#print("Key figures: \n")
#print("Average price per square meter: ", df['Price'].mean()/df['Size'].mean())
# fig = px.bar(df, x="Title", y="Price", barmode="group")

# app.layout = html.Div(children=[
#     html.H1(children='Tori.fi Housing Data Analysis'),

#     html.Div(children='''
#         Data!
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)

