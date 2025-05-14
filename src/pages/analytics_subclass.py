from dash import html, dcc
from src.components.card import Card

# Chart Callbacks
from src.utils.reports import subclass_chart

def render_subclass_filter():
    return html.Div(
        children=[
            html.Div([
                html.Div([
                    html.H4("Enrollment Profile per Subclassification"),
                    html.Div([
                        Card([
                            html.H4(["Total Schools per Subclassification"], className="subclass-graph-title"),
                            html.Div([], id='subclass_total_schools_per_subclass')
                        ], margin=False)
                    ], className="subclass-enroll-graph"),

                    html.Div([
                        Card([
                            html.H4(["Enrollment Distribution by Subclassification"], className="subclass-graph-title"),
                            html.Div([], id='subclass_distrib_by_subclass')
                        ], margin=False)
                    ], className="subclass-enroll-graph"),

                    html.Div([
                        Card([
                            html.H4(["Student-to-School Ratio"], className="subclass-graph-title"),
                            html.Div([], id='subclass_student_school_ratio')
                        ], margin=False)
                    ], className="subclass-enroll-graph"),

                ], className="subclass-left-content"),

                html.Div([
                    html.Div([
                        html.H4("Distribution and Availability"),
                        html.Div([
                            Card([
                                html.H4(["Subclassification by School Type Distribution"], className="subclass-graph-title"),
                                html.Div([], id='subclass_vs_school_type')
                            ], margin=False)
                        ], className="subclass-dist-avail-graph"),

                        html.Div([
                            html.Div([
                                Card([
                                    html.H4(["Sector Affiliation"], className="subclass-graph-title"),
                                    html.Div([], id='subclass_sector_affiliation')
                                ], margin=False)
                            ], className="subclass-dist-avail-graph-1"),

                            html.Div([
                                Card([
                                    html.H4(["Regional Distribution of Schools"], className="subclass-graph-title"),
                                    html.Div([], id='subclass_heatmap')
                                ], margin=False)
                            ], className="subclass-dist-avail-graph-2"),
                        ], className="subclass-dist-avail-lower")

                    ], className="subclass-dist-avail"),

                    html.Div([
                        html.H4("Program and Grade Level Offerings"),
                        html.Div([
                            html.Div([
                                html.Div([
                                    Card([
                                        html.Div([], id='subclass_clustered')
                                    ], margin=False)
                                ], className="subclass-program-graph"),

                                html.Div([
                                    Card([
                                        html.Div([], id='subclass_clustered_tracks')
                                    ], margin=False)
                                ], className="subclass-program-graph"),
                            ], className="subclass-program-graph-left"),

                            html.Div(
                                className="subclass-percentage",
                                children=[
                                    html.Div(className="row", children=[
                                        html.Div(className="col", children=[
                                            Card([
                                                html.Div([
                                                    html.H6("Top 'All Offering' by Subclass", className="percentage-label"),
                                                    html.Span([], id="top_offering_subclass", className="percentage-subclass"),
                                                    html.Div([
                                                        html.Span([], 
                                                        className="percentage-marker-ind"),
                                                        html.Span([], id="top_offering_percentage", className="percentage-value")
                                                    ],className="percentage-marker"),
                                                ], className="subclass-card-center")
                                            ], margin=False)
                                        ])
                                    ]),
                                    html.Div(className="row", children=[
                                        html.Div(className="col", children=[
                                            Card([
                                                html.Div([
                                                    html.H6("Top SHS Track Coverage by Subclass", className="percentage-label"),
                                                    html.Span([], id="top_track_subclass", className="percentage-subclass"),
                                                    html.Span([], id="top_track_percentage", className="percentage-value")
                                                ], className="subclass-card-center")
                                            ], margin=False)

                                        ])
                                    ])
                                ]
                            )
                        ], className="subclass-program-contents")
                    ], className="subclass-program")
                ], className="subclass-right-content")

            ], className="subclass-content")
        ], className='plotted-subclass-report render-plot')
