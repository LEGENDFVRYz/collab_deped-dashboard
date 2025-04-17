from dash import html, dcc


"""
    Template for Senior High Filtering:
    
    
"""


def Subclass_filter():
    return html.Div(
        children=[
            ## options
            html.Div([
                        html.Div(['Sub Classification:'], className='label'),
                        dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Region')
                    ], className='dropdown-opt-box'),
            
            
        ], className='primary-options')
