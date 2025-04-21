import dash
import numpy as np
import pandas as pd
from dash import html, dcc, Output, Input, State, callback, ctx
from sqlalchemy import false
from src.data import enrollment_db_engine, smart_filter


# src/pages/dashboard.py
from src.components.card import Card

# Used the cache:
from src.server import load_location_data

# Callbacks
from src.utils import filter_menu_callback
from src.utils import saved_tabs_analytics

############################### PAGES ################################
from src.pages.analytics_location import render_location_filter
from src.pages.analytics_seniorhigh import render_seniorhigh_filter
from src.pages.analytics_subclass import render_subclass_filter
from src.pages.analytics_offering import render_offering_filter
from src.components.addons_filter import Addons_filter



# Landing page
dash.register_page(__name__, path="/analytics", suppress_callback_exceptions=True)  

# Main Page
layout = html.Div([
    dcc.Store(id="analytics-sub-tracker", data=""),
    dcc.Store(id='sub-status-toggle', data=True), 
    
    ## -- Store for filter menus
    dcc.Store(id='location-filter'),
    
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
                    html.Div([html.Button('Add Additional Filters', id='addons-btn', n_clicks=0)], className='additional'),
                    html.Div([html.Button('Submit', id='proceed-btn', n_clicks=0)], className='proceed'),
                ], id='confirmation-box'),
            dcc.Interval(id='hide-delay', interval=800, n_intervals=0, disabled=True),
            
            
            html.Div([
                html.Div([
                    html.H3(f"Additional Filters:")
                    
                ], className='secondary-tag category'),     
                      
                ## -- Secondary options
                html.Div([
                    ## Render secondary options here
                    
                ], id='secondary-wrap'),
            ], id='secondary-filter')          
        ], id='filter-section', className='left-content'),
        
        
        ## -- Rendering Plots
        html.Div([
            html.Div([
                html.Div([
                        html.H2(["SELECT FILTER TO PROCEED"])
                    ], id="placeholder"),
                
                html.Div([
                    ## -- RENDER THE REPORT HERE
                    html.Div([], id='print'),
                    
                    
                    ], id='plot-filtered-page')
            ], id='plot-content', className="")
            
        ], className='right-content'),
    ], className='content-section'),
], className='analytics-page container')



############################################################
## HANDLE ANIMATION KEY AND RENDERING SUB PAGES
############################################################
@callback(
    Output('filter-section', 'style', allow_duplicate=True),
    Output('placeholder', 'style', allow_duplicate=True),
    Output('hide-delay', 'disabled'),
    Input('proceed-btn', 'n_clicks'),
    Input('hide-delay', 'n_intervals'),
    prevent_initial_call=True
)
def handle_hide(n_clicks, n_intervals):
    triggered_id = ctx.triggered_id
    
    if triggered_id == 'proceed-btn':
        return {'display': 'none'}, {'background-color': '#EFF3F6'}, False  # Enable timer

    elif triggered_id == 'hide-delay':
        return dash.no_update, {'display': 'none'}, True  # Disable after firing

    return dash.no_update, dash.no_update, dash.no_update


@callback(
    Output('plot-filtered-page', 'children', allow_duplicate=True),
    Output('plot-content', 'className', allow_duplicate=True),
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



############################################################
## HANDLE BUTTONS KEY AND RENDERING ADDITIONAL FILTERS
############################################################
@callback(
    [
        Output('confirmation-box', 'style'),
        Output('secondary-filter', 'style'),
        Output('addons-btn', 'children'),
    ],
    [Input('addons-btn', 'n_clicks')]
)
def animation_additional_filter(sensor):
    if (sensor % 2) == 1:
        return {'order': '3'}, {'order': '2', 'display': 'flex'}, "Cancel"
    return {'order': '2'}, {'order': '3', 'display': 'none'}, "Add Additional Filters"


@callback(
    Output('secondary-wrap', 'children'),
    Input("analytics-sub-tracker", "data"),
    # prevent_initial_call=True
)
def render_additional_filters(reference):
    switch = [True, True, True, True]
    opt = ["Location", "Senior High", "Subclassification", "Offering"]
    
    switch[opt.index(reference)] = False    # Exclude the main filter depend on sub page active
    
    return Addons_filter(switch)
    
############################################################
## DETERMINE IF THE USER SWITCH THROUGH PAGES
############################################################
@callback(
    Output('filter-section', 'style', allow_duplicate=True),
    Output('placeholder', 'style', allow_duplicate=True),
    Output('plot-filtered-page', 'children', allow_duplicate=True),
    Output('plot-content', 'className', allow_duplicate=True),
    Output('addons-btn', 'n_clicks'),
    Output('sub-status-toggle', 'data'),

    
    Input("location", "n_clicks"),
    Input("senior-high", "n_clicks"),
    Input("subclass", "n_clicks"),
    Input("offering", "n_clicks"),
    State("analytics-sub-tracker", "data"),
    State("sub-status-toggle", "data"),
    prevent_initial_call=True
)
def sub_tab_has_change(in1, in2, in3, in4, sub_tracker, sub_status):
    triggered_id = ctx.triggered_id
    trans = {
        'location': 'Location',
        'senior-high': 'Senior High',
        'subclass': 'Subclassification',
        'offering': 'Offering',
    }
    

    if trans[triggered_id] == sub_tracker:
        # print("page is still the same")
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    else:
        # print("you clicked different page--")
        return {'display': 'flex'}, {'display': 'flex'}, html.Div(), "", 0, (not sub_status)
    
    
    
#####################################################################################
                        # PRIMARY: LOCATION MULTISELECT #                           
#####################################################################################

### -- TRACK USER INPUT 
@callback(
    Output('location-filter', 'data'),
    
    Output('province', 'disabled'),
    Output('division', 'disabled'),
    Output('district', 'disabled'),
    Output('municipality', 'disabled'),
    Output('barangay', 'disabled'),
    
    Input('region', 'value'),
    Input('province', 'value'),
    Input('division', 'value'),
    Input('district', 'value'),
    Input('municipality', 'value'),
    Input('barangay', 'value'),
)
def update_location_filters(region, province, division, district, municipality, brgy):
    datas = [region, province, division, district, municipality, brgy]
    activation = [True] * 5
    
    result = []
    found_empty = False

    for i, data in enumerate(datas):
        if found_empty or data in [None, []]:
            result.append(None)
            found_empty = True
        else:
            result.append(data)
        if i < 5:
            activation[i] = True if found_empty else False
        
    return (result, *activation)


### -- LOCATION DROPDOWN ACTIVATION 
@callback(
    Output('province', 'options'),
    Output('division', 'options'),
    Output('district', 'options'),
    Output('municipality', 'options'),
    Output('barangay', 'options'),

    Input('location-filter', 'data'),
)
def update_dropdowns(stored_data):
    dataframe = load_location_data()
    activation = [True] * 5
    
    # Initialize empty list for options
    opt = [[], [], [], [], []]
    
    # Controls if users select a region choices
    if stored_data[0] is not None:
        region_df = dataframe[dataframe['region'].isin(stored_data[0])]
        opt[0] = np.sort(region_df['province'].unique())
    
    if stored_data[1] is not None:
        province_df = region_df[region_df['province'].isin(stored_data[1])]
        opt[1] = np.sort(province_df['division'].unique())
        
    if stored_data[2] is not None:
        division_df = province_df[province_df['division'].isin(stored_data[2])]
        opt[2] = np.sort(division_df['district'].unique())
        
    if stored_data[3] is not None:
        district_df = division_df[division_df['district'].isin(stored_data[3])]
        opt[3] = np.sort(district_df['municipality'].unique())
        
    if stored_data[4] is not None:
        municipality_df = district_df[district_df['municipality'].isin(stored_data[4])]
        opt[4] = np.sort(municipality_df['brgy'].unique())
        
    if stored_data[5] is not None:
        brgy_df = municipality_df[municipality_df['brgy'].isin(stored_data[5])]
        # print(brgy_df.head())
    # print(stored_data)
    
    return *opt,


### -- Reset Frontend Values
@callback(
    Output('province', 'value'),
    Output('division', 'value'),
    Output('district', 'value'),
    Output('municipality', 'value'),
    Output('barangay', 'value'),

    Input('region', 'value'),
    Input('province', 'value'),
    Input('division', 'value'),
    Input('district', 'value'),
    Input('municipality', 'value'),
)
def reset_values(region, province, division, district, municipality):
    if ctx.triggered_id == 'region':
        return None, None, None, None, None
    elif ctx.triggered_id == 'province':
        return dash.no_update, None, None, None, None
    elif ctx.triggered_id == 'division':
        return dash.no_update, dash.no_update, None, None, None
    elif ctx.triggered_id == 'district':
        return dash.no_update, dash.no_update, dash.no_update, None, None
    elif ctx.triggered_id == 'municipality':
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, None
    return dash.no_update


    
#####################################################################################
## SENIOR HIGH -- Updating options of track based on strand
#####################################################################################

@callback(
    Output('strand-dropdown', 'options'),
    Output('strand-dropdown', 'disabled'),
    Input('track-dropdown', 'value'),
    prevent_initial_call=True
)
def update_tracks(track):
    # print(strand)
    if 'ACADEMIC' in track:
        return [{'label': strand, 'value': strand} for strand in ['ABM', 'HUMSS', 'STEM', 'GAS']], False
    else:
        return [], True
    

#####################################################################################
## SECTOR AND SUBCLASS -- Updating options of track based on mod coc
#####################################################################################

@callback(
    Output('subclass-dropdown', 'options'),
    Output('subclass-dropdown', 'disabled'),
    Input('sector-dropdown', 'value'),
    prevent_initial_call=True
)
def update_sector(sector_value):
    options = []
    
    if 'Public' in sector_value:
        options += [{'label': strand, 'value': strand} for strand in ['DOST Managed', 'DepED Managed', 'Other GA Managed']]
    if 'Private' in sector_value:
        options += [{'label': strand, 'value': strand} for strand in ['Local International School', 'Non-Sectarian', 'Sectarian']]
    if 'SUCs/LUCs' in sector_value:
        options += [{'label': strand, 'value': strand} for strand in ['LUC Managed', 'SUC Managed']]
    if 'PSO' in sector_value:
        options += [{'label': strand, 'value': strand} for strand in ['School Abroad']]
    
    if sector_value or sector_value is None:
        return options, False
    else:
        return [], True
    

#####################################################################################
## MOD COC -- Updating options of track based on mod coc
#####################################################################################

@callback(
    Output('grade-lvl-dropdown', 'options'),
    Output('grade-lvl-dropdown', 'disabled'),
    Input('modcoc-dropdown', 'value')
)
def update_modcoc(modcoc):
    choices = ['Purely ES', 'JHS with SHS', 'All Offering', 'ES and JHS', 'Purely JHS', 'Purely SHS']
    
    label = ["Kindergarden", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Non-Graded ELEM", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Non-Graded JHS", "Grade 11", "Grade 12"]
    value = ["K", "G1", "G2", "G3", "G4", "G5", "G6", "Elem NG", "G7", "G8", "G9", "G10", "JHS NG", "G11", "G12"]
    
    if modcoc == choices[0]:
        return [{'label': label[i], 'value': value[i]} for i in range(0, 8)], False
    elif modcoc == choices[1]:
        return [{'label': label[i], 'value': value[i]} for i in range(8, 15)], False
    elif modcoc == choices[2]:
        return [{'label': label[i], 'value': value[i]} for i in range(0, 15)], False
    elif modcoc == choices[3]:
        return [{'label': label[i], 'value': value[i]} for i in range(0, 13)], False
    elif modcoc == choices[4]:
        return [{'label': label[i], 'value': value[i]} for i in range(8, 13)], False
    elif modcoc == choices[5]:
        return [{'label': label[i], 'value': value[i]} for i in range(13, 15)], False
    else:
        return [], True


#####################################################################################
## --- ACCESS THE FILTERED SESSION DATA
#####################################################################################

@callback(
    Output('filtered_values', 'data'),
    Input('proceed-btn', 'n_clicks'),
    
    State('types-checklist', 'value'),
    State('gender-dropdown', 'value'),
    State('sector-dropdown', 'value'),
    State('subclass-dropdown', 'value'),
    State('track-dropdown', 'value'),
    State('strand-dropdown', 'value'),
    State('modcoc-dropdown', 'value'),
    State('grade-lvl-dropdown', 'value'),
    State('location-filter', 'data'),
    prevent_initial_call=True
)
def retrieve_filtered_values(btn, types, gender, sector, subclass, track, strand, modcoc, grade, location_data):
    # if any(x is None for x in [sector, types, gender, subclass]):
    #     return no_update
    filter_data = {}
    locs = ['region', 'province', 'division', 'district', 'municipality', 'brgy']
    keys = ['type', 'gender', 'sector', 'sub_class', 'track', 'strand', 'mod_coc', 'grade']
    
    for i, category in enumerate([types, gender, sector, subclass, track, strand, modcoc, grade]):
        if category:
            filter_data[keys[i]] = category
    
    for i, loc_data in enumerate(location_data):
        if loc_data:
            filter_data[locs[i]] = loc_data
            
    return filter_data
    
    
@callback(
    Output('print', 'children'),
    Input('filtered_values', 'data'),
    prevent_initial_call=True
)
def checked(data):
    print(data)
    
    # query, params = smart_filter(data)
    # filtered_df = pd.read_sql(query, enrollment_db_engine, params=params)
    
    # print(filtered_df)
    
    return data