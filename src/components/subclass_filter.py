from dash import html, dcc


"""
    Template for Sub Class Filtering:
    
    
"""


def Subclass_filter():
    return html.Div([
        html.Div([
            
            # Subclassification
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
        ], className='primary-options dropdown-ctn'),
    ], id='subclass-based-filter')
