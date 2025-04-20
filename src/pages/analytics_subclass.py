from pydoc import classname
from re import sub
import dash
from dash import html
from dash import Dash, dcc, html

# --  Shared Components
from src.components.card import Card

# -- Graphs
from src.utils.reports.subclass_chart import subclass_heatmap ## Importing Heatmap
from src.utils.reports.subclass_chart import subclass_clustered ## Importing Clustered Bar Chart
from src.utils.reports.subclass_chart import subclass_clustered_tracks ## Importing Clustered Bar Chart for Tracks
from src.utils.reports.subclass_chart import subclass_firstindicator ## Importing First Indicator Chart
from src.utils.reports.subclass_chart import subclass_secondindicator ## Importing Second Indicator Chart
"""
    Template For Rendering the Location Reports:
    
"""


def render_subclass_filter():
    return html.Div(
        children=[
            ## options
            html.Div([
                # LEFT SIDE CONTENTS
                # ENROLLMENT PROFILE PER SUBCLASSIFICATION
                html.Div([
                    html.H4("Enrollment Profile per Subclassification"),
                    html.Div([
                        Card([
                            # total schools per subclass
                            #########################################
                            ## Sample Use of Charts, Remove this After
                            # dcc.Graph(id="sample_chart", figure=sample_chart,
                            #     config={"responsive": True},
                            #     style={"width": "100%", "height": "100%"}
                            # ),
                            #########################################
                        ], margin=False)
                    ], className="subclass-enroll-graph"),
                    
                    html.Div([
                        html.Div([
                            Card([
                                # enrollment distribution by subclass
                            ], margin=False)
                        ], className="subclass-enroll-graph"),
                        html.Div([
                            Card([
                                # average enrollment per school
                            ], margin=False)
                        ], className="subclass-enroll-graph")
                    ], className="subclass-enroll-middle"),
                    
                    html.Div([
                        Card([
                            # student-to-school ratio
                        ], margin=False)
                    ], className="subclass-enroll-graph")
                ], className="subclass-left-content"),
                
                # RIGHT SIDE CONTENTS
                html.Div([
                    # DISTRIBUTION AND AVAILABILITY
                    html.Div([
                        html.H4("Distribution and Availability"),
                        html.Div([
                            Card([
                                # subclass vs school type
                            ], margin=False)
                        ], className="subclass-dist-avail-graph"),
                        
                        html.Div([
                            html.Div([
                                Card([
                                    # sector affiliation
                                ], margin=False)
                            ], className="subclass-dist-avail-graph"),
                            html.Div([
                                Card([
                                    # regional distribution/ which subclass has the highest number of schools per loc
                                    dcc.Graph(id="subclass_heatmap", figure=subclass_heatmap,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100"}
                                    ),
                                ], margin=False)
                            ], className="subclass-dist-avail-graph"),
                        ], className="subclass-dist-avail-lower")
                        
                    ], className="subclass-dist-avail"),
                    
                    # PROGRAM AND GRADE LEVEL OFFERINGS
                    html.Div([
                        html.H4("Program and Grade Level Offerings"),
                        html.Div([
                            html.Div([
                                Card([
                                    # mcoc breakdown/which subclass offers which program types
                                    dcc.Graph(id="subclass_clustered", figure=subclass_clustered,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100%"}
                                    ),
                                ], margin=False),
                            ], className="subclass-program-graph"),
                            
                            html.Div([
                                Card([
                                    # enrollment in shs tracks across subclass
                                    dcc.Graph(id="subclass_clustered_tracks", figure=subclass_clustered_tracks,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100%"}
                                    ),
                                ], margin=False),
                            ], className="subclass-program-graph"),
                            
                            html.Div([
                                html.Div([
                                    Card([
                                        # % schools offering ‘all offerings’ per subclass
                                        dcc.Graph(id="subclass_firstindicator", figure=subclass_firstindicator,
                                        config={"responsive": True},
                                        style={"width": "100%", "height": "100%"}
                                        ),
                                    ], margin=False),
                                ], className="subclass-program-indicator"),
                                html.Div([
                                    Card([
                                        # % schools offering shs per subclass
                                        dcc.Graph(id="subclass_secondindicator", figure=subclass_secondindicator,
                                        config={"responsive": True},
                                        style={"width": "100%", "height": "100%"}
                                        ),
                                    ], margin=False),
                                ], className="subclass-program-indicator"),
                            ], className="subclass-program-last-cards")
                            
                        ], className="subclass-program-contents"),
                    ], className="subclass-program"),
                    
                ], className="subclass-right-content")
                
            ], className="subclass-content"),
        ], className='plotted-subclass-report render-plot')