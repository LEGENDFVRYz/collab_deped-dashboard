from pydoc import classname
import dash
from dash import html
from dash import Dash, dcc, html

# --  Shared Components
from src.components.card import Card

# -- Graphs
from src.utils.reports.home_enrollment_per_region import format_large_number
from src.utils.reports.home_enrollment_per_region import home_enrollment_per_region, track_ratio_per_track, home_school_number_per_sector, home_gender_distribution
from src.utils.reports.home_enrollment_per_region import total_enrollees, most_active, least_active, academic_track_ratio, number_of_schools, total_male_count, total_female_count, total_es_count, total_jhs_count, total_shs_count

# Landing page
dash.register_page(__name__, path="/")  

layout = html.Div([
    ## -- Standard: Page Content Header
    html.Div([
        html.H1('Overview')
    ], className='page-header'),
    
    html.Div([
        html.Div([
            
            # National Snapshot
            html.Div([
                html.H4("National Snapshot"),
                
                html.Div([
                    html.Div([
                        Card([
                            html.Div([html.H1(f"{total_enrollees}", className="text-center"),], className='indicator'),
                        ], margin=False)
                    ], className="ns-info"),
                    html.Div([
                        Card([
                            html.Div([html.H1(f"{total_es_count}", className="text-center"),], className='indicator'),
                        ], margin=False)
                    ], className="ns-info"),
                    html.Div([
                        Card([
                            html.Div([html.H1(f"{total_jhs_count}", className="text-center"),], className='indicator'),
                        ], margin=False)
                    ], className="ns-info"),
                    html.Div([
                        Card([
                            html.Div([html.H1(f"{total_shs_count}", className="text-center"),], className='indicator'),
                        ], margin=False)
                    ], className="ns-info"),
                ], className="ns-info-cards"),
                
                html.Div([
                    Card([], margin=False)
                ], className="ns-graph"),
            ], className="national-snapshot"),
            
            # Grade-level Dynamics
            html.Div([
                html.H4("Grade-level Dynamics"),
                
                html.Div([
                    html.Div([
                      Card([
                      ## -- GRAPH: Total Enrollment Count per School Level
                        # html.Div(["Enrollments per School Level"], className='header'), 
                        dcc.Graph(id="home_enrollment-per-region", figure=home_enrollment_per_region,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100%"}
                        ),
                      ], margin=False)  
                    ], className="gld-graph"),
                    
                    html.Div([
                        html.Div([
                            Card([], margin=False)
                        ], className="gld-info"),
                        html.Div([
                            Card([], margin=False)
                        ], className="gld-info"),
                    ],className="gld-info-cards"),
                    
                ], className="gld-content"),
            ], className="grade-level-dynamics"),
            
        ], className="upper-content"),
        
        html.Div([
            
            # Learner Profile
            html.Div([
                html.H4("Learner Profiles"),
                
                html.Div([
                    html.Div([
                        
                        html.Div([
                            Card([
                                dcc.Graph(id="home_gender_distribution", figure=home_gender_distribution,
                                            config={"responsive": True},
                                            style={"width": "100%", "height": "100%"}
                                ),
                            ], margin=False)
                        ], className="lp-graph"),
                        
                        html.Div([
                            html.Div([
                                Card([
                                    html.Div([html.H3(f"{total_female_count}")], className='header'),
                                ], margin=False)
                            ], className="lp-info"),
                            html.Div([
                                Card([
                                    html.Div([html.H3(f"{total_male_count}")], className='header'),
                                ], margin=False)
                            ], className="lp-info"),
                        ],className="lp-info-cards"), 
                        
                    ], className="lp-graph-1"),
                    
                    html.Div([
                      Card([], margin=False)  
                    ], className="lp-graph-2"),
                ], className="lp-content"),
                
            ], className="learner-profiles"),
            
            # School System Composition
            html.Div([
                html.H4("School System Composition"),
                
                html.Div([
                    html.Div([
                        
                        html.Div([
                            html.Div([
                                Card([
                                    html.Div([html.H3(f"{number_of_schools}")], className='header'),
                                ], margin=False)
                            ], className="ssc-info"),
                            html.Div([
                                Card([
                                    dcc.Graph(id="home_school_number_per_sector", figure=home_school_number_per_sector,
                                                config={"responsive": True},
                                                style={"width": "100%", "height": "100%"}
                                    )
                                ], margin=False)
                            ], className="ssc-graph"),
                        ],className="ssc-info-graph"), 
                        
                        html.Div([
                            Card([], margin=False)
                        ], className="ssc-table"),
                        
                    ], className="ssc-content-1"),
                    
                    html.Div([
                        Card([], margin=False) 
                    ], className="ssc-content-2"),
                ], className="ssc-content"),  
                
            ], className="school-system-composition"),
        ], className="lower-content")
        
    ], className='content')
    
    #     ## -- Main Part
    #     html.Div([
    #         html.Div([
    #             ## --> Sub layer
    #             html.Div([Card([
    #                         ## -- GRAPH: Total Enrollment Count per School Level
    #                         html.Div(["Enrollments per School Level"], className='header'),
    #                         html.Div([
    #                             dcc.Graph(id="home_enrollment-per-region", figure=home_enrollment_per_region,
    #                                             config={"responsive": True},
    #                                             style={"width": "100%", "height": "100%"}
    #                                     )
    #                         ], className='graph'),
    #                     ]
    #             )], className='area-1'),
    #             html.Div([
    #                     html.Div([Card([
    #                             # -- INDICATOR: TOTAL ENROLEES IN PH
    #                             html.Div([
    #                                     html.Div([html.H1(f"{total_enrollees}", className="text-center"),], className='indicator'),
    #                                     html.Div([html.Img(src='/assets/images/icons_navigation/team-fill.svg')], className='indicator-display'),
    #                                 ], className='display'),
    #                             html.Div(['TOTAL ENROLLEES'], className='details')
    #                         ])], className='loc-1'),
    #                     html.Div([Card([
    #                         html.Div([
    #                                 # -- INDICATOR: Most Active School Level
    #                                 html.Div([
    #                                         html.Div([html.H1(f"{format_large_number(most_active['counts'])}", className="text-center"),], className='indicator'),
    #                                         html.Div([html.Img(src='/assets/images/icons_navigation/arrow-right-up-fill.svg')], className='indicator-display'),
    #                                     ], className='display'),
    #                             ], className='upper'),
    #                         html.Div([
    #                                 # -- INDICATOR: Most Active School Level
    #                                 html.Div([
    #                                         html.Div([html.H1(f"{format_large_number(least_active['counts'])}", className="text-center"),], className='indicator'),
    #                                         html.Div([html.Img(src='/assets/images/icons_navigation/arrow-left-down-fill.svg')], className='indicator-display'),
    #                                     ], className='display'),
    #                             ], className='lower')
    #                     ])], className='loc-2'),
    #                 ], className='area-2'),
    #         ], className='layer-1'),
            
    #         html.Div([Card([
    #             html.Div(["School Distribution Across Sectors"], className='header'),
    #             html.Div([
    #                 dcc.Graph(id="home_school_number_per_sector", figure=home_school_number_per_sector,
    #                                 config={"responsive": True},
    #                                 style={"width": "100%", "height": "100%"}
    #                 )
    #             ], className='graph'),
    #         ])], className='layer-2')
    #     ], className='main-section'),
    
    #     ## -- Side Part
    #     html.Div([
    #         html.Div([
    #                 Card([
    #                     ## -- GRAPH: Ratio distribution of shs strand
    #                     html.Div([html.H3(f"Academic Track is roughly {academic_track_ratio * 100:.2f}%")], className='header'),
    #                     html.Div([
    #                         dcc.Graph(id="track-ratio-per-track", figure=track_ratio_per_track,
    #                                         config={"responsive": True},
    #                                         style={"height": "100%"}
    #                     )], className='graph'),
    #                 ]
    #         )], className='layer-1'),
    #             html.Div([
    #                     Card([
    #                         html.Div([html.H3(f"{number_of_schools}")], className='header'),
    #                         html.Div([html.H3(f"{total_male_count}")], className='header'),
    #                         html.Div([html.H3(f"{total_female_count}")], className='header'),
    #                         html.Div(["School Distribution Across Sectors"], className='header'),
    #                         html.Div([
    #                             dcc.Graph(id="home_school_number_per_sector", figure=home_gender_distribution,
    #                                             config={"responsive": True},
    #                                             style={"width": "100%", "height": "100%"}
    #                             )
    #                         ], className='graph'),
    #                     ])
    #                 ], className='layer-2')
    #         ], className='side-section')
], className='home-page container')