from dash import html, dcc
from src.components.card import Card

## Chart Callbacks
from src.utils.reports import offering_chart


# """
#     Template For Rendering the Program Offering Reports:
    
# """


def render_offering_filter():
    return html.Div(
        children=[
            
            html.Div([
                
                ## LAYER 1
                html.Div([
                    
                    html.Div([
                        html.H3("Program Offering Overview", className="section_title"),
                        html.Div([
                            
                            ## PLOT A
                            html.Div([Card([
                                #########################################
                                ## INSERT PLOT: Number of Schools by MCOC Type
                                #########################################
                                html.H4(["Number of Schools by Program Offerings"], className="offering-title"),
                                html.Div([
                                    html.Div([],id='offering_number-of-schools',),
                                    html.Div([
                                            html.Div([

                                                html.Div([
                                                    html.Span("Purely ES", className="offering-label"),
                                                    html.Div([
                                                        html.Span([], id='purely-es-percentage', className="offering-percentage"),
                                                        html.Div([
                                                            html.Span([], id='purely-es-count', className="offering-count")
                                                        ])    
                                                    ])
                                                ], className="offering-card dark-blue"),
                                                
                                                html.Div([
                                                    html.Span("ES and JHS", className="offering-label"),
                                                    html.Div([
                                                        html.Span([], id='es-and-jhs-percentage', className="offering-percentage"),
                                                        html.Div([
                                                            html.Span([], id='es-and-jhs-count', className="offering-count")
                                                        ])    
                                                    ])
                                                ], className="offering-card light-blue"),
                                                
                                                 html.Div([
                                                    html.Span("Purely JHS", className="offering-label"),
                                                    html.Div([
                                                        html.Span([], id='purely-jhs-percentage', className="offering-percentage"),
                                                        html.Div([
                                                            html.Span([], id='purely-jhs-count', className="offering-count")
                                                        ])
                                                    ])
                                                ], className="offering-card medium-blue"),
                                                
                                                 html.Div([
                                                    html.Span("JHS with SHS", className="offering-label"),
                                                    html.Div([
                                                        html.Span([], id='jhs-with-shs-percentage', className="offering-percentage"),
                                                        html.Div([
                                                            html.Span([], id='jhs-with-shs-count', className="offering-count")
                                                        ])    
                                                    ])
                                                ], className="offering-card lightest-blue"),
                                                 
                                                html.Div([
                                                    html.Span("Purely SHS", className="offering-label"),
                                                    html.Div([
                                                        html.Span([], id='purely-shs-percentage', className="offering-percentage"),
                                                        html.Div([    
                                                            html.Span([], id='purely-shs-count', className="offering-count")
                                                        ])
                                                    ])
                                                ], className="offering-card medium-light-blue"),
                                                 html.Div([
                                                    html.Span("All Offerings", className="offering-label"),
                                                    html.Div([
                                                        html.Span([], id='all-offering-percentage', className="offering-percentage"),
                                                        html.Div([
                                                            html.Span([], id='all-offering-count', className="offering-count")
                                                        ])    
                                                    ])
                                                ], className="offering-card white"),
                                            ], className="offering-grid")
                                        ])

                                        ], className="offering-overview-graph-cont")
                                    ], margin=False)
                                ], className='offering-overview-graph first'),
                       
                            ## PLOT B
                            html.Div([Card([
                                #########################################
                                ## INSERT PLOT: Gender Distribution Aross MCOC types
                                #########################################
                                html.H4(["Gender Distribution Across Program Offerings"], className="offering-title"),
                                html.Div([],id='offering_gender-distribution',)
                            ], margin=False)], className='offering-overview-graph second'),
                            
                            ## PLOT C
                            html.Div([Card([
                                #########################################
                                ## INSERT PLOT: MCOC Types Ranked by Total Student Enrollment
                                #########################################
                                html.H4(["Program Offerings Ranked by Total Student Enrollment"], className="offering-title"),
                                html.Div([],id='offering_ranked-mcoc',)
                            ], margin=False)], className='offering-overview-graph third'),
                            
                        ], className='offering-overview-content'),
                    ], className='offering-overview'),
                
                ], className='plot-layer-1'),
                
                ## LAYER 2
                html.Div([
                    
                    html.Div([
                        html.H3("Geographic Distribution", className="section_title"),
                        html.Div([
                            
                            ## PLOT A
                            html.Div([Card([
                                #########################################
                                ## INSERT PLOT: ...
                                #########################################
                                html.H4(["Number of Schools per Region by School Level"], className="offering-title"),
                                html.Div([],id='offering_mcoc-offerings-per-loc',)
                            ], margin=False)], className='offering-geographic-graph'),
                            
                            ## PLOT B
                            html.Div([Card([
                                #########################################
                                ## INSERT PLOT: ...
                                #########################################
                                html.H4(["Regions with Highest and Lowest Offerings per School Level"], className="offering-title"),
                                html.Div([],id='offering_location-extremes',)
                            ], margin=False)], className='offering-geographic-graph'),
                            
                        ], className='offering-geographic-content'),
                    ], className='offering-geographic'),
                    
                ], className='plot-layer-2'), 
                
                #LAYER 3
                html.Div([
                    html.Div([
                        html.H3("Grade-level Overview", className="section_title"),
                        html.Div([
                            
                            # PLOT A
                            html.Div([
                                
                                html.Div([
                                    Card([
                                        html.H4(["Senior High Tracks Distribution"], className="offering-title"),
                                        html.Div([],id='offering_enroll_dist',)   
                                    ], margin=False),
                                ], className="offering-g1-graph"),
                                
                                html.Div([
                                    html.Div([
                                        Card([
                                            html.Div([
                                            html.Span("Most Populated", className="offering-pop-title"),
                                            html.Span([], id="offering-highest-grade", className="offering-grade"),
                                            html.Div([
                                                html.Span([], id="offering-highest-count", className="offering-count"),
                                                html.Span("students", className="offering-student-text"),
                                            ], className="offering-student-count most"),
                                    ], className="offering-populated"),
                                            
                                        ], margin=False),
                                    ], className="offering-info"),
                                    
                                    html.Div([
                                        Card([
                                            html.Div([
                                                html.Span("Least Populated", className="offering-pop-title"),
                                                html.Span([], id="offering-lowest-grade", className="offering-grade"),
                                                html.Div([
                                                    html.Span([], id="offering-lowest-count", className="offering-count"),
                                                    html.Span("students", className="offering-student-text"),
                                                ], className="offering-student-count least"),
                                            ], className="offering-populated"),
                                        ], margin=False),
                                    ], className="offering-info"),
                                ], className="offering-info-cards"),
                            ], className="offering-group-1"),
                            
                            ## PLOT B
                            html.Div([Card([
                                #########################################
                                ## INSERT PLOT: ...
                                #########################################
                                html.H4(["Senior High Tracks Distribution"], className="offering-title"),
                                html.Div([],id='offering_enrollees_num',)
                            ], margin=False)], className='offering-group-2'),
                            
                        ], className='offering-grade-level-content'),
                    ], className='offering-grade-level'),
                    
                ], className='plot-layer-3') 
                
            ], className="offering-content"),  
            
        ], className='plotted-offering-report render-plot')
