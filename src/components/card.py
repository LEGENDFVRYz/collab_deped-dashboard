from dash import html

"""
    Template for Dash Application:
    
    Plcaholder for main content section

"""


def Card(children=[], **kwargs):
    # Styles: Box Container
    box_styles = {
        # Default Stylings
        'background-color': '#FFFFFF',
        'width': 'inherit',
        'height': '100%',
        'display': 'flex',
        'flex': '1',
        
        'box-sizing': 'content-box',
        'border-radius': '1em',
        'margin': '0.5em',
        # 'box-shadow' : '10px 10px 25px #f0f0f0, -10px -10px 25px #565856'
    }
    
    return html.Div(
        children=[
            
            html.Div(children, className='card-wrap', style={
                'padding': '1em',
                'display': 'flex',
                'flex-direction': 'column',
                'flex': '1'
            })
            
            ], 
        className='card',
        style=box_styles,
        **kwargs)
