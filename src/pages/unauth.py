import dash
from dash import html
from dash import dcc, html


# Landing page
dash.register_page(__name__, path="/unauthorized", suppress_callback_exceptions=True)  

layout = html.Div([
    html.Div(
        [
            html.Div("UNAUTHORIZED", className="response-tag"),
            html.Div("Access Denied, You do not have permission to view this page.", className="response-short"),
            html.Div("Please log in if you are a registered user!", className="response-reco")
        ]
    , className='content'),
], className='unauth container')