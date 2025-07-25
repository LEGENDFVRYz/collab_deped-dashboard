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
            html.Div(
                [
                    ## LEFT SECTION
                    html.Div([Card([
                        
                        ## TOP SECTION
                        html.Div([
                            # html.H3(["Enrollees per Location"], className='label'),
                            html.Div([
                                ## PLOT B
                                html.Div([
                                    
                                    html.Div([
                                        html.Div([
                                        Card([
                                            html.Div([
                                                html.Div([
                                                    html.Span("", className="hi-glevel-marker hi-enrollees"),
                                                    html.Img(src="/assets/images/icons_navigation/person-white.svg"),
                                                    html.H1([], id="truncated-average-enrollees", className="hi-truncated_total_enrollees"),
                                                ], className="hi-glevel-count"),
                                                html.Span([], id="raw-average-enrollees", className="hi-raw_total_enrollees"),
                                                html.Div([
                                                    html.Span("Average Enrollees", className="hi-label_total_enrollees"),
                                                    
                                                ], className="hi-total_label")
                                            ], className="hi-total_enrollees"),    
                                        ], margin=False, bg='#0072e8', gradient=True)
                                    ], className="plot-b-box2"),
                                        
                                        html.Div([
                                            Card([
                                                html.Div([
                                                    html.Div([
                                                        html.Span("", className="glevel-marker enrollees"),
                                                        html.Img(src="/assets/images/icons_navigation/person-blue.svg"),
                                                        html.H1([], id="truncated-total-enrollees", className="truncated_total_enrollees"),
                                                    ], className="glevel-count"),
                                                    html.Span([], id="raw-total-enrollees", className="raw_total_enrollees"),
                                                    html.Div([
                                                        html.Span("Total Enrollees", className="label_total_enrollees"),
                                                        
                                                    ], className="total_label")
                                                    
                                                ], className="total_enrollees"),    
                                            ], margin=False, bg='##ECF8FF')
                                        ], className="plot-b-box2"),

                                        html.Div([
                                            Card([
                                                html.Div([
                                                    html.Div([
                                                        html.Span("", className="glevel-marker schools"),
                                                        html.Img(src="/assets/images/icons_navigation/school-blue.svg"),
                                                        html.H1([], id="truncated-total-schools", className="truncated_total_schools"),
                                                    ], className="glevel-count"),
                                                    html.Span([], id="raw-total-schools", className="raw_total_schools"),
                                                    html.Div([
                                                        html.Span("Total Schools", className="label_total_schools"),
                                                        
                                                    ], className="total_label")
                                                ], className="total_enrollees"),
                                            ], margin=False, bg='##ECF8FF')
                                        ], className="plot-b-box2"),
                                    ], className="ns-sub-detail"),
                                    
                                    html.Div([
                                        
                                        
                                        
                                    ], className="lfury"),
                                
                                ], className='plot-b-section'),
                                
                                ## PLOT A
                                html.Div([
                                    #########################################
                                    ## INSERT PLOT: Distribution of enrollees per location 
                                    #########################################
                                    html.H4(["Enrollment Distribution by Gender"], className="edrg-graph-title", id="edrg-graph-title"),
                                    # dcc.Loading(
                                    #     id="loading-graph",
                                    #     type="default",
                                        # children=
                                        html.Div([], id='location_enrollees-distribution-per-location',)
                                    # )
                                    
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
                                    
                                ], className='plot-a-section'),
                                
                                
                            ], className='track-box plot-content')
                        ], className='plot-top-section plot-sec-wrap'),
                        
                        # ## BOTTOM SECTION
                        # html.Div([
                        #     html.H3(["Strand/Track Preferences"], className='label'),
                        #     html.Div([Card([
                        #         #########################################
                        #         ## INSERT PLOT: Strand preferences per region
                        #         #########################################
                        #         html.H4(["Strand and Track Preferences per Region"], className="spr-graph-title"), 
                                
                        #         # dcc.Loading(
                        #         #     id="loading-graph",
                        #         #     type="default",
                        #         #     children=
                        #             html.Div([
                        #             ],id='track-preference-heatmap')
                        #         # )
                        #         # dcc.Graph(
                        #         #     id="track-preference-heatmap",
                        #         #     # figure=heatmap_fig,
                        #         #     config={"responsive": True},
                        #         #     style={"width": "100%", "height": "100%", "display": "none"}
                        #         # )

                                
                        #     ], margin=False)], className='plot-content')
                        # ], className='plot-bottom-section plot-sec-wrap'),
                    ])], className='plot-left-section'),
                    
                    
                    ## RIGHT SECTION
                    html.Div([
                        
                        
                        # ## BOT SECTION
                        # html.Div([
                        #     html.H3(["School Type Analysis"], className='label'),
                        #     html.Div([Card([
                        #         #########################################
                        #         ## INSERT PLOT: school sectors
                        #         #########################################
                        #         html.H4(["Student Enrollment by School Sector per Region"], className="ss-graph-title"), 
                        #         # dcc.Loading(
                        #         #     id="loading-graph",
                        #         #     type="default",
                        #         #     children=
                        #             html.Div([], id='location_school_sectors',)
                        #         # ),
                                
                        #     ], margin=False)], className='plot-content')
                        # ], className='plot-bottom-section plot-sec-wrap'),
                    ], className='plot-right-section'), 
                ]
            , className="revlov-top"),
            
            
            html.Div(
                [
                    html.Div([
                        
                        ## TOP SECTION
                        html.Div([
                            html.H3(["Geographic Distribution"], className='label'),
                            html.Div([Card([
                                    #########################################
                                    ## INSERT PLOT: enrollment density (students per location)
                                    #########################################
                                    html.Div([], id='cloroplet')

                                
                                ], margin=False)], className='plot-content')
                        ], className='plot-top-section plot-sec-wrap'),
                    ], className="rev-left"),
                    
                    html.Div([
                        
                        ## BOTTOM SECTION
                        html.Div([
                            html.H3(["Student Preferences"], className='label'),
                            html.Div([Card([
                                html.Div([
                                    
                                    html.Div(
                                        [
                                            #########################################
                                            ## INSERT PLOT: Strand preferences per region
                                            #########################################
                                            html.H4(["By Strand and Track Preferences"], className="spr-graph-title"), 
                                            
                                            # dcc.Loading(
                                            #     id="loading-graph",
                                            #     type="default",
                                            #     children=
                                                html.Div([
                                                ],id='track-preference-heatmap')
                                            # )
                                            # dcc.Graph(
                                            #     id="track-preference-heatmap",
                                            #     # figure=heatmap_fig,
                                            #     config={"responsive": True},
                                            #     style={"width": "100%", "height": "100%", "display": "none"}
                                            # )
                                        ]
                                    , className='plt-loc-top'),
                                    
                                    html.Div(
                                        [
                                            #########################################
                                            ## INSERT PLOT: school sectors
                                            #########################################
                                            html.H4(["By School Sector"], className="spr-graph-title"), 
                                            # dcc.Loading(
                                            #     id="loading-graph",
                                            #     type="default",
                                            #     children=
                                                html.Div([], id='location_school_sectors',)
                                            # ),
                                        ]
                                    , className='plt-loc-bot'),
                                    
                                ], className='plttt'),

                            ], margin=False, padding='1.5em')], className='plot-content')
                        ], className='plot-bottom-section plot-sec-wrap'),
                        
                        
                        # ## BOT SECTION
                        # html.Div([
                        #     html.H3(["School Type Analysis"], className='label'),
                        #     html.Div([Card([
                        #         #########################################
                        #         ## INSERT PLOT: school sectors
                        #         #########################################
                        #         html.H4(["Student Enrollment by School Sector per Region"], className="ss-graph-title"), 
                        #         # dcc.Loading(
                        #         #     id="loading-graph",
                        #         #     type="default",
                        #         #     children=
                        #             html.Div([], id='location_school_sectors',)
                        #         # ),
                                
                        #     ], margin=False)], className='plot-content')
                        # ], className='plot-bottom-section plot-sec-wrap'),
                        
                    ], className="rev-right"),

                ]
            , className="revlov-bot"),
            
        ], className='plotted-location-report render-plot')
    
    

def new_location_filter():
    return html.Div(
        children=[
            ## LEFT SECTION
            html.Div([
                
                html.Div(
                    [
                        html.Div([
                            html.Div([
                                html.Div([
                                    
                                    Card([
                                        html.Div([
                                            html.Div([
                                                html.Img(src="/assets/images/icons_navigation/person-white.svg", className="total-icon"),
                                                html.H1([], id="highest-avg-enroll", className="total-text"),
                                            ], className='icon-and-text'),
                                            html.Div([
                                                html.Span("", className="year-marker"),
                                                html.Span("Academic Year 2023-2024", className="year-text", id="year-text"),
                                            ], className='academic-year'),
                                            html.Div([
                                                html.Span("Peak Enrollment Accross Years", className="desc-text"),
                                            ], className='indicator'),
                                        ], className="ns-card-1"),
                                    ], margin=False, padding="1em", gradient=True),
                                ], className='mainnnn'),
                                
                                html.Div([
                                    Card([
                                        html.Div([
                                            html.Div([
                                                html.Span("", className="glevel-marker es"),
                                                html.H1([], id="high-avg-enroll", className="count-text"),
                                            ], className="glevel-count"),
                                            html.Span([], id="esss-text", className="full-count-text"),
                                            html.Span([], id="high-tag-loc"),
                                            html.Span("Highest Average", className="desc-text"),
                                        ], className="ns-sub-cards"),
                                    ], margin=False)
                                ], className="ns-indicator"),
                                
                                
                                html.Div([
                                    Card([
                                        html.Div([
                                            html.Div([
                                                html.Span("", className="glevel-marker jhs"),
                                                html.H1([], id="low-avg-enroll", className="count-text"),
                                            ], className="glevel-count"),
                                            html.Span([], id="jhs-text", className="full-count-text"),
                                            html.Span([], id="low-tag-loc"),
                                            html.Span("Lowest Average", className="desc-text"),
                                        ], className="ns-sub-cards"),
                                    ], margin=False)
                                ], className="ns-indicator"),
                                
                            ], className="ns-main-detail"),
                            
                            # html.Div([
                            #     html.Div([
                            #         Card([
                            #             html.Div([
                            #                 html.Div([
                            #                     html.Span("", className="glevel-marker es"),
                            #                     html.H1([], id="es-text-formatted", className="count-text"),
                            #                 ], className="glevel-count"),
                            #                 html.Span([], id="es-text", className="full-count-text"),
                            #                 html.Span("Elementary", className="desc-text"),
                            #             ], className="ns-sub-cards"),
                            #         ], margin=False)
                            #     ], className="ns-indicator"),
                                
                            #     html.Div([
                            #         Card([
                            #             html.Div([
                            #                 html.Div([
                            #                     html.Span("", className="glevel-marker jhs"),
                            #                     html.H1([], id="jhs-text-formatted", className="count-text"),
                            #                 ], className="glevel-count"),
                            #                 html.Span([], id="jhs-text", className="full-count-text"),
                            #                 html.Span("Junior High School", className="desc-text"),
                            #             ], className="ns-sub-cards"),
                            #         ], margin=False)
                            #     ], className="ns-indicator"),
                                
                            #     html.Div([
                            #         Card([
                            #             html.Div([
                            #                 html.Div([
                            #                     html.Span("", className="glevel-marker shs"),
                            #                     html.H1([], id="shs-text-formatted", className="count-text"),
                            #                 ], className="glevel-count"),
                            #                 html.Span([], id="shs-text", className="full-count-text"),
                            #                 html.Span("Senior High School", className="desc-text"),
                            #             ], className="ns-sub-cards"),
                            #         ], margin=False)
                            #     ], className="ns-indicator")
                                
                            # ], className="ns-sub-detail"),
                        ], className="ns-details"),
                    ]
                , className='plt-top plt'),
                
                html.Div(Card(
                    [
                        html.Div([html.Div([], id='enrollment-by-years'),], className='plt-mid plt'),
                        html.Div([html.Div([], id='total-enrollment-by-year'),], className='plt-bot plt'),
                    ]
                , margin=False), className='year-analysis'),
                
                
            ], className='plot-left-section'),
            
            ## RIGHT SECTION
            html.Div([
                Card(
                    [
                        html.Div([], id='cloroplet')
                        
                    ]
                , margin=False)
            ], className='plot-right-section'),
            
        ], className='plotted-location-reporttt render-plot')