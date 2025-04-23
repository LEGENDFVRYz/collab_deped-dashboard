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
                # LEFT SIDE CONTENTS
                # ENROLLMENT PROFILE PER SUBCLASSIFICATION
                html.Div([
                    html.H4("Enrollment Profile per Subclassification"),
                    html.Div([
                        Card([
                            # total schools per subclass
                            html.H4(["Total Schools per Subclassification"], className="subclass-graph-title"),
                            dcc.Loading(
                                id="loading-graph",
                                type="default",
                                children=html.Div([],id='subclass_total_schools_per_subclass',)
                            ),
                            # dcc.Graph(id="subclass_total_schools_per_subclass", 
                            #     figure=total_schools_per_subclass,
                            #     config={"responsive": True},
                            #     style={"width": "100%", "height": "100%"}
                            # ),
                        ], margin=False)
                    ], className="subclass-enroll-graph"),

                    html.Div([
                        Card([
                            html.H4(["Enrollment Distribution by Subclassification"], className="subclass-graph-title"),
                            dcc.Loading(
                                id="loading-graph",
                                type="default",
                                children=html.Div([],id='subclass_distrib_by_subclass',)
                            ),
                            # enrollment distribution by subclass
                            # dcc.Graph(id="subclass_distrib_by_subclass", 
                            #     figure=distrib_by_subclass,
                            #     config={"responsive": True},
                            #     style={"width": "100%", "height": "100%"}
                            # ),
                        ], margin=False)
                    ], className="subclass-enroll-graph"),

                    html.Div([
                        # Column 1
                        html.Div(className="subclass-col1", children=[
                            # Row 1: Graph
                            html.Div([
                                Card([
                                    # student to school ratio
                                    html.H4(["Student-to-School Ratio"], className="subclass-graph-title"),
                                    dcc.Loading(
                                        id="loading-graph",
                                        type="default",
                                        children=html.Div([],id='subclass_student_school_ratio',)
                                    ), 
                                ], margin=False)
                            ], className="subclass-enroll-scatter"),

                            # Row 2: Indicator Cards B2-C2
                            html.Div(className="subclass-row", children=[
                                # B2
                                html.Div([
                                    Card([
                                        html.Div([
                                            html.Div([
                                                html.Span(),
                                                html.H6("Non-Sectarian", className="sei-label"),
                                            ]),
                                            html.Span([], id="subclass-enroll-nonsec", className="sei-count"),
                                            html.P("average enrollees", className="sei-text"),
                                        ], className="subclass-enroll-ind")
                                    ], margin=False)
                                ]),
                                # B3
                                html.Div([
                                    Card([
                                        html.Div([
                                            html.Div([
                                                html.Span(),
                                                html.H6("Other GA Mgd.", className="sei-label"),
                                            ]),
                                            html.Span([], id="subclass-enroll-ga", className="sei-count"),
                                            html.P("average enrollees", className="sei-text"),
                                        ], className="subclass-enroll-ind")
                                    ], margin=False)
                                ]),
                                # C1
                                html.Div([
                                    Card([
                                        html.Div([
                                            html.Div([
                                                html.Span(),
                                                html.H6("School Abroad", className="sei-label"),
                                            ]),
                                            html.Span([], id="subclass-enroll-abroad", className="sei-count"),
                                            html.P("average enrollees", className="sei-text"),
                                        ], className="subclass-enroll-ind")
                                    ], margin=False)
                                ]),
                                # C2
                                html.Div([
                                    Card([
                                        html.Div([
                                            html.Div([
                                                html.Span(),
                                                html.H6("SUC Managed", className="sei-label"),
                                            ]),
                                            html.Span([], id="subclass-enroll-suc", className="sei-count"),
                                            html.P("average enrollees", className="sei-text"),
                                        ], className="subclass-enroll-ind")
                                    ], margin=False)
                                ]),
                            ]),
                        ]),

                        # Column 2
                        html.Div(className="subclass-col2", children=[
                            # Row 1: Indicator Cards A1-B1  
                            # A1
                            html.Div([
                                Card([
                                    html.Div([
                                        html.Div([
                                            html.Span(),
                                            html.H6("DOST Managed", className="sei-label"),
                                        ]),
                                        html.Span([], id="subclass-enroll-dost", className="sei-count"),
                                        html.P("average enrollees", className="sei-text"),
                                    ], className="subclass-enroll-ind")
                                ], margin=False)
                            ]),
                            # A2
                            html.Div([
                                Card([
                                    html.Div([
                                        html.Div([
                                            html.Span(),
                                            html.H6("DepED Managed", className="sei-label"),
                                        ]),
                                        html.Span([], id="subclass-enroll-deped", className="sei-count"),
                                        html.P("average enrollees", className="sei-text"),
                                    ], className="subclass-enroll-ind")
                                ], margin=False)
                            ]),
                            # A3
                            html.Div([
                                Card([
                                    html.Div([
                                        html.Div([
                                            html.Span(),
                                            html.H6("LUC Managed", className="sei-label"),
                                        ]),
                                        html.Span([], id="subclass-enroll-luc", className="sei-count"),
                                        html.P("average enrollees", className="sei-text"),
                                    ], className="subclass-enroll-ind")
                                ], margin=False)
                            ]),
                            # B1
                            html.Div([
                                Card([
                                    html.Div([
                                        html.Div([
                                            html.Span(),
                                            html.H6("Local Int'l School", className="sei-label"),
                                        ]),
                                        html.Span([], id="subclass-enroll-int", className="sei-count"),
                                        html.P("average enrollees", className="sei-text"),
                                    ], className="subclass-enroll-ind")
                                ], margin=False)
                            ]),
                            # C3
                            html.Div([
                                Card([
                                    html.Div([
                                        html.Div([
                                            html.Span(),
                                            html.H6("Sectarian", className="sei-label"),
                                        ]),
                                        html.Span([], id="subclass-enroll-sec", className="sei-count"),
                                        html.P("average enrollees", className="sei-text"),
                                    ], className="subclass-enroll-ind")
                                ], margin=False)
                            ])
                        ])
                    ], className="subclass-enroll-middle")
                ], className="subclass-left-content"),
                
                # RIGHT SIDE CONTENTS
                html.Div([
                    # DISTRIBUTION AND AVAILABILITY
                    html.Div([
                        html.H4("Distribution and Availability"),
                        html.Div([
                            Card([
                                # subclass vs school type
                                html.H4(["Subclassification by School Type Distribution"], className="subclass-graph-title"),
                                dcc.Loading(
                                    id="loading-graph",
                                    type="default",
                                    children=html.Div([],id='subclass_vs_school_type',)
                                ),   
                                # dcc.Graph(id="subclass_vs_school_type", 
                                #     figure=subclass_vs_school_type,
                                #     config={"responsive": True},
                                #     style={"width": "100%", "height": "100%"}
                                # ),    
                            ], margin=False)
                        ], className="subclass-dist-avail-graph"),
                        
                        html.Div([
                            html.Div([
                                Card([
                                    # sector affiliation
                                    html.H4(["Sector Affiliation"], className="subclass-graph-title"),
                                    dcc.Loading(
                                        id="loading-graph",
                                        type="default",
                                        children=html.Div([],id='subclass_sector_affiliation',)
                                    ),  
                                    # dcc.Graph(id="subclass_sector_affiliation", 
                                    #     figure=sector_affiliation,
                                    #     config={"responsive": True},
                                    #     style={"width": "100%", "height": "100%"}
                                    # ),
                                ], margin=False)
                            ], className="subclass-dist-avail-graph-1"),
                            html.Div([
                                Card([
                                    # regional distribution/ which subclass has the highest number of schools per loc
                                    html.H4(["Regional Distribution of Schools"], className="subclass-graph-title"),
                                    dcc.Loading(
                                        id="loading-graph",
                                        type="default",
                                        children=html.Div([],id='subclass_heatmap',)
                                    ), 
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
                                html.Div([
                                    Card([
                                        # mcoc breakdown/which subclass offers which program types
                                        dcc.Loading(
                                            id="loading-graph",
                                            type="default",
                                            children=html.Div([],id='subclass_clustered',)
                                        ),  
                                        # dcc.Graph(id="subclass_clustered", figure=subclass_clustered,
                                        # config={"responsive": True},
                                        # style={"width": "100%", "height": "100%"}
                                        # ),
                                    ], margin=False),
                                ], className="subclass-program-graph"),
                                
                                html.Div([
                                    Card([
                                        # enrollment in shs tracks across subclass
                                        dcc.Loading(
                                            id="loading-graph",
                                            type="default",
                                            children=html.Div([],id='subclass_clustered_tracks',)
                                        ),
                                        # dcc.Graph(id="subclass_clustered_tracks", figure=subclass_clustered_tracks,
                                            # config={"responsive": True},
                                            # style={"width": "100%", "height": "100%"}
                                        # ),
                                    ], margin=False),
                                ], className="subclass-program-graph"),
                            ], className="subclass-program-graph-left"),

                            html.Div(
                                className="subclass-percentage",  # Updated to match the new class name
                                children=[
                                    # Row 1: Displaying the percentage of "All Offering" schools
                                    html.Div(className="row", children=[
                                        html.Div(className="col", children=[
                                            Card([
                                                html.H6("Top 'All Offering' Subclass"),
                                                html.Span([], id="top_offering_subclass", className="subclass-percentage"),
                                                html.Span([], id="top_offering_percentage", className="subclass-percentage"),
                                                html.H6("schools offering all programs"),
                                            ], margin=False)
                                        ]),
                                    ]),
                                    html.Div(className="row", children=[
                                        html.Div(className="col", children=[
                                            Card([
                                                html.H6("Top SHS Track Coverage Subclass"),
                                                html.Span([], id="top_track_subclass", className="subclass-percentage"),
                                                html.Span([], id="top_track_percentage", className="subclass-percentage"),
                                                html.H6("track coverage"),
                                            ], margin=False)
                                        ]),
                                    ]),
                                ]
                            )                            
                        ], className="subclass-program-contents"),
                    ], className="subclass-program"),
                    
                ], className="subclass-right-content")
                
            ], className="subclass-content"),
        ], className='plotted-subclass-report render-plot')