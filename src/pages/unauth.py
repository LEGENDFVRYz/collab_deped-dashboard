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
dash.register_page(__name__, path="/unauthorized", suppress_callback_exceptions=True)  

layout = html.Div([
    html.Div(
        [
            html.Div("UNAUTHORIZED", className="response-tag"),
            html.Div("Access Denied, You do not have permission to view this page.", className="response-short"),
            html.Div("Please log in if you are a registered user!", className="response-reco")
        ]
    , className='content'),
], className='unauth container')