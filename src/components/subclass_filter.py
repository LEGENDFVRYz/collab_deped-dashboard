from dash import html, dcc


"""
    Template for Sub Class Filtering:
    
    
"""


def Subclass_filter():
    return html.Div([
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
                                disabled=True,
                            ),
            ], className='dropdown-opt-box'),
            
        ], className='primary-options dropdown-ctn'),
    ], id='subclass-based-filter')
