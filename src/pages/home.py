import dash
from dash import html

# Landing page
dash.register_page(__name__, path="/")  

layout = html.Div([
    html.Div([html.H1("Homies Page")], className='home-page')
])