from dash import html, dcc


"""
    Template For Rendering the Location Reports:
    
"""


def render_seniorhigh_filter():
    return html.Div(
        children=[
            ## options
            html.Div([
                    html.H1(["SENIORHIGH SHEEESH!!!!!"])
            ]),
        ], className='plotted-seniorhigh-report render-plot')