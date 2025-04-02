import dash
from dash import html

# src/pages/dashboard.py
from src.components.card import Card

# Landing page
dash.register_page(__name__, path="/")  

layout = html.Div([
    ## -- Standard: Page Content Header
    html.Div([
        html.H1('Overview:')
    ], className='page-header'),
    
    html.Div([
            ## -- Main Part
    html.Div([
        html.Div([
            ## --> Sub layer
            html.Div([Card()], className='area-1'),
            html.Div([Card()], className='area-2'),
            html.Div([Card()], className='area-3'),
        ], className='layer-1'),
        html.Div([
            Card()
        ], className='layer-2')
    ], className='main-section'),
    
    ## -- Side Part
    html.Div([
        html.Div([
                Card([
                    html.H5()
                ])
            ], className='layer-1'),
            
            html.Div([
                    Card()
                ], className='layer-2')
        ], className='side-section')
    ], className='content')
], className='home-page container')