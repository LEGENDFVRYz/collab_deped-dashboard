from dash import html

"""
    Template for Dash Application:
    
    Plcaholder for main content section

"""


def Card(children=[], margin=True, padding='1em', **kwargs):
    # Styles: Box Container
    margin = '0.5em' if margin else '0em'
    
    box_styles = {
        # Default Stylings
        'background-color': '#FFFFFF',
        'width': 'inherit',
        'height': '100%',
        'display': 'flex',
        'flex': '1',
        
        'box-sizing': 'content-box',
        'border-radius': '0.75em',
        'margin': margin,
        'box-shadow' : '-2px 0px 6px rgba(0, 0, 0, 0.03)'    
    }
    
    return html.Div(
        children=[
            
            html.Div(children, className='card-wrap', style={
                'padding': padding,
                'display': 'flex',
                'flex-direction': 'column',
                'flex': '1'
            })
            
            ], 
        className='card',
        style=box_styles,
        **kwargs)
