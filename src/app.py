import dis
import dash
from dash import Dash, dcc, html, callback_context
from dash import Input, Output, State
import dash_bootstrap_components as dbc

from src.server import server
from src.server import cache
from flask import session
from auth_db import authentication_db, login_user

# Callbacks
from src.utils import activeTab_callback

# Initialize DB
from src.data import enrollment_db_engine
authentication_db()

# Main Applications
app = Dash(__name__, server=server, use_pages=True, suppress_callback_exceptions=True)
cache.init_app(app.server)


# Main File Content
app.layout = html.Div(
    children=[
        dcc.Store(id='user-data', data={}, storage_type="local"),
        dcc.Store(id="active-tab", data="", storage_type="session"),  # Store clicked tab
        dcc.Store(id="chart-trigger", data=False, storage_type="session"),
        dcc.Store(id="base-trigger", data=False, storage_type="session"),
        
        dcc.Store(id="rotation-state", data=False),  # stores toggle state
        
        dcc.Location(id="url", refresh=True),  # Gets the current pathname
        
        # MODAL: Login inputs
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Member Login"), close_button=True),
                dbc.ModalBody(
                    html.Div([
                        # Top: Logo area
                        html.Div("LOGO HERE", id="login-logo"),

                        # Middle: Form inputs and login button
                        html.Div([
                            html.Label("Username or Email", htmlFor="login-username"),
                            dcc.Input(
                                type="text",
                                id="login-username",
                                placeholder="Enter username or email"
                            ),

                            html.Label("Password", htmlFor="login-password"),
                            dcc.Input(
                                type="password",
                                id="login-password",
                                placeholder="Enter password"
                            ),

                            html.Button("Log in", id="login-button", type="submit"),
                        ], id="login-form"),

                        # Bottom: Links
                        html.Div([
                            html.A("Sign Up", href="#", id="signup-link"),
                            html.A("Forgot Password?", href="#", id="reset-link"),
                        ], id="login-links"),
                    ], id="login-container")
                ),
                # dbc.ModalFooter(
                #     html.Button("Close", id="close", className="ms-auto", n_clicks=0)
                # )
            ],
            id="login-modal",
            backdrop="static",
            is_open=False,
            size="md",
            centered=True,
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
                
                # html.Div([
                #     html.Div([], className='indicator'),
                #     dcc.Link([
                #             html.Div([html.Img(src="/assets/images/icons_navigation/pie-chart-fill.svg")], className='light icon'),
                #             html.Div([html.Img(src="/assets/images/icons_navigation/pie-chart-2-fill.svg")], className='dark icon'),
                #             html.Div(['Help'], className='text')
                #         ], href='/help', className='overview nav-btn'),
                # ], id='opt-2', className='item-ctn'),
                
                html.Div([
                    html.Div([], className='indicator'),
                    dcc.Link([
                            html.Div([html.Img(src="/assets/images/icons_navigation/settings-1-fill.svg")], className='light icon'),
                            html.Div([html.Img(src="/assets/images/icons_navigation/settings-1.svg")], className='dark icon'),
                            html.Div(['App Settings'], className='text')
                        ], href='/settings', className='overview nav-btn'),
                ], id='opt-3', className='item-ctn'),
            ], className='settings-section'),
            
            html.Div([
                html.Div([

                    html.Div([
                        # ACCOUNT LOGIN OR PROFILE
                        html.Div([
                                html.Img(src="/assets/images/guest-icon.svg")
                            ], className='display-picture'),
                        html.Div([
                                html.Div([html.H4('Guest')], className='Username', id='username-holder'),
                                html.Div(['Public Account Mode'], className='email', id='email-holder'),
                            ], className='details'),
                        # html.A([
                            html.Div([
                                html.Img(src="/assets/images/icons_navigation/more-2-fill-1.svg"),
                            ], id='more-btn'),
                        # ], id='more-btn', n_clicks=0),
                    ], className='acc-details'),
                
                    html.Div([
                        html.Div(['LOGIN'], id='login-call', className='setting-btn'),
                        html.Div(['LOG OUT'], id='logout-call', className='setting-btn'),
                    ], id='acc-opts'),
                    
                ], className='ctn-wrap')
                
                
            ], className='account-section')
        ], className='navigation'),
        
        
        # output: layout pages
        html.Div([
            
            # dcc.Location(id="url", refresh=False),
            dash.page_container
        ], className='content-wrapper', id='content-render')
    ],
    className= "app-container"
)


############################ LOGIN MODAL CALLBACKS ############################

@app.callback(
    Output("login-modal", "is_open"),
    Input("login-call", "n_clicks"),
    # Input("close", "n_clicks"),
    State("login-modal", "is_open"),
)
def toggle_modal(n1, is_open):
    # if n1 or n2:
    if n1:
        return not is_open
    return is_open


@app.callback(
    Output('url', 'pathname'),  # ✅ THIS TRIGGERS A PAGE CHANGE
    Output("user-data", "data"),
    Input("login-button", "n_clicks"),
    Input("login-password", "n_submit"),
    State("login-username", "value"),
    State("login-password", "value"),
    prevent_initial_call=True
)
def get_login_details(n_clicks, n_submit, identifier, password):
    triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id in ["login-button", "login-password"]:
        user = login_user(identifier, password)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            # print(session)
            return '/', {
                'username': user.username,
                'email': user.email,
                'name': user.full_name,
                'role': user.role
            }
    return dash.no_update, dash.no_update
    

@app.callback(
    Output('username-holder', 'children'),
    Output('email-holder', 'children'),
    Input("user-data", "data"),
    prevent_initial_call=True
)
def get_login_details(user_info):
    # print(user_info)
    if user_info:
        return html.H4(f"{user_info['name']}"), user_info["email"]
    return html.H4(f"Guest"), "Public Account Mode"


############################ LOGOUT CALLBACKS ############################

@app.callback(
    Output("user-data", "data", True),          
    Output("url", "href"),                
    Input("logout-call", "n_clicks"),
    prevent_initial_call=True
)
def logout(trigger):
    if trigger:
        session.clear()  # clears all session data
        # print(session)
        return {}, "/"   # or "/login" if you have a login page
    return dash.no_update, dash.no_update


##################### ACCOUNT SETTING COLLAPSE #####################
@app.callback(
    Output("acc-opts", "style"),
    Input("more-btn", "n_clicks"),
    State("acc-opts", "style"),
    prevent_initial_call=True
)
def toggle_collapse(n_clicks, current_style):
    # Default to showing if no style has been set yet
    if not current_style or current_style.get("display") == "none":
        return {"display": "flex"}
    else:
        return {"display": "none"}


@app.callback(
    Output("more-btn", "style"),
    Output("rotation-state", "data"),
    Input("more-btn", "n_clicks"),
    State("rotation-state", "data"),
    prevent_initial_call=True
)
def rotate_div(n_clicks, rotated):
    new_state = not rotated
    style = {
        "transition": "transform 0.3s ease-in-out",
        "display": "flex",
        "flexDirection": "column",
        "alignSelf": "center",
        "width": "1.75em",
        "cursor": "pointer",
        "transform": "rotate(180deg)" if new_state else "rotate(0deg)"
    }
    return style, new_state



##################### RENDERING BASED ON ROLE #####################
@app.callback(
    Output("nav-2", "style"),
    Output("nav-3", "style"),
    Output("opt-3", "style", True),
    Output("login-call", "style"),
    Output("logout-call", "style"),
    Input("url", "pathname"),
    prevent_initial_call=True
)
def display_limitations(user):
    role = session.get("role", "guest")
    
    # Pre-definded Styles
    disabled =  { "pointerEvents": "none",  "cursor": "not-allowed",  "opacity": 0.6 }
    noshow = {"display": "none"}

    # print(session)
    if role == "admin":
        return dash.no_update, dash.no_update, dash.no_update, noshow, dash.no_update,
    elif role == "guest":
        return disabled, disabled, noshow, dash.no_update, noshow



##################### PROTECTING PAGES BASED ON ROLE #####################
@app.callback(
    Output("content-render", "children"),
    Input("url", "pathname")
)
def route_protected_pages(pathname):
    # print("????")
    role = session.get("role", "guest")
    
    # RESTRICTED
    if pathname in ("/school-level", "/settings", "/analytical"):
        if role != "admin":
            return dcc.Location(href="/unauthorized", id="redirect-unauth")
    return dash.no_update


# Run the script
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
