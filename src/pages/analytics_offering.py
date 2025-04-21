from dash import html, dcc
from src.components.card import Card

# ## IMPORTED CHARTS
# from src.utils.reports.offering_chart import sample_chart


# """
#     Template For Rendering the Program Offering Reports:
    
# """


# def render_offering_filter():
#     return html.Div(
#         children=[
            
#             ## LEFT SECTION
#             html.Div([
                
#                 ## TOP SECTION
#                 html.Div([
#                     html.Div(["Program Offering Overview"], className='label'),
#                     html.Div([
                        
#                         ## PLOT A
#                         html.Div([Card([
#                             #########################################
#                             ## INSERT PLOT: Number of Schools by MCOC Type
#                             #########################################
                            
#                             ## SAMPLE, REMOVE IT
#                             dcc.Graph(id="home_distribution-per-location", figure=sample_chart,
#                                         config={"responsive": True},
#                                         style={"width": "100%", "height": "100%"}
#                             )
                            
#                         ], margin=False, padding='0.25em')], className='plot-a'),
                        
#                         ## PLOT B
#                         html.Div([
                            
#                             ## PLOT B - TOP
#                             html.Div([Card([
#                                 #########################################
#                                 ## INSERT PLOT: Gender Distribution Aross MCOC types
#                                 #########################################
                                
                            
#                             ], margin=False)], className='plot-b-top'),
                            
#                             ## PLOT B - BOT
#                             html.Div([Card([
#                                 #########################################
#                                 ## INSERT PLOT: MCOC Types Ranked by Total Student Enrollment
#                                 #########################################
                                
                            
#                             ], margin=False)], className='plot-b-bot'),
#                         ], className='plot-b'),
#                     ], className='plot-content plot-box'),
#                 ], className='plot-top-section plot-sec-wrap'),
                
#                 ## BOTTOM SECTION
#                 html.Div([
#                     html.Div(["Location-Based Analysis"], className='label'),
#                     html.Div([
#                         ## PLOT A
#                         html.Div([Card([
#                             #########################################
#                             ## INDICATOR: Locations with the Highest and Lowest Number of Offerings
#                             #########################################
                            
                        
#                         ], margin=False)], className='plot-a'),
                        
#                         ## PLOT B
#                         html.Div([Card([
#                             #########################################
#                             ## INSERT PLOT: Number of MCOC Offerings per Location by School Level
#                             #########################################
                            
                        
#                         ], margin=False)], className='plot-b'),
#                     ], className='plot-content plot-box')
#                 ], className='plot-bottom-section plot-sec-wrap'),
#             ], className='plot-left-section'),
            
            
#             ## RIGHT SECTION
#             html.Div([
                
#                 ## TOP SECTION
#                 html.Div([
#                     html.Div(["Geographic Distribution"], className='label'),
#                     html.Div([Card([
#                         #########################################
#                         ## INSERT PLOT: Geographic Distribution of Program Offerings
#                         #########################################
                        
                        
#                     ], margin=False)], className='plot-content')
#                 ], className='plot-top-section plot-sec-wrap'),
                
#                 ## BOT SECTION
#                 html.Div([
#                     html.Div(["Enrollment Overview"], className='label'),
#                     html.Div([
                        
#                         ## PLOT A
#                         html.Div([Card([
#                             #########################################
#                             ## INDICATOR: Total Number of Enrollees Across All MCOC Types
#                             #########################################
                            
                            
#                         ], margin=False)], className='plot-sec-a'),

#                         ## PLOT B
#                         html.Div([Card([
#                             #########################################
#                             ## INSERT PLOT: Enrollment Distribution by Grade Level
#                             #########################################
                            
                            
#                         ], margin=False)], className='plot-sec-b'),
#                     ], className='plot-content plot-box')
#                 ], className='plot-bottom-section plot-sec-wrap'),
#             ], className='plot-right-section'),    
            
#         ], className='plotted-offering-report render-plot')


## --- TEMPORARY
def render_offering_filter():
    return html.Div(
        children=[]
    )