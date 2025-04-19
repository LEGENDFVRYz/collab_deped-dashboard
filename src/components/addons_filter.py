from random import choice
import selectors
from tkinter import YES
from dash import html, dcc, callback, Output, Input, State, ctx
from dash import no_update

"""
    Template for Additional Filters:
    
    
"""


def Addons_filter():
    return html.Div(children=[
        
        ## MODIFIED MOC SECTION
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
        
        
        ### -- SENIOR HIGH SECTION
        html.Div([
            ## FILTER FIRST BY STRAND
            html.Div([
                        html.Div(['Filter by Tracks:'], className='label'),
                        dcc.Dropdown(options=[
                                        {'label': 'ACADEMIC', 'value': 'ACADEMIC'},
                                        {'label': 'TECHNICAL-VOCATIONAL-LIVELIHOOD', 'value': 'TVL'},
                                        {'label': 'ARTS AND DESIGN', 'value': 'ARTS'},
                                        {'label': 'SPORTS', 'value': 'SPORTS'},
                                        {'label': 'MIXED (ALL TRACKS)', 'value': 'MIXED'}],
                                    placeholder="Select Strand First...",
                                    multi=True,
                                    id='strand-dropdown'
                                    )
                ], className='dropdown-opt-box'),
            
            ## FILTER BY TRACKS
            html.Div([
                        html.Div(['Filter by Strand:'], className='label'),
                        dcc.Dropdown([], id='track-dropdown', disabled=True, multi=True, placeholder='Select "Academic" Track to Multiselect Strand...'),
                ], className='dropdown-opt-box'),
        ], className='add-shs-options category-ctn'),

          
        ## SUB CLASSIFICATION SECTION
        html.Div([
            html.Div([
                        html.Div(['Filter by Subclassification:'], className='label'),
                        dcc.Dropdown(options=[
                                                'DepED Managed', 'Sectarian', 'Non-Sectarian', 'LUC', 'SUC Managed', 'DOST Managed', 'Other GA Managed', 'Local International School', 'SCHOOL ABROAD'
                                            ],
                                            placeholder="Multi-select Subclassification to Filter...",
                                        id='subclass-dropdown',
                                        multi=True,
                                    ),
                ], className='dropdown-opt-box'),
            ], className='add-subclass-options category-ctn'),
        
        
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
            ### -- SECTOR SECTION
            html.Div([
                ## FILTER BY SECTORS
                html.Div([
                            html.Div(['Filter by Sector:'], className='label'),
                            dcc.Checklist([ 
                                    'Public', 'Private', 'SUCsLUCs', 'PSO'
                                ], id='sector-checklist', className='modernized'),
                    ], className='checklist-opt-box'),
            ], className='add-sector-options category-ctn'),
            
            ### -- TYPES SECTION
            html.Div([
                ## FILTER BY SECTORS
                html.Div([
                            html.Div(['Filter by Types:'], className='label'),
                            dcc.Checklist([ 
                                    'School with no Annexes', 'Mother school', 'Annex or Extension school(s)', 'Mobile School(s)/Center(s)'
                                ], id='types-checklist', className='modernized'),
                    ], className='checklist-opt-box'),
            ], className='add-types-options category-ctn'),
        ], className='double-section'),
        
    ], className='secondary-rendered')
    


############################################################
## SENIOR HIGH -- Updating options of track based on strand
############################################################
@callback(
    Output('track-dropdown', 'options'),
    Output('track-dropdown', 'disabled'),
    Input('strand-dropdown', 'value'),
    prevent_initial_call=True
)
def update_tracks(strand):
    # print(strand)
    if 'ACADEMIC' in strand:
        return [{'label': track, 'value': track} for track in ['ABM', 'HUMSS', 'STEM', 'GAS']], False
    else:
        return [], True
    


############################################################
## MOD COC -- Updating options of track based on mod coc
############################################################
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



############################################################
## --- ACCESS THE FILTERED SESSION DATA
############################################################

@callback(
    Output('filtered_values', 'data'),
    Input('proceed-btn', 'n_clicks'),
    
    State('sector-checklist', 'value'),
    State('types-checklist', 'value'),
    State('gender-dropdown', 'value'),
    State('subclass-dropdown', 'value'),
    State('strand-dropdown', 'value'),
    State('track-dropdown', 'value'),
    State('grade-lvl-dropdown', 'value'),
    prevent_initial_call=True
)
def retrieve_filtered_values(btn, sector, types, gender, subclass, strand, track, grade):
    # if any(x is None for x in [sector, types, gender, subclass]):
    #     return no_update
    filter_data = {}
    keys = ['sector', 'types', 'gender', 'subclass', 'strand', 'track', 'grade']
    
    for i, category in enumerate([sector, types, gender, subclass, strand, track, grade]):
        if category:
            print(i, category)
            filter_data[keys[i]] = category
    return filter_data
    
    
@callback(
    Output('print', 'children'),
    Input('filtered_values', 'data'),
)
def checked(data):
    for key, value in data.items():
        print(f"{key}: {value}")
    
    return data