import dash
from dash import html

# src/pages/dashboard.py
from src.components.card import Card

# Landing page
dash.register_page(__name__, path="/school-level")  

# Main Page
layout = html.Div([
    ## -- Standard: Page Content Header
    html.Div([
        html.H1('School-Level Insights')
    ], className='page-header'),
    
    html.Div([
        html.Div([
            html.Span(["Sample"]),
        ], className='gray-1'),
        html.Div([
            html.Span(["EX"]),
        ], className='gray-2'),
        html.Div([
            html.Img(src="/assets/images/icons_navigation/filter.svg")
        ], className="filter-icon")
    ], className='buttons-level'),
    
    html.Div([
        html.Div([
            html.Div([
                html.Div([Card()], className='card-1'),
            ], className='si-layer-1'),
            html.Div([
                html.Div([Card()], className='card-2'),
                html.Div([Card()], className='card-3'),
            ], className='si-layer-2')
        ], className='main-content'),
        
        html.Div([
            html.Div([
                html.Div([Card()], className='card-4'),
            ], className='si-layer-1'),
        ], className='side-content')
    ], className='content')
], className='school-level-page container')