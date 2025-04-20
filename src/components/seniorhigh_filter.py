from dash import html, dcc


"""
    Template for Senior High Filtering:
    
    
"""


def Seniorhigh_filter():
    return html.Div([
        html.Div([
            ## FILTER FIRST BY STRAND
            html.Div([
                        html.Div(['Filter by Tracks:'], className='label'),
                        dcc.Dropdown(options=[
                                        {'label': 'ACADEMIC', 'value': 'ACADEMIC'},
                                        {'label': 'TECHNICAL-VOCATIONAL-LIVELIHOOD', 'value': 'TVL'},
                                        {'label': 'ARTS AND DESIGN', 'value': 'ARTS'},
                                        {'label': 'SPORTS', 'value': 'SPORTS'}],
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

        ], className='primary-options dropdown-ctn'),
    ], id='seniorhigh-based-filter')
