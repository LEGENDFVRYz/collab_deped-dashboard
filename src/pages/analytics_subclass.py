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
from src.utils.reports.subclass_chart import avg_enroll_dost, avg_enroll_deped, avg_enroll_luc, avg_enroll_int, avg_enroll_nonsec, avg_enroll_ga, avg_enroll_abroad, avg_enroll_suc, avg_enroll_sec 
from src.utils.reports.subclass_chart import total_schools_per_subclass, distrib_by_subclass, student_school_ratio, subclass_vs_school_type, sector_affiliation


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
                            dcc.Graph(id="subclass_total_schools_per_subclass", 
                                figure=total_schools_per_subclass,
                                config={"responsive": True},
                                style={"width": "100%", "height": "100%"}
                            ),
                        ], margin=False)
                    ], className="subclass-enroll-graph"),

                    html.Div([
                        Card([
                            # enrollment distribution by subclass
                            dcc.Graph(id="subclass_distrib_by_subclass", 
                                figure=distrib_by_subclass,
                                config={"responsive": True},
                                style={"width": "100%", "height": "100%"}
                            ),
                        ], margin=False)
                    ], className="subclass-enroll-graph"),

                    html.Div([
                        html.Div([
                            Card([
                                # student-to-school ratio    
                                dcc.Graph(id="student_school_ratio", 
                                figure=student_school_ratio,
                                config={"responsive": True},
                                style={"width": "100%", "height": "100%"}
                                ),
                            ], margin=False)
                        ], className="subclass-enroll-graph"),
                        html.Div( 
                            # average enrollees per school
                            #html.H5("Average per Subclassification"),
                            children=[
                                html.Div(
                                    className="subclass-enroll-indcard", 
                                    children=[
                                        # Row 1
                                        html.Div(className="row", children=[
                                            html.Div(className="col", children=[
                                                Card([ #A1
                                                    html.H6("DOST Managed"),
                                                    html.Span(f"{avg_enroll_dost}", className="subclass-enroll-ind"),
                                                    html.H6("average enrollees"),
                                                ], margin=False)
                                            ]),
                                            html.Div(className="col", children=[
                                                Card([ #B1
                                                    html.H6("Local Int'l School"),
                                                    html.Span(f"{avg_enroll_int}", className="subclass-enroll-ind"),
                                                    html.H6("average enrollees"),
                                                ], margin=False)
                                            ]),
                                            html.Div(className="col", children=[
                                                Card([ #C1
                                                    html.H6("School Abroad"),
                                                    html.Span(f"{avg_enroll_abroad}", className="subclass-enroll-ind"),
                                                    html.H6("average enrollees"),
                                                ], margin=False)
                                            ]),
                                        ]),
                                        # Row 2
                                        html.Div(className="row", children=[
                                            html.Div(className="col", children=[
                                                Card([ #A2
                                                    html.H6("DepED Managed"),
                                                    html.Span(f"{avg_enroll_deped}", className="subclass-enroll-ind"),
                                                    html.H6("average enrollees"),
                                                ], margin=False)
                                            ]),
                                            html.Div(className="col", children=[
                                                Card([ #B2
                                                    html.H6("Non-Sectarian"),
                                                    html.Span(f"{avg_enroll_nonsec}", className="subclass-enroll-ind"),
                                                    html.H6("average enrollees"),
                                                ], margin=False)
                                            ]),
                                            html.Div(className="col", children=[
                                                Card([ #C2
                                                    html.H6("SUC Managed"),
                                                    html.Span(f"{avg_enroll_suc}", className="subclass-enroll-ind"),
                                                    html.H6("average enrollees"),
                                                ], margin=False)
                                            ]),
                                        ]),
                                        # Row 3
                                        html.Div(className="row", children=[
                                            html.Div(className="col", children=[
                                                Card([ #A3
                                                    html.H6("LUC Managed"),
                                                    html.Span(f"{avg_enroll_luc}", className="subclass-enroll-ind"),
                                                    html.H6("average enrollees"),
                                                ], margin=False)
                                            ]),
                                            html.Div(className="col", children=[
                                                Card([ #B3
                                                    html.H6("Other GA Mgd."),
                                                    html.Span(f"{avg_enroll_ga}", className="subclass-enroll-ind"),
                                                    html.H6("average enrollees"),
                                                ], margin=False)
                                            ]),
                                            html.Div(className="col", children=[
                                                Card([ #C3
                                                    html.H6("Sectarian"),
                                                    html.Span(f"{avg_enroll_sec}", className="subclass-enroll-ind"),
                                                    html.H6("average enrollees"),
                                                ], margin=False)
                                            ]),
                                        ]),
                                    ]
                                )
                            ]
                        ) ###
                    ], className="subclass-enroll-middle"),
                ], className="subclass-left-content"),
                
                # RIGHT SIDE CONTENTS
                html.Div([
                    # DISTRIBUTION AND AVAILABILITY
                    html.Div([
                        html.H4("Distribution and Availability"),
                        html.Div([
                            Card([
                                # subclass vs school type
                                dcc.Graph(id="subclass_vs_school_type", 
                                    figure=subclass_vs_school_type,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100%"}
                                ),    
                            ], margin=False)
                        ], className="subclass-dist-avail-graph"),
                        
                        html.Div([
                            html.Div([
                                Card([
                                    # sector affiliation
                                    dcc.Graph(id="sector_affiliation", 
                                    figure=sector_affiliation,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100%"}
                                ),
                                ], margin=False)
                            ], className="subclass-dist-avail-graph-1"),
                            html.Div([
                                Card([
                                    # regional distribution/ which subclass has the highest number of schools per loc
                                    dcc.Graph(id="subclass_heatmap", figure=subclass_heatmap,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100"}
                                    ),
                                ], margin=False)
                            ], className="subclass-dist-avail-graph-2"),
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