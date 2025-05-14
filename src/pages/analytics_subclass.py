from dash import html, dcc
from src.components.card import Card

## Chart Callbacks
from src.utils.reports import subclass_chart


# """
#     Template For Rendering the Location Reports:
    
# """


def render_subclass_filter():
    return html.Div(
        children=[
            ## options
            html.Div([
                # # LEFT SIDE CONTENTS
                # # ENROLLMENT PROFILE PER SUBCLASSIFICATION
                # html.Div([
                #     html.H4("Enrollment Profile per Subclassification"),
                #     html.Div([
                #         # Card([
                #         #     # total schools per subclass
                #         #     html.H4(["Total Schools per Subclassification"], className="subclass-graph-title"),
                #         #     # dcc.Loading(
                #         #     #     id="loading-graph",
                #         #     #     type="default",
                #         #     #     children=
                #         #         html.Div([],id='subclass_total_schools_per_subclass',)
                #         #     # ),
                #         #     # dcc.Graph(id="subclass_total_schools_per_subclass", 
                #         #     #     figure=total_schools_per_subclass,
                #         #     #     config={"responsive": True},
                #         #     #     style={"width": "100%", "height": "100%"}
                #         #     # ),
                #         # ], margin=False)
                #     ], className="subclass-enroll-graph"),

                #     html.Div([
                #         Card([
                #             html.H4(["Enrollment Distribution by Subclassification"], className="subclass-graph-title"),
                #             # dcc.Loading(
                #             #     id="loading-graph",
                #             #     type="default",
                #                 # children=
                #                 html.Div([],id='subclass_distrib_by_subclass',)
                #             # ),
                #             # enrollment distribution by subclass
                #             # dcc.Graph(id="subclass_distrib_by_subclass", 
                #             #     figure=distrib_by_subclass,
                #             #     config={"responsive": True},
                #             #     style={"width": "100%", "height": "100%"}
                #             # ),
                #         ], margin=False)
                #     ], className="subclass-enroll-graph"),

                # ], className="subclass-left-content"),
                
                # RIGHT SIDE CONTENTS
                html.Div([
                    # DISTRIBUTION AND AVAILABILITY
                    html.Div([
                        # html.H4("Distribution and Availability"),
                        html.Div([
                            Card([
                                # subclass vs school type
                                html.H4(["School Subclassification Breakdown by Type and Curriculum Mode ", html.Span([" Logarithm ▼ "], id="log-button-sc", n_clicks=0),], className="subclass-graph-title"), 
                                # dcc.Loading(
                                #     id="loading-graph",
                                #     type="default",
                                #     children=
                                    html.Div([], id='subclass_vs_school_type', className='chart-ctn-sc')
                                # ),   
                                # dcc.Graph(id="subclass_vs_school_type", 
                                #     figure=subclass_vs_school_type,
                                #     config={"responsive": True},
                                #     style={"width": "100%", "height": "100%"}
                                # ),    
                            ], margin=False)
                        ], className="subclass-dist-avail-graph"),
                        
                        html.Div([
                            html.Div([
                                # Card([
                                    # sector affiliation
                                    # html.H4(["Sector Affiliation"], className="subclass-graph-title"),
                                    # dcc.Loading(
                                    #     id="loading-graph",
                                    #     type="default",
                                    #     children=
                                        html.Div([],id='subclass_sector_affiliation', className='chart-ctn-sc')
                                    # ),  
                                    # dcc.Graph(id="subclass_sector_affiliation", 
                                    #     figure=sector_affiliation,
                                    #     config={"responsive": True},
                                    #     style={"width": "100%", "height": "100%"}
                                    # ),
                                # ], margin=False)
                            ], className="subclass-dist-avail-graph-1"),
                            html.Div([
                                Card([
                                    # regional distribution/ which subclass has the highest number of schools per loc
                                    html.H4(["Regional Distribution of Schools"], className="subclass-graph-title"),
                                    # dcc.Loading(
                                    #     id="loading-graph",
                                    #     type="default",
                                    #     children=
                                        html.Div([],id='subclass_student_school_ratio', className='chart-ctn-sc')
                                    # ), 
                                    # dcc.Graph(id="subclass_heatmap", figure=subclass_heatmap,
                                    # config={"responsive": True},
                                    # style={"width": "100%", "height": "100%"}
                                    # ),
                                ], margin=False)
                            ], className="subclass-dist-avail-graph-2"),
                        ], className="subclass-dist-avail-lower")
                        
                    ], className="subclass-dist-avail"),
                    
                    # PROGRAM AND GRADE LEVEL OFFERINGS
                    html.Div([
                        html.H4("Program and Grade Level Offerings"),
                        html.Div([
                            html.Div([
                                # html.Div([
                                #     Card([
                                #         # mcoc breakdown/which subclass offers which program types
                                #         # dcc.Loading(
                                #         #     id="loading-graph",
                                #         #     type="default",
                                #         #     children=
                                #             html.Div([],id='subclass_clustered',)
                                #         # ),  
                                #         # dcc.Graph(id="subclass_clustered", figure=subclass_clustered,
                                #         # config={"responsive": True},
                                #         # style={"width": "100%", "height": "100%"}
                                #         # ),
                                #     ], margin=False),
                                # ], className="subclass-program-graph"),
                                
                                html.Div([
                                    Card([
                                        
                                        html.Div(
                                            [
                                                html.Div([
                                                    html.Div(
                                                        [
                                                            html.Div([], id="max-sc-dist"),
                                                            html.Div([], id="name-max-sc-dist"),
                                                            html.Div([], id="max-sc-dist-value"),
                                                        ]
                                                    , className='tag-wrap')
                                                    
                                                    ],id='subclass_dist_tag', className='chart-ctn-sc'),
                                                
                                                html.Div([],id='subclass_distrib_by_subclass', className='chart-ctn-sc'),
                                                
                                                html.Div([
                                                        html.H3([html.Span([f"0.49% Others"], id="sc-dist-tag", className="lfury-highlight"), " in Detailed:"]),
                                                        html.Div([], id='others_subclass_distrib_by_subclass')
                                                    
                                                    ], className='detailed-sc chart-ctn-sc'),
                                                
                                            ]
                                        , className='subdist-wrap'),
                                        
                                        # enrollment in shs tracks across subclass
                                        # dcc.Loading(
                                        #     id="loading-graph",
                                        #     type="default",
                                        #     children=
                                            # html.Div([],id='subclass_clustered_tracks',)
                                        # ),
                                        # dcc.Graph(id="subclass_clustered_tracks", figure=subclass_clustered_tracks,
                                            # config={"responsive": True},
                                            # style={"width": "100%", "height": "100%"}
                                        # ),
                                    ], margin=False),
                                ], className="subclass-program-graph"),
                            ], className="subclass-program-graph-left"),

                            # html.Div(
                            #     className="subclass-percentage",  # Updated to match the new class name
                            #     children=[
                            #         # Row 1: Displaying the percentage of "All Offering" schools
                            #         html.Div(className="row", children=[
                            #             html.Div(className="col", children=[
                            #                 Card([
                            #                     html.H6("Top 'All Offering' by Subclass"),
                            #                     html.Span([], id="top_offering_subclass", className="subclass-percentage"),
                            #                     html.Span([], id="top_offering_percentage", className="subclass-percentage-value"),
                            #                     # html.P("schools offering all programs", className="sub-text"),
                            #                 ], margin=False)
                            #             ]),
                            #         ]),
                            #         html.Div(className="row", children=[
                            #             html.Div(className="col", children=[
                            #                 Card([
                            #                     html.H6("Top SHS Track Coverage by Subclass"),
                            #                     html.Span([], id="top_track_subclass", className="subclass-percentage"),
                            #                     html.Span([], id="top_track_percentage", className="subclass-percentage-value"),
                            #                     # html.P("track coverage", className="sub-text"),
                            #                 ], margin=False)
                            #             ]),
                            #         ]),
                            #     ]
                            # )                            
                        ], className="subclass-program-contents"),
                    ], className="subclass-program"),
                    
                ], className="subclass-right-content")
                
                
            ], className="subclass-content"),
        ], className='plotted-subclass-report render-plot')
    
    
    
def new_subclass_offering():
    return html.Div(
        children=[
            ## LEFT SECTION
            "NEWW subclass"
            
        ], className='plotted-location-report render-plot')