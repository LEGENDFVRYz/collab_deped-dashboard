import dash
from dash import html

# Landing page
dash.register_page(__name__, path="/school-level")  

layout = html.Div([
    html.H1("School-Level Insights Page"),
])