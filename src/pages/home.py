import dash
from dash import html
from dash import Dash, dcc, html

# --  Shared Components
from src.components.card import Card

# -- Graphs
from src.utils.reports.home_enrollment_per_region import format_large_number
from src.utils.reports.home_enrollment_per_region import home_enrollment_per_region, track_ratio_per_track
from src.utils.reports.home_enrollment_per_region import total_enrollees, most_active, least_active, academic_track_ratio

# Landing page
dash.register_page(__name__, path="/")  

layout = html.Div([
    ## -- Standard: Page Content Header
    html.Div([
        html.H1('Overview')
    ], className='page-header'),
    
    html.Div([
            ## -- Main Part
    html.Div([
        html.Div([
            ## --> Sub layer
            html.Div([Card(
                    [
                        ## -- GRAPH: Total Enrollment Count per School Level
                        html.Div(["Enrollments per School Level"], className='header'),
                        html.Div([
                            dcc.Graph(id="home_enrollment-per-region", figure=home_enrollment_per_region,
                                            config={"responsive": True},
                                            style={"width": "100%", "height": "100%"}
                                      )
                        ], className='graph'),
                    ]
                )], className='area-1'),
            html.Div([
                    html.Div([Card([
                            # -- INDICATOR: TOTAL ENROLEES IN PH
                            html.Div([
                                    html.Div([html.H1(f"{total_enrollees}", className="text-center"),], className='indicator'),
                                    html.Div([html.Img(src='/assets/images/icons_navigation/team-fill.svg')], className='indicator-display'),
                                ], className='display'),
                            html.Div(['TOTAL ENROLLEES'], className='details')
                        ])], className='loc-1'),
                    html.Div([Card([
                        html.Div([
                                # -- INDICATOR: Most Active School Level
                                html.Div([
                                        html.Div([html.H1(f"{format_large_number(most_active['counts'])}", className="text-center"),], className='indicator'),
                                        html.Div([html.Img(src='/assets/images/icons_navigation/arrow-right-up-fill.svg')], className='indicator-display'),
                                    ], className='display'),
                            ], className='upper'),
                        html.Div([
                                # -- INDICATOR: Most Active School Level
                                html.Div([
                                        html.Div([html.H1(f"{format_large_number(least_active['counts'])}", className="text-center"),], className='indicator'),
                                        html.Div([html.Img(src='/assets/images/icons_navigation/arrow-left-down-fill.svg')], className='indicator-display'),
                                    ], className='display'),
                            ], className='lower')
                    ])], className='loc-2'),
                ], className='area-2'),
        ], className='layer-1'),
        html.Div([Card(
            
            
        )], className='layer-2')
    ], className='main-section'),
    
    ## -- Side Part
    html.Div([
        html.Div([
                Card(
                    [
                        ## -- GRAPH: Ratio distribution of shs strand
                        html.Div([html.H3(f"Academic Track is roughly {academic_track_ratio * 100:.2f}%")], className='header'),
                        html.Div([
                            dcc.Graph(id="track-ratio-per-track", figure=track_ratio_per_track,
                                            config={"responsive": True},
                                            style={"height": "100%"}
                                      )
                        ], className='graph'),
                    ]
            )], className='layer-1'),
            html.Div([
                    Card()
                ], className='layer-2')
        ], className='side-section')
    ], className='content')
], className='home-page container')