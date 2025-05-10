import dash
from dash import Dash, dcc, html
from dash import Input, Output, State
import dash_bootstrap_components as dbc
from src.server import server
from src.server import cache
from src.data import enrollment_db_engine

# Callbacks
from src.utils import activeTab_callback

# important part
# from src.data import enrollment_db_engine, smart_filter


# Main Applications
app = Dash(__name__, server=server, use_pages=True, suppress_callback_exceptions=True)
cache.init_app(app.server)


# Main File Content
app.layout = html.Div(
    children=[
        dcc.Store(id="active-tab", data="", storage_type="session"),  # Store clicked tab
        dcc.Store(id="chart-trigger", data=False, storage_type="session"),
        dcc.Store(id="base-trigger", data=False, storage_type="session"),
        dcc.Location(id="url", refresh=False),  # Gets the current pathname
        
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Header"), close_button=True),
                dbc.ModalBody("Modal content here"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)
                ),
            ],
            id="modal",
            is_open=False,
        ),
        
        
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
                                    html.Div([html.Img(src="/assets/images/icons_navigation/overview-blue.svg")], className='dark icon'),
                                    html.Div(['Overview'], className='text')
                                ], href="/", className='overview nav-btn')
                        ], className='main-tab'),
                ], id='nav-1', className='item-ctn'),
                
                html.Div([
                    html.Div([
                        html.Div([], className='indicator'),
                        dcc.Link([
                                html.Div([html.Img(src="/assets/images/icons_navigation/analytics-white.svg")], className='light icon'),
                                html.Div([html.Img(src="/assets/images/icons_navigation/analytics-blue.svg")], className='dark icon'),
                                html.Div(['Enrollment Insights'], className='text')
                            ], href='/analytics', className='overview nav-btn'),
                    ], className='main-tab'),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.A("by Location")
                            ], id='location', className='tab-btn'),      

                            html.Div([
                                html.A("by Tracks and Strands")
                            ], id='senior-high', className='tab-btn'),

                            html.Div([
                                html.A("by Subclassification")
                            ], id='subclass', className='tab-btn'),
                            
                            html.Div([
                                html.A("by Program Offerings")
                            ], id='offering', className='tab-btn'),
                            html.Div([], className="animation"),
                        ], className='tabs-menu-ctn'),
                        html.Div([], className="tabs-scroll"), 
                    ], className='tabs-menu')
                    
                ], id='nav-2', className='item-ctn'),
                
                html.Div([
                    html.Div([
                        html.Div([], className='indicator'),
                        dcc.Link([
                                html.Div([html.Img(src="/assets/images/icons_navigation/school-level-1-white.svg")], className='light icon'),
                                html.Div([html.Img(src="/assets/images/icons_navigation/school-level-1-blue.svg")], className='dark icon'),
                                html.Div(['School Profile'], className='text')
                            ], href='/school-level', className='overview nav-btn'),
                    ], className='main-tab'),
                    
                    html.Div([
                            html.Div([
                                html.Div([
                                    # html.Img(src="/assets/images/icons_navigation/nav-tab-map-icon.svg"),
                                    html.A("Analysis")
                                ], id='analysis', className='tab-btn'),
                                html.Div([
                                    # html.Img(src="/assets/images/icons_navigation/nav-tab-map-icon.svg"),
                                    html.A("Comparison"),
                                ], id='comparison', className='tab-btn'),
                                html.Div([], className="animation"),
                            ], className='tabs-menu-ctn'),
                            html.Div([], className="tabs-scroll"), 
                        ], className='tabs-menu')
                ], id='nav-3', className='item-ctn'),
            ], className='menu-section'),
            
            html.Div([
                # Account Settings
                html.Div([
                    html.Div([], className='indicator'),
                    dcc.Link([
                            html.Div([html.Img(src="/assets/images/icons_navigation/updates-white.svg")], className='light icon'),
                            html.Div([html.Img(src="/assets/images/icons_navigation/updates-blue.svg")], className='dark icon'),
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
                            html.Div([html.Img(src="/assets/images/icons_navigation/settings-1-fill.svg")], className='light icon'),
                            html.Div([html.Img(src="/assets/images/icons_navigation/settings-1.svg")], className='dark icon'),
                            html.Div(['Settings'], className='text')
                        ], href='/settings', className='overview nav-btn'),
                ], id='opt-3', className='item-ctn'),
            ], className='settings-section'),
            
            html.Div([
                # ACCOUNT LOGIN OR PROFILE
                html.Div([
                    html.Div([
                            html.Img(src="/assets/images/icons_navigation/jaeroorette.jpg")
                        ], className='display-picture'),
                    html.Div([
                            html.Div([html.H4('April Kim Zurc')], className='Username'),
                            html.Div(['aprkimzurc@gmail.com'], className='email'),
                        ], className='details'),
                    html.A([
                        html.Div([
                            html.Img(src="/assets/images/icons_navigation/more-2-fill-1.svg"),
                        ], className='more-btn'),
                    ], id='more-btn', n_clicks=0),
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


@app.callback(
    Output("modal", "is_open"),
    [Input("more-btn", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Run the script
if __name__ == '__main__':
    app.run(debug=True, threaded=True)