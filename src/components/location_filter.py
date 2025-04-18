from dash import html, dcc, Output, Input, State, callback, ctx
import os, sys, re
import pandas as pd
import numpy as np

# Utilities
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from utils.get_data import auto_extract


"""
    Template for Location Filtering:
    
"""

dataframe = auto_extract([
        'region', 'division', 'district', 'province', 'municipality', 'brgy'
    ], is_specific=True, distinct=True)
dataframe

region_options = np.sort(dataframe['region'].unique())
region_options

location_data_filter = {
    'region': [],
    'province': [],
    'division': [],
    'district': [],
    'municipality': [],
    'brgy': [],
}


def Location_filter():
    return html.Div([
        html.Div([
            ## PRIMARY FILTERS:
            html.Div([
                html.Div([
                            html.Div(['Region'], className='label'),
                            dcc.Dropdown(region_options, id='region', multi=True),
                    ], className='dropdown-opt-box'),
                html.Div([
                            html.Div(['Province'], className='label'),
                            dcc.Dropdown([], id='province', disabled=True, multi=True),
                    ], className='dropdown-opt-box'),
            ], className='double-dropdown'),
            
            html.Div([
                html.Div([
                            html.Div(['Division'], className='label'),
                            dcc.Dropdown([], id='division', disabled=True, multi=True),
                    ], className='dropdown-opt-box'),
                html.Div([
                            html.Div(['District'], className='label'),
                            dcc.Dropdown([], id='district', disabled=True, multi=True),
                    ], className='dropdown-opt-box'),
            ], className='double-dropdown'),
            
            html.Div([
                        html.Div(['Municipality'], className='label'),
                        dcc.Dropdown([], id='municipality', disabled=True, multi=True),
                ], className='dropdown-opt-box'),
            html.Div([
                        html.Div(['Barangay'], className='label'),
                        dcc.Dropdown([], id='barangay', disabled=True, multi=True),
                ], className='dropdown-opt-box'),
            dcc.Store(id='location-filter', data=location_data_filter)
        ], className='primary-options dropdown-ctn'),
        
        # html.Div([
        #     html.Div([
        #         html.Div([
        #                 html.Div(['Strand:'], className='label'),
        #                 dcc.Dropdown(['Academic', 'Non Academic'], id='strand', disabled=True, multi=True),
        #         ], className='dropdown-opt-box'),
                
        #         html.Div([
        #                 html.Div(['Tracks'], className='label'),
        #                 dcc.Checklist(
        #                     options={}
        #                 )
        #         ], className='selectable')
        #     ], className='tracks-dropdown')
        # ], className='secondary-options')
        
    ], id='Location-based-filter')







#####################################################################################
                        # PRIMARY: LOCATION MULTISELECT #                           
#####################################################################################

### -- TRACK USER INPUT 
@callback(
    Output('location-filter', 'data'),
    
    Input('region', 'value'),
    Input('province', 'value'),
    Input('division', 'value'),
    Input('district', 'value'),
    Input('municipality', 'value'),
    Input('barangay', 'value'),
)
def update_location_filters(region, province, division, district, municipality, brgy):
    datas = [region, province, division, district, municipality, brgy]
    result = []
    found_empty = False
    
    for data in datas:
        if found_empty or data == []:
            result.append(None)
            found_empty = True
        else:
            result.append(data)
    
    # print('data stored:\n\t', result, '\n---')
    return result


### -- LOCATION DROPDOWN ACTIVATION 
@callback(
    Output('province', 'disabled'),
    Output('division', 'disabled'),
    Output('district', 'disabled'),
    Output('municipality', 'disabled'),
    Output('barangay', 'disabled'),
    
    Output('province', 'options'),
    Output('division', 'options'),
    Output('district', 'options'),
    Output('municipality', 'options'),
    Output('barangay', 'options'),
    
    Input('location-filter', 'data')
)
def main_query(stored_data):
    activation = [True, True, True, True, True]
    opt = [[], [], [], [], []]
    
    # Controls if users select a region choices
    if stored_data[0] is not None:
        activation[0] = False
        region_df = dataframe[dataframe['region'].isin(stored_data[0])]
        opt[0] = np.sort(region_df['province'].unique())
    
    if stored_data[1] is not None:
        activation[1] = False
        province_df = region_df[region_df['province'].isin(stored_data[1])]
        opt[1] = np.sort(province_df['division'].unique())
        
    if stored_data[2] is not None:
        activation[2] = False
        division_df = province_df[province_df['division'].isin(stored_data[2])]
        opt[2] = np.sort(division_df['district'].unique())
        
    if stored_data[3] is not None:
        activation[3] = False
        district_df = division_df[division_df['district'].isin(stored_data[3])]
        opt[3] = np.sort(district_df['municipality'].unique())
        
    if stored_data[4] is not None:
        activation[4] = False
        municipality_df = district_df[district_df['municipality'].isin(stored_data[4])]
        opt[4] = np.sort(municipality_df['brgy'].unique())
        
    if stored_data[5] is not None:
        brgy_df = municipality_df[municipality_df['brgy'].isin(stored_data[5])]
        # print(brgy_df.head())
    
    return tuple(activation) + tuple(opt)


### -- Reset Frontend Values
@callback(
    Output('province', 'value'),
    Input('region', 'value')
)
def reset_dropdown2_value(dropdown1_value):
    if dropdown1_value is None:
        return None  # Reset dropdown-2 value when dropdown-1 is cleared
    return None  # No value set by default for dropdown-2 (optional)

@callback(
    Output('division', 'value'),
    Input('province', 'value')
)
def reset_dropdown2_value(dropdown1_value):
    if dropdown1_value is None:
        return None  # Reset dropdown-2 value when dropdown-1 is cleared
    return None  # No value set by default for dropdown-2 (optional)

@callback(
    Output('district', 'value'),
    Input('division', 'value')
)
def reset_dropdown2_value(dropdown1_value):
    if dropdown1_value is None:
        return None  # Reset dropdown-2 value when dropdown-1 is cleared
    return None  # No value set by default for dropdown-2 (optional)

@callback(
    Output('municipality', 'value'),
    Input('district', 'value')
)
def reset_dropdown2_value(dropdown1_value):
    if dropdown1_value is None:
        return None  # Reset dropdown-2 value when dropdown-1 is cleared
    return None  # No value set by default for dropdown-2 (optional)

@callback(
    Output('barangay', 'value'),
    Input('municipality', 'value')
)
def reset_dropdown2_value(dropdown1_value):
    if dropdown1_value is None:
        return None  # Reset dropdown-2 value when dropdown-1 is cleared
    return None  # No value set by default for dropdown-2 (optional)

#####################################################################################
