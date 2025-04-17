from dash import html, dcc
from src.components.card import Card


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
                    html.Div(["Strand/Track Preferences"], className='label'),
                    html.Div([
                        
                        ## PLOT A
                        html.Div([Card([
                            #########################################
                            ## INSERT PLOT: Distribution of enrollees per location 
                            #########################################
                            
                            
                        ], margin=False)], className='plot-a-section'),
                        
                        ## PLOT B
                        html.Div([
                            html.Div([Card([
                                #########################################
                                ## TABLE: highest and lowest number of enrollees
                                #########################################
                                
                                
                            ], margin=False)], className='plot-b-box1'),
                            
                            html.Div([Card([], margin=False)], className='plot-b-box2'),
                            html.Div([Card([], margin=False)], className='plot-b-box2'),
                        
                        ], className='plot-b-section'),
                    ], className='track-box plot-content')
                ], className='plot-top-section plot-sec-wrap'),
                
                ## BOTTOM SECTION
                html.Div([
                    html.Div(["Strand/Track Preferences"], className='label'),
                    html.Div([Card([
                        #########################################
                        ## INSERT PLOT: ENROLLMENT DENSIITY
                        #########################################
                        
                        
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
                        ## INSERT PLOT: ENROLLMENT DENSIITY
                        #########################################
                        
                        
                        ], margin=False)], className='plot-content')
                ], className='plot-top-section plot-sec-wrap'),
                
                ## BOT SECTION
                html.Div([
                    html.Div(["School Type Analysis"], className='label'),
                    html.Div([Card([
                        #########################################
                        ## INSERT PLOT: SCHOOL TYPE ANALYSIS (school sectors)
                        #########################################
                        
                        
                    ], margin=False)], className='plot-content')
                ], className='plot-bottom-section plot-sec-wrap'),
            ], className='plot-right-section'),          
        ], className='plotted-location-report render-plot')