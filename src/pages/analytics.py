import dash
from dash import html

# src/pages/dashboard.py
from src.components.card import Card

# Landing page
dash.register_page(__name__, path="/analytics")  

# Main Page
layout = html.Div([
    ## -- Standard: Page Content Header
    html.Div([
        html.H1('Analytical Tools')
    ], className='page-header'),
    
    ## -- Content Container
    html.Div([
            ## -- Insert Here



    ], className='content')
], className='analytics-page container')