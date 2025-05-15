import dash
from dash import html
from dash import dcc, html

# --  Shared Components
from src.components.card import Card

# -- Graphs
from src.utils.reports import home_chart
# from src.utils.reports.home_enrollment_per_region import home_regional_distribution, home_enrollment_per_region, home_school_number_per_sector, home_gender_distribution, home_subclass_table, home_program_offering, home_shs_tracks, home_shs_strands
# from src.utils.reports.home_enrollment_per_region import total_enrollees, number_of_schools, number_of_schools_formatted, total_male_count, total_male_count_formatted, total_female_count, total_female_count_formatted, total_es_count, total_es_count_formatted, total_jhs_count, total_jhs_count_formatted, total_shs_count, total_shs_count_formatted, gender_gap, greater_gender, lesser_gender


# Landing page
dash.register_page(__name__, path="/", suppress_callback_exceptions=True)  


layout = html.Div([
    ## -- Standard: Page Content Header
        ## -- Standard: Page Content Header
    html.Div([
        html.Div([html.H1('Overview')]),

        html.Div(
            [
                ## Year Mode Analysis:
                html.Div([
                    html.Div(["Latest Year"], id="year-scope"),
                    html.Div([html.Img(src="/assets/images/control-switch-icon.svg")], id="year-toggle"),
                ], id="year-toggle-box")
            ]
        , className="page-controls")
    ], className='page-header'),
    
    
    # html.Div([
    #     html.H1('Overview')
    # ], className='page-header'),
    
    dcc.Loading([
        html.Div([], id="render-base"),
        html.Div([
            html.Div([

                # National Snapshot
                html.Div([
                    html.H3(["National Snapshot"], className="section_title"),
                    
                    html.Div([
                        html.Div([
                            
                            html.Div([
                                Card([
                                    html.Div([
                                        html.Div([
                                            html.Img(src="/assets/images/icons_navigation/person-white.svg", className="total-icon"),
                                            html.H1([], id="total-text", className="total-text"),
                                        ], className='icon-and-text'),
                                        html.Div([
                                            html.Span("", className="year-marker"),
                                            html.Span("Academic Year ", className="year-text first"),
                                            html.Span([], id="max-year", className="year-text second"),
                                        ], className='academic-year'),
                                        html.Div([
                                            html.Span("Total Number of Enrollees", className="desc-text"),
                                        ], className='indicator'),
                                    ], className="ns-card-1"),
                                ], margin=False, padding="1em", gradient=True)
                            ], className="ns-main-detail"),
                            
                            html.Div([
                                html.Div([
                                    Card([
                                        html.Div([
                                            html.Div([
                                                html.Span("", className="glevel-marker es"),
                                                html.H1([], id="es-text-formatted", className="count-text"),
                                            ], className="glevel-count"),
                                            html.Span([], id="es-text", className="full-count-text"),
                                            html.Span("Elementary", className="desc-text"),
                                        ], className="ns-sub-cards"),
                                    ], margin=False)
                                ], className="ns-indicator"),
                                
                                html.Div([
                                    Card([
                                        html.Div([
                                            html.Div([
                                                html.Span("", className="glevel-marker jhs"),
                                                html.H1([], id="jhs-text-formatted", className="count-text"),
                                            ], className="glevel-count"),
                                            html.Span([], id="jhs-text", className="full-count-text"),
                                            html.Span("Junior High School", className="desc-text"),
                                        ], className="ns-sub-cards"),
                                    ], margin=False)
                                ], className="ns-indicator"),
                                
                                html.Div([
                                    Card([
                                        html.Div([
                                            html.Div([
                                                html.Span("", className="glevel-marker shs"),
                                                html.H1([], id="shs-text-formatted", className="count-text"),
                                            ], className="glevel-count"),
                                            html.Span([], id="shs-text", className="full-count-text"),
                                            html.Span("Senior High School", className="desc-text"),
                                        ], className="ns-sub-cards"),
                                    ], margin=False)
                                ], className="ns-indicator")
                                
                            ], className="ns-sub-detail"),
                        ], className="ns-details"),
                    
                        html.Div([
                            Card([
                                html.H4(["Regional Distribution"], className="ns-graph-title"),
                                dcc.Graph(id="home_regional_distribution", figure={},
                                        config={"responsive": True},
                                        style={"width": "100%", "height": "100%"}
                                ),
                            ], margin=False)
                        ], className="ns-graph")
                        
                    ], className="ns-content"),
                ], className="national-snapshot"),
                
            ], className="overview-layer-1"),
            
            html.Div([
                
                # Grade-level Dynamics
                html.Div([
                    html.H3(["Grade-level Dynamics"], className="section_title"),
                    
                    html.Div([
                        html.Div([
                            Card([
                            ## -- GRAPH: Total Enrollment Count per School Level
                                html.H4(["Grade-level Distribution"], className="gld-graph-title"), 
                                dcc.Graph(
                                    id='home-enrollment-per-region',
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100%"},
                                    figure={},  # Initialize with empty figure
                                ),
                            ], margin=False)  
                        ], className="gld-graph"),
                        
                        html.Div([
                            
                            html.Div([
                                Card([
                                    html.Div([
                                        html.Span("Most Populated", className="gld-pop-title"),
                                        html.Span([], id="highest-grade", className="gld-grade"),
                                        html.Div([
                                            html.Span([], id="highest-count", className="gld-count"),
                                            html.Span("students", className="gld-student-text"),
                                        ], className="gld-student-count most"),
                                    ], className="gld-populated"),
                                ], margin=False)
                            ], className="gld-info"),
                            
                            html.Div([
                                Card([
                                    html.Div([
                                        html.Span("Least Populated", className="gld-pop-title"),
                                        html.Span([], id="lowest-grade", className="gld-grade"),
                                        html.Div([
                                            html.Span([], id="lowest-count", className="gld-count"),
                                            html.Span("students", className="gld-student-text"),
                                        ], className="gld-student-count least"),
                                    ], className="gld-populated"),
                                ], margin=False)
                            ], className="gld-info"),
                            
                        ],className="gld-info-cards"),
                        
                    ], className="gld-content"),
                ], className="grade-level-dynamics"),
                
                # Learner Profile
                html.Div([
                    html.H3(["Learner Profiles"], className="section_title"),
                    
                    html.Div([
                        html.Div([
                            
                            html.Div([
                                Card([
                                    html.Div([
                                        dcc.Graph(id="home_gender_distribution", className="lp-dist-graph", figure={},
                                                    config={"responsive": True},
                                                    style={"width": "100%", "height": "100%"}
                                        ),
                                        html.Div([
                                            html.Div([
                                                html.Img(src="/assets/images/icons_navigation/up-green.svg", className="up-icon"),
                                                html.Span([], id="gender-gap", className="percentage"),
                                            ], className="gap-percentage"),
                                            html.Div([
                                                html.Span("more"),
                                                html.Span(id="greater-gender", className="greater")
                                            ], className="greater-div"),
                                            html.Span("enrollees"),
                                            html.Div([
                                                html.Span("than"),
                                                html.Span(id="lesser-gender", className="lesser")
                                            ], className="lesser-div"),
                                        ], className="lp-desc"),
                                    ], className="lp-graph-desc"),
                                ], margin=False)
                            ], className="lp-graph"),
                            
                            html.Div([
                                html.Div([
                                    Card([
                                        html.Div([
                                            html.Div([
                                                html.Span("", className="gender-marker female"),
                                                html.H1([], id="total-female-count-formatted", className="count-text"),
                                            ], className="gender-count"),
                                            html.Span([], id="total-female-count", className="full-count-text"),
                                            html.Div([
                                                html.Span("Female Students", className="desc-text female"),
                                                html.Img(src="/assets/images/icons_navigation/female.svg"),
                                            ], className="desc-n-icon"),
                                        ], className="lp-sub-cards"),
                                    ], margin=False, padding="1em 1em 0.25em 1em"),
                                ], className="lp-indicator"),
                                
                                html.Div([
                                    Card([
                                        html.Div([
                                            html.Div([
                                                html.Span("", className="gender-marker male"),
                                                html.H1([], id="total-male-count-formatted", className="count-text"),
                                            ], className="gender-count"),
                                            html.Span([], id="total-male-count", className="full-count-text"),
                                            html.Div([
                                                html.Span("Male Students", className="desc-text male"),
                                                html.Img(src="/assets/images/icons_navigation/male.svg"),
                                            ], className="desc-n-icon"),
                                        ], className="lp-sub-cards"),
                                    ], margin=False, padding="1em 1em 0.25em 1em"),
                                ], className="lp-indicator"),
                            ],className="lp-info-cards"), 
                            
                        ], className="lp-graph-1"),
                        
                        html.Div([
                            Card([
                                html.Div([
                                    
                                    html.Div([
                                        html.H5("Track Preference"),
                                        dcc.Graph(id="home_shs_tracks", figure={},
                                                config={"responsive": True},
                                                style={"width": "100%", "height": "100%"}
                                        ),
                                    ], className="lp-upper"),
                                    
                                    html.Div([
                                        html.Div([html.Hr()] , style={'paddingTop': '8px', 'paddingBottom': '8px', 'color': '#E9E8E8'}),
                                        html.H5("Academic Track"),
                                        html.H6("Strand Breakdown", className="lp-strand-break"),
                                        dcc.Graph(id="home_shs_strands", figure={},
                                                config={"responsive": True},
                                                style={"width": "100%", "height": "100%"}
                                        ),    
                                    ], className="lp-lower")
                                    
                                ], className="lp-tracks-strands"),
                            ], margin=False)  
                        ], className="lp-graph-2"),
                    ], className="lp-content"),
                    
                ], className="learner-profiles"),
                
            ], className="overview-layer-2"),
            
            html.Div([
                
                # School System Composition
                html.Div([
                    html.H3(["School System Composition"], className="section_title"),
                    
                    html.Div([
                        html.Div([
                            
                            html.Div([
                                Card([
                                    html.Div([
                                        html.Div([
                                            html.Img(src="/assets/images/icons_navigation/school-count.svg", className="total-school-icon"),
                                            html.H1([], id="number-of-schools", className="total-school-text"),
                                        ], className='ssc-icon-and-text'),
                                        html.Div([
                                            html.Span("Total Number of Schools", className="ssc-desc-text"),
                                        ], className='ssc-indicator'),
                                    ], className="ssc-school-detail"),
                                ], margin=False, gradient=True)
                            ], className="ssc-info"),
                            
                            html.Div([
                                Card([
                                    html.Div([
                                        html.H6("Subclassification"),
                                        html.H6("School Count"),
                                        html.H6("Student Count"),
                                    ], className="ssc-table-header"),
                                    dcc.Graph(id="ssc-subclass-table", figure={},
                                            config={"responsive": True},
                                            style={"width": "100%", "height": "100%"}
                                    ),
                                ], margin=False)
                            ], className="ssc-table"),
                        ], className="ssc-content-1"),
                        
                        html.Div([
                            Card([
                                html.H4(["School Distribution Across Sectors"], className="sector-graph-title"),
                                dcc.Graph(id="home_school_number_per_sector", figure={},
                                        config={"responsive": True},
                                        style={"width": "100%", "height": "100%"}
                                ),
                            ], margin=False),
                        ], className="ssc-content-2"),
                        
                        html.Div([
                            Card([
                                html.Div([  
                                    html.H4(["School Distribution by Program Offering"], className="offering-graph-title"),
                                    
                                    html.Div([
                                        
                                        html.Div([
                                            html.Div([
                                                html.Span([], id="shs-percentage", className="shs-percent-text"),
                                                html.Span("of schools offers Senior High School", className="shs-desc-text"),
                                            ], className="program-offering-percentage"),
                                            
                                            html.Div([
                                                html.Div([
                                                    html.Span("", className="legend-color es"),
                                                    html.Span("Elementary", className="legend-text"),
                                                ], className="legend-label"),
                                                html.Div([
                                                    html.Span("", className="legend-color jhs"),
                                                    html.Span("Junior High School", className="legend-text"),
                                                ], className="legend-label"),
                                                html.Div([
                                                    html.Span("", className="legend-color shs"),
                                                    html.Span("Senior High School", className="legend-text"),
                                                ], className="legend-label"),
                                                html.Div([html.Hr()] , style={'paddingTop': '8px', 'paddingBottom': '8px', 'color': '#E9E8E8'}),
                                                html.Div([
                                                    html.Span("", className="legend-color purees"),
                                                    html.Span("Purely ES", className="legend-text"),
                                                ], className="legend-label"),
                                                html.Div([
                                                    html.Span("", className="legend-color purejhs"),
                                                    html.Span("Purely JHS", className="legend-text"),
                                                ], className="legend-label"),
                                                html.Div([
                                                    html.Span("", className="legend-color pureshs"),
                                                    html.Span("Purely SHS", className="legend-text"),
                                                ], className="legend-label"),
                                                html.Div([
                                                    html.Span("", className="legend-color esjhs"),
                                                    html.Span("ES with JHS", className="legend-text"),
                                                ], className="legend-label"),
                                                html.Div([
                                                    html.Span("", className="legend-color jhsshs"),
                                                    html.Span("JHS with SHS", className="legend-text"),
                                                ], className="legend-label"),
                                                html.Div([
                                                    html.Span("", className="legend-color alloffer"),
                                                    html.Span("All Offering", className="legend-text"),
                                                ], className="legend-label"),
                                            ], className="program-offering-legend"),
                                            
                                        ], className = "percent-legend-container"),
                                        
                                        dcc.Graph(id="home_program_offering", figure={},
                                                config={"responsive": True},
                                                style={"width": "100%", "height": "100%"},
                                                className="home_program_offering"
                                        ),
                                    ], className="program-offering-graph"),
                                    
                                ], className="ssc-container"),
                            ], margin=False),
                            
                        ], className="ssc-content-3"),
                        
                    ], className="ssc-content"),  
                    
                ], className="school-system-composition"),
                
            ], className="overview-layer-3")
            
        ], className='content')
    ], className='home-loading', delay_hide=1)
    
], className='home-page container')

