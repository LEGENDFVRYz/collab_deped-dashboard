import plotly.express as px
import dash
from dash import Dash, dcc, html, Output, Input
from src.server import server
import pandas as pd
# from src.data import dataframe

# Callbacks
from src.utils import activeTab_callback
# from src.utils import filter_menu_callback

# Main Applications
app = Dash(__name__, server=server, use_pages=True, suppress_callback_exceptions=True)


app.layout = html.Div(
    children=[
        dcc.Store(id="active-tab", data="", storage_type="local"),  # Store clicked tab
        dcc.Location(id="url"),  # Gets the current pathname
        
        # Navigation style
        html.Div([
            html.Div([
                # DataDash Brand Mark
                html.H2("DATA DASHBOARD")    
            ], className='brand-section'),
            
            html.Div([
                # Navigation Options
                html.Div([
                    html.Div([
                        html.Div([], className='indicator'),
                        dcc.Link([
                                html.Div([html.Img(src="/assets/images/icons_navigation/overview-light.svg")], className='light icon'),
                                html.Div([html.Img(src="/assets/images/icons_navigation/overview-green.svg")], className='dark icon'),
                                html.Div(['Overview'], className='text')
                            ], href="/", className='overview nav-btn')
                    ], className='main-tab')
                ], id='nav-1', className='item-ctn'),
                
                html.Div([
                    html.Div([
                        html.Div([], className='indicator'),
                        dcc.Link([
                                html.Div([html.Img(src="/assets/images/icons_navigation/pie-chart-fill.svg")], className='light icon'),
                                html.Div([html.Img(src="/assets/images/icons_navigation/pie-chart-2-fill.svg")], className='dark icon'),
                                html.Div(['Analytical Tools'], className='text')
                            ], href='/analytics', className='overview nav-btn'),
                    ], className='main-tab'),
                    html.Div([
                        html.Div([
                                html.Div([
                                        html.Img(src="/assets/images/icons_navigation/nav-tab-map-icon.svg"),
                                        html.A("Location")
                                    ], id='location', className='tab-btn'),
                                html.Div([
                                        html.Img(src="/assets/images/icons_navigation/nav-tab-map-icon.svg"),
                                        html.A("Senior High")
                                    ], id='senior-high', className='tab-btn'),
                                html.Div([
                                        html.Img(src="/assets/images/icons_navigation/nav-tab-map-icon.svg"),
                                        html.A("Subclassification")
                                    ], id='subclass', className='tab-btn'),
                                html.Div([
                                        html.Img(src="/assets/images/icons_navigation/nav-tab-map-icon.svg"),
                                        html.A("Offering")
                                    ], id='offering', className='tab-btn'),
                            ], className='tabs-menu-ctn')    
                        ], className='tabs-menu')
                    
                ], id='nav-2', className='item-ctn'),
                
                html.Div([
                    html.Div([
                        html.Div([], className='indicator'),
                        dcc.Link([
                                html.Div([html.Img(src="/assets/images/icons_navigation/pie-chart-fill.svg")], className='light icon'),
                                html.Div([html.Img(src="/assets/images/icons_navigation/pie-chart-2-fill.svg")], className='dark icon'),
                                html.Div(['School-level'], className='text')
                            ], href='/school-level', className='overview nav-btn'),
                    ], className='main-tab'),
                    html.Div([
                            html.Div([
                                html.Div([
                                        html.Img(src="/assets/images/icons_navigation/nav-tab-map-icon.svg"),
                                        html.A("Analysis")
                                    ], className='tab-btn'),
                                html.Div([
                                        html.Img(src="/assets/images/icons_navigation/nav-tab-map-icon.svg"),
                                        html.A("Comparizon")
                                    ], className='tab-btn'),
                            ], className='tabs-menu-ctn')  
                        ], className='tabs-menu')
                ], id='nav-3', className='item-ctn'),
            ], className='menu-section'),
            
            html.Div([
                # Account Settings
                html.Div([
                    html.Div([], className='indicator'),
                    dcc.Link([
                            html.Div([html.Img(src="/assets/images/icons_navigation/pie-chart-fill.svg")], className='light icon'),
                            html.Div([html.Img(src="/assets/images/icons_navigation/pie-chart-2-fill.svg")], className='dark icon'),
                            html.Div(['Updates'], className='text')
                        ], href="/updates", className='overview nav-btn')
                ], id='opt-1', className='item-ctn'),
                
                html.Div([
                    # html.Div([], className='indicator'),
                    # dcc.Link([
                    #         html.Div([html.Img(src="/assets/images/icons_navigation/pie-chart-fill.svg")], className='light icon'),
                    #         html.Div([html.Img(src="/assets/images/icons_navigation/pie-chart-2-fill.svg")], className='dark icon'),
                    #         html.Div(['Help'], className='text')
                    #     ], href='/help', className='overview nav-btn'),
                ], id='opt-2', className='item-ctn'),
                
                html.Div([
                    html.Div([], className='indicator'),
                    dcc.Link([
                            html.Div([html.Img(src="/assets/images/icons_navigation/pie-chart-fill.svg")], className='light icon'),
                            html.Div([html.Img(src="/assets/images/icons_navigation/pie-chart-2-fill.svg")], className='dark icon'),
                            html.Div(['Settings'], className='text')
                        ], href='/settings', className='overview nav-btn'),
                ], id='opt-3', className='item-ctn'),
            ], className='settings-section'),
            
            html.Div([
                html.Div([
                    html.Div([
                            html.Img(src="/assets/images/icons_navigation/jaeroorette.jpg")
                        ], className='display-picture'),
                    html.Div([
                            html.Div([html.H4('April Kim Zurc')], className='Username'),
                            html.Div(['aprkimzurc@gmail.com'], className='email'),
                        ], className='details'),
                    html.Div([
                            html.Img(src="/assets/images/icons_navigation/more-2-fill-1.svg"),
                        ], className='more-btn')
                ], className='ctn')
            ], className='account-section')
        ], className='navigation'),
                
        
        
        # output: layout pages
        html.Div([
            # dcc.Location(id="url", refresh=False),
            dash.page_container
        ], className='content-wrapper')
    ],
    className= "app-container"
)

# Run the script
if __name__ == '__main__':
    app.run(debug=True, threaded=True)