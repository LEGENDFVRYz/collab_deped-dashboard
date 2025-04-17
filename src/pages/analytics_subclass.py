from dash import html, dcc


"""
    Template For Rendering the Location Reports:
    
"""


def render_subclass_filter():
    return html.Div(
        children=[
            ## options
            html.Div([
                    html.H1(["SUBCLASS SHEEESH!!!!!"])
            ]),
        ], className='plotted-subclass-report render-plot')