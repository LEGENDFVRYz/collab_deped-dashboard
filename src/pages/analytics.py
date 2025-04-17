import dis
import dash
from dash import html, dcc, Output, Input, State, callback, ctx

# src/pages/dashboard.py
from src.components.card import Card

####### PAGES ########
from src.pages.analytics_location import render_location_filter
from src.pages.analytics_seniorhigh import render_seniorhigh_filter
from src.pages.analytics_subclass import render_subclass_filter
from src.pages.analytics_offering import render_offering_filter



# Callbacks
from src.utils import filter_menu_callback
from src.utils import saved_tabs_analytics


# Landing page
dash.register_page(__name__, path="/analytics")  

# Main Page
layout = html.Div([
    dcc.Store(id="analytics-sub-tracker", data=""),
    
    ## -- Standard: Page Content Header
    html.Div([
        html.H1('Analytical Tools')
    ], className='page-header'),
    
    ## -- Main Content: Start hereee
    html.Div([
        html.Div([
            ## -- Filtering Options
            html.Div([
                    Card([
                        html.Div([
                            html.H3(f"Filter by :", id='filter-header')
                        ], className='primary-tags'),
                        
                        ## -- Primary options
                        html.Div([
                            ## Render options here
                            
                        ], id='filter-options'),
                    ], margin=False)
                ], id='primary-wrap', className='primary-filter'),
            
        
            
            
            html.Div([
                    html.Div([html.Button('Add Additional Features', id='addons-btn', n_clicks=0)], className='additional'),
                    html.Div([html.Button('Submit', id='proceed-btn', n_clicks=0)], className='proceed'),
                ], className='confirmation-box'),
            dcc.Interval(id='hide-delay', interval=500, n_intervals=0, max_intervals=0)
            
            # ## -- Additional filters
            # html.Div([
            #         html.Div([
            #             html.H3(f"Select Additional Filters:")
            #         ], className='secodary-tags'),
                    

            #     ], id='secondary-wrap', className='secondary-filter'),
            
            
            # html.Div([

            #     ], className='added-filter'),
            
            
        ], id='filter-section', className='left-content'),
        
        html.Div([
        ## -- Rendering Plots

            html.Div([
                html.Div([
                        html.H2(["SELECT FILTER TO PROCEED"])
                    ], id="placeholder"),
                
                html.Div([
                    ## -- RENDER THE REPORT HERE
                    
                    
                    ], id='plot-filtered-page')
            ], id='plot-content', className="")
            
        ], className='right-content'),
    ], className='content-section'),
], className='analytics-page container')



# close the filter function:
# # Step 1: Add animation class (but keep visible)
# @callback(
#     Output('filter-section', 'style'),
#     Output('placeholder', 'style'),
#     Input('proceed-btn', 'n_clicks')
# )
# def hide_div(n_clicks):
#     if n_clicks > 0:
#         return {'display': 'none'}, {'background-color': '#EFF3F6'}
#     return {'display': 'flex'}, {}


@callback(
    Output('filter-section', 'style'),
    Output('placeholder', 'style'),
    Output('hide-delay', 'max_intervals'),
    Input('proceed-btn', 'n_clicks'),
    Input('hide-delay', 'n_intervals'),
    prevent_initial_call=True
)
def handle_hide(n_clicks, n_intervals):
    triggered_id = ctx.triggered_id

    if triggered_id == 'proceed-btn':
        # Step 1: Fade out placeholder, instantly hide filter-section
        return {'display': 'none'}, {'background-color': '#EFF3F6'}, 1

    elif triggered_id == 'hide-delay':
        # Step 2: After delay, hide placeholder
        return dash.no_update, {'display': 'none'}, dash.no_update

    return dash.no_update, dash.no_update, dash.no_update


@callback(
    Output('plot-filtered-page', 'children'),
    Output('plot-content', 'className'),
    Input('hide-delay', 'n_intervals'),
    State('analytics-sub-tracker', 'data'),
    prevent_initial_call=True
)
def render_after_fade(n, data):
    opt = ["Location", "Senior High", "Subclassification", "Offering"]
    pages = [
        render_location_filter, render_seniorhigh_filter, render_subclass_filter, render_offering_filter
    ]
    for i, choices in enumerate(opt):
        if data == choices:
            return pages[i](), "rendered"
        