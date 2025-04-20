from dash import html, dcc, Output, Input, State, callback, ctx, Patch
import os, sys
import numpy as np
import dash


# Utilities
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from utils.get_data import auto_extract


"""
    Template for Location Filtering:
    
"""


def Location_filter():
    return html.Div([
        html.Div([
            
            ## Location Filters:
            html.Div([
                html.Div([
                            html.Div(['Region'], className='label'),
                            dcc.Dropdown(np.array([
                                'BARMM', 'CAR', 'CARAGA', 'MIMAROPA', 'NCR', 'PSO', 'Region I',
                                'Region II', 'Region III', 'Region IV-A', 'Region IX', 'Region V',
                                'Region VI', 'Region VII', 'Region VIII', 'Region X', 'Region XI', 'Region XII'
                            ]), id='region', multi=True),
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
            # dcc.Store(id='location-filter', data={
            #     'region': [],
            #     'province': [],
            #     'division': [],
            #     'district': [],
            #     'municipality': [],
            #     'brgy': [],
            # })
        ], className='primary-options dropdown-ctn'),
        
    ], id='location-based-filter')

