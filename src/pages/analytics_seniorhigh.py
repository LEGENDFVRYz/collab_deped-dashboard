from pydoc import classname
import dash
from dash import html
from dash import Dash, dcc, html

# --  Shared Components
from src.components.card import Card
from src.utils.reports import seniorhigh_chart

# """
#     Template For Rendering the Location Reports:
    
# """


def render_seniorhigh_filter():
    return html.Div(
        children=[
            ## options
            html.Div([
                # LAYER 1
                html.Div([
                    # ENROLLMENT DISTRIBUTION
                    html.Div([
                        html.H3("SHS Enrollment Distribution", className="section_title"),
                        html.Div([
                            html.Div([
                                html.Div([
                                    Card([
                                        # distribution of enrollees per track
                                        #########################################
                                        ## Sample Use of Charts, Remove this After
                                        # dcc.Loading(
                                        #     id="loading-graph",
                                        #     type="default",
                                        #     children=
                                        html.H4(["Senior High Tracks Distribution"], className="shs-track-dist-title"),
                                        html.Div([],id='seniorhigh_distri_per_track', )
                                        # ),
                                        # dcc.Graph(id="seniorhigh_distri_per_track", className="seniorhigh_distri_per_track", figure=seniorhigh_distri_per_track,
                                        #     config={"responsive": True},
                                        #     style={"width": "100%", "height": "100%"}
                                        # ),
                                        #########################################
                                    ], margin=False),
                                ], className="shs-enrollment-dist-graph"),
                                
                                html.Div([
                                    Card([
                                        # ratio enrollment in Academic vs. non-Academic tracks
                                        # dcc.Loading(
                                        #     id="loading-graph",
                                        #     type="default",
                                        #     children=
                                        html.Div([
                                            html.Div([],id='seniorhigh_ratio_enrollment',),
                                            html.Div([
                                                html.Div([
                                                    html.Span("Academic"),
                                                    html.Span([], id="acad-count"),
                                                    html.Span([], id="acad-percentage"),
                                                ], className="shs-academic"),
                                                html.Div([
                                                    html.Span("Non-academic"),
                                                    html.Span([], id="non-acad-count"),
                                                    html.Span([], id="non-acad-percentage"),
                                                ], className="shs-non-academic"),
                                            ], className="seniorhigh_ratio_enrollment_ind")
                                        ], className="shs-donut-container")
                                    ], margin=False),
                                ], className="shs-enrollment-donut"),
                                
                            ], className="shs-enrollment-left"),
                            
                            html.Div([
                                Card([
                                    # most and least enrolled  (strand)
                                    # dcc.Loading(
                                    #     id="loading-graph",
                                    #     type="default",
                                    #     children=
                                    html.H4(["Gender Distribution Across Academic Strands"], className="shs-gender-dist-title"),
                                    html.Div([
                                        html.Div([], id='seniorhigh_gender_distri',),
                                        # html.Div([],id='seniorhigh_most_least_enrolled',)
                                        
                                        html.Div([
                                            html.Div([
                                                html.Span("Most Populated"),
                                                html.Span([], id="shs-highest-strand"),
                                                html.Span([], id="shs-highest-count"),
                                                html.Span("students"),
                                            ], className="shs-population-container"),
                                            html.Div([
                                                html.Span("Least Populated"),
                                                html.Span([], id="shs-lowest-strand"),
                                                html.Span([], id="shs-lowest-count"),
                                                html.Span("students"),
                                            ], className="shs-population-container")
                                        ], className="shs-population")
                                        
                                    ], className="shs-right-content"),
                                    
                                ], margin=False),
                            ], className="shs-enrollment-right"),
                        
                        ], className="shs-enrollment-content"),
                    ], className="shs-enrollment"),
                ], className="shs-layer-1"),
                
                # LAYER 2
                html.Div([
                    # TRACK AVAILABILITY
                    html.Div([
                        html.H3("Track Availability", className="section_title"),
                        
                        html.Div([
                            html.Div([
                                Card([
                                    # differences in the number of schools offering each track
                                    # dcc.Loading(
                                    #     id="loading-graph",
                                    #     type="default",
                                    #     children=
                                    html.H4(["Number of Schools Offering Each Track by Sector"], className="shs-school-track-title"),
                                    html.Div([],id='seniorhigh_school_offering_per_track_by_sector',)
                                    # ),
                                    # dcc.Graph(id="seniorhigh_school_offering_per_track_by_sector", className="seniorhigh_school_offering_per_track_by_sector", figure=seniorhigh_school_offering_per_track_by_sector,
                                    #     config={"responsive": True},
                                    #     style={"width": "100%", "height": "100%"}
                                    # ),
                                ], margin=False)
                            ], className="shs-track-avail-graph"),
                            html.Div([
                                Card([
                                    # which SHS tracks are least offered but in high demand
                                    # dcc.Loading(
                                    #     id="loading-graph",
                                    #     type="default",
                                    #     children=
                                    html.H4(["Relationship between Student Demand and Track Supply"], className="shs-high-demand-title"),
                                    html.Div([],id='seniorhigh_least_offered_high_demand',)
                                    # ),
                                    
                                    # dcc.Graph(id="seniorhigh_least_offered_high_demand", className="seniorhigh_least_offered_high_demand", figure=seniorhigh_least_offered_high_demand,
                                    #     config={"responsive": True},
                                    #     style={"width": "100%", "height": "100%"}
                                    # ),
                                ], margin=False)
                            ], className="shs-track-avail-graph"),
                        ], className="shs-track-avail-content")
                        
                    ], className="shs-track-avail")
                ], className="shs-layer-2"),
                
                html.Div([
                    html.Div([
                        html.H3("Region and Sector-based Distribution" , className="section_title"),
                        html.Div([
                            html.Div([
                                Card([
                                    # which SHS tracks are more prevalent in each sector\
                                    # dcc.Loading(
                                    #     id="loading-graph",
                                    #     type="default",
                                    #     children=
                                    html.H4(["Prevalence of SHS Strands by Sector (Based on Student Count)"], className="shs-prevalent-title"),
                                    html.Div([],id='seniorhigh_prevalent_tracks', className="seniorhigh_prevalent_tracks")
                                    # ),
                                ], margin=False),
                            ], className="shs-region-sector-graph sector-1"),
                            
                            html.Div([
                                html.Div([
                                    Card([
                                        # how many schools offer each SHS track per region
                                        # dcc.Loading(
                                        #     id="loading-graph",
                                        #     type="default",
                                        #     children=
                                        html.H4(["Heatmap"], className="shs-offers-title"),
                                        html.Div([],id='seniorhigh_shs_offers',)
                                        # ),
                                    ], margin=False),
                                ], className="shs-region-sector-upper"),
                                html.Div([
                                    Card([
                                        # do mother schools or annexes offer a wider range of SHS tracks
                                        # dcc.Loading(
                                        #     id="loading-graph",
                                        #     type="default",
                                        #     children=
                                        html.H4(["Number of SHS Strand Offered by Mother Schools vs Annexes"], className="shs-range-title"),
                                        html.Div([],id='seniorhigh_offer_range',)
                                        # ),
                                    ], margin=False),
                                ], className="shs-region-sector-lower"),
                            ], className="shs-region-sector-graph sector-2")
                            
                        ], className="shs-region-sector-content"),
                    ], className="shs-region-sector"),
                ], className="shs-layer-3"),
                
            ], className="shs-content"),
        ], className='plotted-seniorhigh-report render-plot')
    
    
    
def new_location_shs():
    return html.Div(
        children=[
            ## LEFT SECTION
            "NEWW shs"
            
        ], className='plotted-seniorhigh-report render-plot')