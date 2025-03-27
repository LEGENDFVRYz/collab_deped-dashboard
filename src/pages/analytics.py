import dash
from dash import html

# Landing page
dash.register_page(__name__, path="/analytics")  

layout = html.Div([
    html.H1("Analytical Tool Page"),
])