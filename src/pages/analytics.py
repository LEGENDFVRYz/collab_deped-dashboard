import dash
from dash import html, dcc

# src/pages/dashboard.py
from src.components.card import Card

# Landing page
dash.register_page(__name__, path="/analytics")  

# Main Page
layout = html.Div([
    ## -- Standard: Page Content Header
    html.Div([
        html.Div([
            html.Div([
                html.H1('Analytical Tools')
            ], className='page-header'),
            
            html.Div([
                html.Div([
                    html.Img(src="/assets/images/icons_navigation/filter.svg")
                ], className="search-icon"),
                dcc.Input(
                    id='input-text',
                    type='text',
                    placeholder='Search here . . .',
                    className="search-input"
                ),
                html.Div(["X"], className="clear-button")
            ], className='search-bar'),
            
            html.Div([
                html.Div(["Sample"], className='gray-1'),
                html.Div([
                    html.Img(src="/assets/images/icons_navigation/filter.svg")
                ], className="filter-icon"),
            ], className='buttons-level'),
            
            html.Div([
                Card()
            ], className='card-1'),
            
        ], className='left-content'),
        
        html.Div([
            html.Div([
                html.Div(['Option 1'], className='option-1'),
                html.Div(['Option 2'], className='option'),
                html.Div(['Option 3'], className='option'),
                html.Div(['Option 4'], className='option'),
            ], className='tab-options'),
            
            html.Div([
                Card()
            ], className='content-card')
            
        ], className='right-content'),
    ], className='content-section'),
], className='analytics-page container')