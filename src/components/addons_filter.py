import array
import numpy as np
from dash import html, dcc, callback, Output, Input, State, ctx

"""
    Template for Additional Filters:
    
    
"""


def Addons_filter(reference:array):
    return html.Div(children=[
        *([
            ## -- LOCATION SECTION
            html.Div([
                # dcc.Store(id='location-filter'),
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
            ], className='add-location-options category-ctn'),
        ] if reference[0] else []),
        
        *([
            ## -- MODIFIED MOC SECTION
            html.Div([
                ## FILTER FIRST BY MOD COC
                html.Div([
                            html.Div(['Filter by Modified MOC:'], className='label'),
                            dcc.Dropdown(['Purely ES', 'JHS with SHS', 'All Offering', 'ES and JHS', 'Purely JHS', 'Purely SHS'],
                                            placeholder="Select Strand First...",
                                            id='modcoc-dropdown'
                                        )
                    ], className='dropdown-opt-box'),
                
                ## FILTER BY GRADE LEVEL
                html.Div([
                    html.Div(['Filter by Grade Level:'], className='label'),
                    dcc.Dropdown(options=[],
                                id='grade-lvl-dropdown', disabled=True, multi=True, placeholder="Multi-select Grade Level to Filter..."),
                    ], className='dropdown-opt-box'),
            ], className='add-mod-coc-options category-ctn'),
        ] if reference[3] else []),
        
        *([
            ## -- SUB CLASSIFICATION SECTION
            html.Div([
                ## Filter by Sectors
                html.Div([
                    html.Div(['Filter by Sector:'], className='label'),
                    dcc.Dropdown([ 
                                    'Public', 'Private', 'SUCs/LUCs', 'PSO'
                                ], 
                                id='sector-dropdown',
                                placeholder="Select Sector to proceed...",
                                multi=True,),
                    ], className='dropdown-opt-box'),
                
                ## Filter by Subclassification
                html.Div([
                    html.Div(['Filter by Subclassification:'], className='label'),
                    dcc.Dropdown(options=[],
                                    placeholder='Select "Sector" first to select Subclassification...',
                                    id='subclass-dropdown',
                                    multi=True,
                                    disabled=True
                                ),
                ], className='dropdown-opt-box'),
                    
            ], className='add-subclass-options category-ctn'),
        ] if reference[2] else []),
        
        *([
            ### -- SENIOR HIGH SECTION
            html.Div([
                ## FILTER FIRST BY TRACK
                html.Div([
                            html.Div(['Filter by Tracks:'], className='label'),
                            dcc.Dropdown(options=[
                                            {'label': 'ACADEMIC', 'value': 'ACADEMIC'},
                                            {'label': 'TECHNICAL-VOCATIONAL-LIVELIHOOD', 'value': 'TVL'},
                                            {'label': 'ARTS AND DESIGN', 'value': 'ARTS'},
                                            {'label': 'SPORTS', 'value': 'SPORTS'}],
                                        placeholder="Select Strand First...",
                                        multi=True,
                                        id='track-dropdown'
                                        )
                    ], className='dropdown-opt-box'),
                
                ## FILTER BY STRAND
                html.Div([
                            html.Div(['Filter by Strand:'], className='label'),
                            dcc.Dropdown([], id='strand-dropdown', disabled=True, multi=True, placeholder='Select "Academic" Track to Multiselect Strand...'),
                    ], className='dropdown-opt-box'),
        ], className='add-shs-options category-ctn'),
        ] if reference[1] else []),
        
        
        ## GENDER SECTION
        html.Div([
            html.Div([
                        html.Div(['Filter by Gender:'], className='label'),
                        dcc.Dropdown(options=[
                                                {'label': 'Male', 'value': 'M'},
                                                {'label': 'Female', 'value': 'F'},
                                            ],
                                        placeholder="Select Gender to Filter... (Default Both)",
                                        id='gender-dropdown'
                                    ),
                ], className='dropdown-opt-box'),
            ], className='add-gender-options category-ctn'),
        
        
        html.Div([
            ### -- TYPES SECTION
            html.Div([
                ## FILTER BY TYPEs
                html.Div([
                            html.Div(['Filter by Types:'], className='label'),
                            dcc.Checklist([ 
                                    'School with no Annexes', 'Mother school', 'Annex or Extension school(s)', 'Mobile School(s)/Center(s)'
                                ], id='types-checklist', className='modernized'),
                    ], className='checklist-opt-box'),
            ], className='add-types-options category-ctn'),
        ], className='double-section'),
    ], className='secondary-rendered')