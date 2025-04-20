from dash import html, dcc


"""
    Template for Senior High Filtering:
    
    
"""


def Offering_filter():
    return html.Div([
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

        ], className='primary-options dropdown-ctn'),
    ], id='offering-based-filter')
