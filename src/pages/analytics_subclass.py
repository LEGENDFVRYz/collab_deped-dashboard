from pydoc import classname
import dash
from dash import html
from dash import Dash, dcc, html

# --  Shared Components
from src.components.card import Card

"""
    Template For Rendering the Location Reports:
    
"""


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
                        ], margin=False)
                    ], className="subclass-enroll-graph"),
                    
                    html.Div([
                        html.Div([
                            Card([
                                # enrollment distribution by subclass
                            ], margin=False)
                        ], className="subclass-enroll-graph"),
                        html.Div([
                            Card([
                                # average enrollment per school
                            ], margin=False)
                        ], className="subclass-enroll-graph")
                    ], className="subclass-enroll-middle"),
                    
                    html.Div([
                        Card([
                            # student-to-school ratio
                        ], margin=False)
                    ], className="subclass-enroll-graph")
                ], className="subclass-left-content"),
                
                # RIGHT SIDE CONTENTS
                html.Div([
                    # DISTRIBUTION AND AVAILABILITY
                    html.Div([
                        html.H4("Distribution and Availability"),
                        html.Div([
                            Card([
                                # subclass vs school type
                            ], margin=False)
                        ], className="subclass-dist-avail-graph"),
                        
                        html.Div([
                            html.Div([
                                Card([
                                    # sector affiliation
                                ], margin=False)
                            ], className="subclass-dist-avail-graph"),
                            html.Div([
                                Card([
                                    # regional distribution/ which subclass has the highest number of schools per loc
                                ], margin=False)
                            ], className="subclass-dist-avail-graph"),
                        ], className="subclass-dist-avail-lower")
                        
                    ], className="subclass-dist-avail"),
                    
                    # PROGRAM AND GRADE LEVEL OFFERINGS
                    html.Div([
                        html.H4("Program and Grade Level Offerings"),
                        html.Div([
                            html.Div([
                                Card([
                                    # mcoc breakdown/which subclass offers which program types
                                ], margin=False),
                            ], className="subclass-program-graph"),
                            
                            html.Div([
                                Card([
                                    # enrollment in shs tracks across subclass
                                ], margin=False),
                            ], className="subclass-program-graph"),
                            
                            html.Div([
                                html.Div([
                                    Card([
                                        # % schools offering ‘all offerings’ per subclass
                                    ], margin=False),
                                ], className="subclass-program-indicator"),
                                html.Div([
                                    Card([
                                        # % schools offering shs per subclass
                                    ], margin=False),
                                ], className="subclass-program-indicator"),
                            ], className="subclass-program-last-cards")
                            
                        ], className="subclass-program-contents"),
                    ], className="subclass-program"),
                    
                ], className="subclass-right-content")
                
            ], className="subclass-content"),
        ], className='plotted-subclass-report render-plot')