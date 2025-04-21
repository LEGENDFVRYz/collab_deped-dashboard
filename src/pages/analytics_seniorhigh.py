from pydoc import classname
import dash
from dash import html
from dash import Dash, dcc, html

# --  Shared Components
from src.components.card import Card

# -- Graphs
from src.utils.reports.seniorhigh_chart import seniorhigh_distri_per_track ## Importing Charts
from src.utils.reports.seniorhigh_chart import seniorhigh_ratio_enrollment
from src.utils.reports.seniorhigh_chart import seniorhigh_most_least_enrolled
from src.utils.reports.seniorhigh_chart import seniorhigh_gender_distri
from src.utils.reports.seniorhigh_chart import seniorhigh_school_offering_per_track_by_sector
from src.utils.reports.seniorhigh_chart import seniorhigh_least_offered_high_demand
from src.utils.reports.seniorhigh_chart import sample_chart ## Importing Indicators


"""
    Template For Rendering the Location Reports:
    
"""


def render_seniorhigh_filter():
    return html.Div(
        children=[
            ## options
            html.Div([
                # LEFT SIDE CONTENTS
                html.Div([
                    # ENROLLMENT DISTRIBUTION
                    html.Div([
                        html.H4("SHS Enrollment Distribution"),
                        html.Div([
                            Card([
                                # distribution of enrollees per track
                                #########################################
                                ## Sample Use of Charts, Remove this After
                                dcc.Graph(id="seniorhigh_distri_per_track", className="seniorhigh_distri_per_track", figure=seniorhigh_distri_per_track,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100%"}
                                ),
                                #########################################
                            ], margin=False),
                        ], className="shs-enrollment-dist-graph"),
                        html.Div([
                            html.Div([
                                Card([
                                    # ratio enrollment in Academic vs. non-Academic tracks
                                    dcc.Graph(id="seniorhigh_ratio_enrollment", className="seniorhigh_ratio_enrollment", figure=seniorhigh_ratio_enrollment,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100%"}
                                ),
                                ], margin=False),
                            ], className="shs-enrollment-graph"),
                            html.Div([
                                Card([
                                    # most and least enrolled  (strand)
                                    dcc.Graph(id="seniorhigh_most_least_enrolled", className="seniorhigh_most_least_enrolled", figure=seniorhigh_most_least_enrolled,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100%"}
                                ),
                                ], margin=False),
                            ], className="shs-enrollment-graph"),
                            html.Div([
                                Card([
                                    # gender distribution
                                    dcc.Graph(id="seniorhigh_gender_distri", className="seniorhigh_gender_distri", figure=seniorhigh_gender_distri,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100%"}
                                ),
                                ], margin=False),
                            ], className="shs-enrollment-graph"),
                            
                        ], className="shs-enrollment-lower")
                    ], className="shs-enrollment"),
                    
                    # TRACK AVAILABILITY
                    html.Div([
                        html.H4("Track Availability"),
                        
                        html.Div([
                            html.Div([
                                Card([
                                    # differences in the number of schools offering each track
                                    dcc.Graph(id="seniorhigh_school_offering_per_track_by_sector", className="seniorhigh_school_offering_per_track_by_sector", figure=seniorhigh_school_offering_per_track_by_sector,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100%"}
                                ),
                                ], margin=False)
                            ], className="shs-track-avail-graph"),
                            html.Div([
                                Card([
                                    # which SHS tracks are least offered but in high demand
                                    dcc.Graph(id="seniorhigh_least_offered_high_demand", className="seniorhigh_least_offered_high_demand", figure=seniorhigh_least_offered_high_demand,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100%"}
                                ),
                                ], margin=False)
                            ], className="shs-track-avail-graph"),
                        ], className="shs-track-avail-content")
                        
                    ], className="shs-track-avail")
                ], className="shs-left-content"),
                
                # RIGHT SIDE CONTENTS
                # REGIONAL AND SECTOR-BASED DISTRIBUTION
                html.Div([
                    html.H4("Region and Sector-based Distribution"),
                    html.Div([
                        Card([
                            # how many schools offer each SHS track per region
                        ], margin=False),
                    ], className="shs-region-sector-graph"),
                    html.Div([
                        Card([
                            # which SHS tracks are more prevalent in each sector
                        ], margin=False),
                    ], className="shs-region-sector-graph"),
                    html.Div([
                        Card([
                            # do mother schools or annexes offer a wider range of SHS tracks
                        ], margin=False),
                    ], className="shs-region-sector-graph"),
                ], className="shs-right-content"),
                
            ], className="shs-content"),
        ], className='plotted-seniorhigh-report render-plot')