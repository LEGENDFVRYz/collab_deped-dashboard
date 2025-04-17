from dash import html, dcc


"""
    Template For Rendering the Location Reports:
    
"""


def render_location_filter():
    return html.Div(
        children=[
            ## options
            html.Div([
                    html.H1(["LOKASYOONN!!!!!"])
            ]),
        ], className='plotted-location-report render-plot')