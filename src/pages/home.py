from pydoc import classname
import dash
from dash import html
from dash import Dash, dcc, html

# --  Shared Components
from src.components.card import Card

# -- Graphs
from src.utils.reports.home_enrollment_per_region import home_regional_distribution, home_enrollment_per_region, home_school_number_per_sector, home_gender_distribution, home_subclass_table, home_program_offering, home_shs_tracks, home_shs_strands
from src.utils.reports.home_enrollment_per_region import total_enrollees, number_of_schools, number_of_schools_formatted, total_male_count, total_male_count_formatted, total_female_count, total_female_count_formatted, total_es_count, total_es_count_formatted, total_jhs_count, total_jhs_count_formatted, total_shs_count, total_shs_count_formatted, gender_gap, greater_gender, lesser_gender

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
                html.H3(["National Snapshot"], className="section_title"),
                
                html.Div([
                    html.Div([
                        
                        html.Div([
                            Card([
                                html.Div([
                                    html.Div([
                                        html.Img(src="/assets/images/icons_navigation/person-white.svg", className="total-icon"),
                                        html.H1(f"{total_enrollees:,}", className="total-text"),
                                    ], className='icon-and-text'),
                                    html.Div([
                                        html.Span("", className="year-marker"),
                                        html.Span("Academic Year 2023-2024", className="year-text"),
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
                                            html.H1(f"{total_es_count_formatted}", className="count-text"),
                                        ], className="glevel-count"),
                                        html.Span(f"{total_es_count:,} enrollees", className="full-count-text"),
                                        html.Span("Elementary", className="desc-text"),
                                    ], className="ns-sub-cards"),
                                ], margin=False)
                            ], className="ns-indicator"),
                            html.Div([
                                Card([
                                    html.Div([
                                        html.Div([
                                            html.Span("", className="glevel-marker jhs"),
                                            html.H1(f"{total_jhs_count_formatted}", className="count-text"),
                                        ], className="glevel-count"),
                                        html.Span(f"{total_jhs_count:,} enrollees", className="full-count-text"),
                                        html.Span("Junior High School", className="desc-text"),
                                    ], className="ns-sub-cards"),
                                ], margin=False)
                            ], className="ns-indicator"),
                            html.Div([
                                Card([
                                    html.Div([
                                        html.Div([
                                            html.Span("", className="glevel-marker shs"),
                                            html.H1(f"{total_shs_count_formatted}", className="count-text"),
                                        ], className="glevel-count"),
                                        html.Span(f"{total_shs_count:,} enrollees", className="full-count-text"),
                                        html.Span("Senior High School", className="desc-text"),
                                    ], className="ns-sub-cards"),
                                ], margin=False)
                            ], className="ns-indicator")
                        ], className="ns-sub-detail"),
                    ], className="ns-details"),
                
                    html.Div([
                        Card([
                            html.H4(["Regional Distribution"], className="ns-graph-title"),
                            dcc.Graph(id="home_regional_distribution", figure=home_regional_distribution,
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
            
            # Learner Profile
            html.Div([
                html.H3(["Learner Profiles"], className="section_title"),
                
                html.Div([
                    html.Div([
                        
                        html.Div([
                            Card([
                                html.Div([
                                    dcc.Graph(id="home_gender_distribution", className="lp-dist-graph", figure=home_gender_distribution,
                                                config={"responsive": True},
                                                style={"width": "100%", "height": "100%"}
                                    ),
                                    html.Div([
                                        html.Div([
                                            html.Img(src="/assets/images/icons_navigation/up-green.svg", className="up-icon"),
                                            html.Span(f"{gender_gap}%", className="percentage"),
                                        ], className="gap-percentage"),
                                        html.Div([
                                            html.Span("more"),
                                            html.Span(f"{greater_gender}", className=f"greater {'male-dominant' if greater_gender == 'MALE' else 'female-dominant'}"),
                                        ], className="greater-div"),
                                        html.Span("enrollees"),
                                        html.Div([
                                            html.Span("than"),
                                            html.Span(f"{lesser_gender}", className=f"lesser {'male-less-dominant' if lesser_gender == 'MALE' else 'female-less-dominant'}"),
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
                                            html.H1(f"{total_female_count_formatted}", className="count-text"),
                                        ], className="gender-count"),
                                        html.Span(f"{total_female_count:,} students", className="full-count-text"),
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
                                            html.H1(f"{total_male_count_formatted}", className="count-text"),
                                        ], className="gender-count"),
                                        html.Span(f"{total_male_count:,} students", className="full-count-text"),
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
                                    dcc.Graph(id="home_shs_tracks", figure=home_shs_tracks,
                                            config={"responsive": True},
                                            style={"width": "100%", "height": "100%"}
                                    ),
                                ], className="lp-upper"),
                                
                                html.Div([
                                    html.Hr(),
                                    html.H5("Academic Track"),
                                    html.H6("Strand Breakdown"),
                                    dcc.Graph(id="home_shs_strands", figure=home_shs_strands,
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
                                html.Div([html.H3(f"{number_of_schools_formatted}")], className='header'),
                                html.Div([html.Span(f"{number_of_schools:,} schools", className="text-center"),], className='indicator'),
                            ], margin=False, gradient=True)
                        ], className="ssc-info"),
                        
                        html.Div([
                            Card([
                                html.Div([
                                    html.H6("Subclassification"),
                                    html.H6("School Count"),
                                    html.H6("Student Count"),
                                ], className="ssc-table-header"),
                                dcc.Graph(id="ssc-subclass-table", figure=home_subclass_table,
                                                config={"responsive": True},
                                                style={"width": "100%", "height": "100%"}
                                ),
                            ], margin=False)
                        ], className="ssc-table"),
                        
                    ], className="ssc-content-1"),
                    
                    html.Div([
                        Card([
                            dcc.Graph(id="home_school_number_per_sector", figure=home_school_number_per_sector,
                                            config={"responsive": True},
                                            style={"width": "100%", "height": "100%"}
                            ),   
                        ], margin=False),
                    ], className="ssc-content-2"),
                    
                    html.Div([
                        Card([
                            dcc.Graph(id="home_program_offering", figure=home_program_offering,
                                    config={"responsive": True},
                                    style={"width": "100%", "height": "100%"}
                            ),
                        ], margin=False),
                    ], className="ssc-content-3"),
                    
                ], className="ssc-content"),  
                
            ], className="school-system-composition"),
            
        ], className="overview-layer-3")
        
    ], className='content')
    
], className='home-page container')