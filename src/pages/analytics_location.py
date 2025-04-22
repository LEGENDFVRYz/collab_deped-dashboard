from dash import html, dcc
from src.components.card import Card


## Chart Callbacks
from src.utils.reports import location_chart


"""
    Template For Rendering the Location Reports:
    
"""


def render_location_filter():
    return html.Div(
        children=[
            ## LEFT SECTION
            html.Div([
                
                ## TOP SECTION
                html.Div([
                    html.Div(["Enrollees per Location"], className='label'),
                    html.Div([
                        
                        ## PLOT A
                        html.Div([Card([
                            #########################################
                            ## INSERT PLOT: Distribution of enrollees per location 
                            #########################################
                            
                            dcc.Loading(
                                id="loading-graph",
                                type="default",
                                children=html.Div([], id='location_enrollees-distribution-per-location',)
                            )
                            
                            #                             dcc.Loading(
                            #     id="loading-graph",
                            #     type="circle",
                            #     children=html.Div(
                            #         children=html.Div(
                            #             style={
                            #                 "height": "200px",
                            #                 "width": "80%",
                            #                 "backgroundColor": "#e6e6e6",
                            #                 "borderRadius": "8px",
                            #                 # "animation": "pulse 1.5s infinite",
                            #             }
                            #         ),
                            #         id='graph-container',
                            #         style={
                            #             'display': 'flex',
                            #             'justifyContent': 'center',
                            #             'alignItems': 'center',
                            #             'height': '300px'
                            #         }
                            #     ),
                            #     style={'padding': '1em'}
                            # )

                            
                            
                            # dcc.Graph(id="location_enrollees-distribution-per-location", 
                            #             # figure=gender_region_fig,
                            #             config={"responsive": True},
                            #             style={"width": "100%", "height": "100%"}
                            # )
                            
                        ], margin=False, padding='0.25em')], className='plot-a-section'),
                        
                        ## PLOT B
                        html.Div([
                            html.Div([Card([
                                #########################################
                                ## TABLE: highest and lowest number of enrollees
                                #########################################
                                
                                dcc.Loading(
                                    id="loading-graph",
                                    type="default",
                                    children=html.Div([
                                    ],id='location_highest_lowest_enrollees')
                                )
                                
                                #     dcc.Graph(id="location_highest_lowest_enrollees", 
                                #             # figure=hi_low_fig,
                                #             config={"responsive": True},
                                #             style={"width": "100%", "height": "100%", "display": "none"}
                                # )
                                
                            ], margin=False)], className='plot-b-box1'),
                            
                            html.Div([
                                    Card([
                                        html.Div([
                                            html.H1([], id="truncated-total-enrollees", className="truncated_total_enrollees"), 
                                            html.Span([], id="raw-total-enrollees", className="raw_total_enrollees"),
                                            html.Span("Total Enrollees", className="label_total_enrollees")
                                        ], className="total_enrollees")
                                    ], margin=False)
                                ], className='plot-b-box2'),

                            
                            html.Div([Card([
                                    html.H1([], id="truncated-total-schools", className="truncated_total_schools"), 
                                    html.Span([], id="raw-total-schools", className="raw_total_schools"),
                                ], margin=False)], className='plot-b-box2'),
                        ], className='plot-b-section'),
                    ], className='track-box plot-content')
                ], className='plot-top-section plot-sec-wrap'),
                
                ## BOTTOM SECTION
                html.Div([
                    html.Div(["Strand/Track Preferences"], className='label'),
                    html.Div([Card([
                        #########################################
                        ## INSERT PLOT: Strand preferences per region
                        #########################################
                        
                        dcc.Loading(
                            id="loading-graph",
                            type="default",
                            children=html.Div([
                            ],id='track-preference-heatmap')
                        )
                        # dcc.Graph(
                        #     id="track-preference-heatmap",
                        #     # figure=heatmap_fig,
                        #     config={"responsive": True},
                        #     style={"width": "100%", "height": "100%", "display": "none"}
                        # )

                        
                    ], margin=False)], className='plot-content')
                ], className='plot-bottom-section plot-sec-wrap'),
            ], className='plot-left-section'),
            
            
            ## RIGHT SECTION
            html.Div([
                
                ## TOP SECTION
                html.Div([
                    html.Div(["Geographic Distribution"], className='label'),
                    html.Div([Card([
                        #########################################
                        ## INSERT PLOT: enrollment density (students per location)
                        #########################################
                        
                        
                        ], margin=False)], className='plot-content')
                ], className='plot-top-section plot-sec-wrap'),
                
                ## BOT SECTION
                html.Div([
                    html.Div(["School Type Analysis"], className='label'),
                    html.Div([Card([
                        #########################################
                        ## INSERT PLOT: school sectors
                        #########################################
                        dcc.Loading(
                            id="loading-graph",
                            type="default",
                            children=html.Div([], id='location_school_sectors',)
                        ),
                    ], margin=False)], className='plot-content')
                ], className='plot-bottom-section plot-sec-wrap'),
            ], className='plot-right-section'), 
            
        ], className='plotted-location-report render-plot')