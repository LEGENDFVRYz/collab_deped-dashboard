from enum import auto
from turtle import title
# from networkx import center
import numpy as np
import pandas as pd
import dash
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, callback, Output, Input, State, Patch
from plotly.subplots import make_subplots 
import os

import json
from geojson_rewind import rewind

# important part
from src.data import enrollment_db_engine, smart_filter

# Extra Utilities
from src.utils.extras_utils import smart_truncate_number



"""
    Analytics/Location Charts and Indicator
    
"""


#################################################################################
##                     MAIN DATAFRAME BASED FROM THE QUERY                     ##
#################################################################################

# # ## -- This only a temporary dataframe for testing your charts, you can change it whatever you want

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# from config import project_root
# from utils.get_data import auto_extract

# FILTERED_DF = dataframe = auto_extract(['counts'], is_specific=False)
# FILTERED_DF

# ## -- Check the document for all valid columns and structurette
# ## -- Dont change the all caps variables

#################################################################################

# ## QUERYY
# @callback(
#     Output('base-trigger', 'data'),
#     Output('render-base', 'children'),
#     Input("url", "pathname"),
#     State('base-trigger', 'data')
# )
# def trigger_base_charts(pathname, base_status):
#     if pathname != "/analytics":
#         return dash.no_update, html.Div([])
    
#     # Initialize DF
#     smart_filter({}, _engine=enrollment_db_engine)
    
#     return (not base_status), dash.no_update





## -- FIND YOUR CHARTS HERE:

################################################################################
##  --- CHART: Distribution of enrollees per location 
#################################################################################

@callback(
    Output('location_enrollees-distribution-per-location', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    # print("triggered dispilinr")
    # Step 1: Group by region and gender
    gender_region = FILTERED_DATA.groupby(['region', 'gender'])['counts'].sum().reset_index()

    # Step 2: Define brand colors
    brand_colors = {
        'M': '#5DB7FF',
        'F': '#FF5B72'
    }

    # Step 3: Create the stacked bar chart
    gender_region_fig = px.bar(
        gender_region,
        x='counts',
        y='region',
        color='gender',
        orientation='h',
        barmode='stack',
        labels={'counts': 'Number of Enrollees', 'region': 'Region', 'gender': 'Gender'},
        color_discrete_map=brand_colors
    )
    

    # Step 4: Calculate total per region for annotations
    region_totals = gender_region.groupby('region')['counts'].sum().reset_index()

    # Step 5: Add truncated total annotations using your function
    for _, row in region_totals.iterrows():
        short_text = smart_truncate_number(row['counts'])  # Your custom truncation
        gender_region_fig.add_annotation(
            x=row['counts'] + 1,
            y=row['region'],
            text=short_text,
            hovertext=str(row['counts']),  # Full raw number on hover
            showarrow=False,
            font=dict(color="#04508c", size=12),
            xanchor="left",
            yanchor="middle"
        )

    # Step 6: Customize layout
    gender_region_fig.update_layout(
        xaxis_title="Number of Students",
        yaxis_title="Region",
        legend_title="Gender",
        font=dict(color="#667889", family='Inter'),
        margin=dict(l=80, r=20, t=20, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # barcornerradius=3,
    )
    gender_region_fig

    return dcc.Graph(figure=gender_region_fig)

#################################################################################




# #################################################################################
# ##  --- CHART: enrollment density (students per location)
# #################################################################################
@callback(
    Output('location_choropleth-map', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
)
def update_province_choropleth_map(trigger, data):
    FILTERED_DF = smart_filter(data, enrollment_db_engine)
    

    FILTERED_DF = FILTERED_DF.groupby('province', as_index=False)['counts'].sum()

    unique_provinces = FILTERED_DF['province'].drop_duplicates().tolist()
    for province in unique_provinces:
        print(province)    
        
        # Print for debug
    unique_provinces = FILTERED_DF['province'].drop_duplicates().tolist()
    print("Provinces in DataFrame:", len(unique_provinces))
    for province in sorted(unique_provinces):
        print(province)

    # Folder where all region-wise GeoJSON files are stored
    geojson_folder = "/Users/marke/Downloads/low/"
    geojson_files = [
        "provdists-region-100000000.0.001",
        "provdists-region-1000000000.0.001",
        "provdists-region-1100000000.0.001",
        "provdists-region-1200000000.0.001",
        "provdists-region-1300000000.0.001",
        "provdists-region-1400000000.0.001",
        "provdists-region-1600000000.0.001",
        "provdists-region-1700000000.0.001",
        "provdists-region-1900000000.0.001",
        "provdists-region-200000000.0.001",
        "provdists-region-300000000.0.001",
        "provdists-region-400000000.0.001",
        "provdists-region-500000000.0.001",
        "provdists-region-600000000.0.001",
        "provdists-region-700000000.0.001",
        "provdists-region-800000000.0.001",
        "provdists-region-900000000.0.001",
    ]

    # Combine all province GeoJSONs into one FeatureCollection
    all_features = []
    for filename in geojson_files:
        filepath = os.path.join(geojson_folder, filename + ".json")
        with open(filepath) as f:
            geo = json.load(f)
            geo = rewind(geo, rfc7946=False)  # Ensure proper winding
            all_features.extend(geo['features'])

    combined_geojson = {
        "type": "FeatureCollection",
        "features": all_features
    }

    # Extract province names from GeoJSON
    geo_provinces = [feature['properties']['adm2_en'] for feature in combined_geojson['features']]
    print("Provinces in GeoJSON:", len(set(geo_provinces)))
    print("Provinces in DataFrame:", set(FILTERED_DF['province']))


    # Normalize casing and whitespace
    FILTERED_DF['normalized_province'] = FILTERED_DF['province'].str.strip().str.title()
    geo_provinces_normalized = [prov.strip().title() for prov in geo_provinces if prov]


    # Keep only matching provinces
    FILTERED_DF = FILTERED_DF[FILTERED_DF['normalized_province'].isin(geo_provinces_normalized)]
    
    # 4. Plotly Choropleth
    map_chart = px.choropleth(
        FILTERED_DF,
        geojson=combined_geojson,
        locations='normalized_province',
        featureidkey='properties.adm2_en',
        color='counts',
        hover_name=None,
        hover_data=None,
        color_continuous_scale='Viridis',
        
    )
    
    map_chart.update_traces(
        hovertemplate="<b>%{location}</b><br>Total Enrollment: %{z:,}<extra></extra>"
    )


    map_chart.update_geos(
        visible=False,
        # showcountries=False,
        # showcoastlines=False,
        showland=True,
        fitbounds="locations",        # Ensures focus on actual geojson features
        center = {'lat':12.8797, 'lon':121.7740},
        resolution=50,
        lataxis_range=[4, 21],        # Latitude range for PH
        lonaxis_range=[115, 128],  # Longitude range for PH
    )



    map_chart.update_layout(
        # title="Enrollment by Region",
        # title_font=dict(size=20, family='Inter', color='#3C6382'),
        # title_x=0.5,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='white',
        plot_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False,
        # dragmode=False,
    )


    return dcc.Graph(
        figure=map_chart,
        style={'width': '100%', 'height': '100%'},
        config={
            'responsive': True,
            # 'scrollZoom': False,      # Disable scroll zooming
            # 'displayModeBar': False,  # Hide the mode bar with zoom/pan controls
            # 'doubleClick': False,     # Disable double-click zooming
            # 'showAxisDragHandles': False,  # Disable axis drag handles
            # 'showTips': False,        # Disable hover tips on modebar
        }
    )



# import os
# import json
# import plotly.express as px
# from dash import dcc, Output, Input, State, callback
# # from utils import smart_filter
# from geojson_rewind import rewind

# @callback(
#     Output('location_choropleth-map', 'children'),
#     Input('chart-trigger', 'data'),
#     State('filtered_values', 'data'),
# )
# def update_municipality_choropleth_map(trigger, data):
#     # 1. Filter the DataFrame
#     FILTERED_DF = smart_filter(data, enrollment_db_engine)
#     FILTERED_DF = FILTERED_DF.groupby('municipality', as_index=False)['counts'].sum()

#     # 2. Load and combine all municipality-level GeoJSON files
#     geojson_folder = "src/assets/geojson/municipalities"
#     geojson_files = [
#   "municities-provdist-1001300000.0.001.json",
#   "municities-provdist-1001800000.0.001.json",
#   "municities-provdist-1003500000.0.001.json",
#   "municities-provdist-1004200000.0.001.json",
#   "municities-provdist-1004300000.0.001.json",
#   "municities-provdist-102800000.0.001.json",
#   "municities-provdist-102900000.0.001.json",
#   "municities-provdist-103300000.0.001.json",
#   "municities-provdist-105500000.0.001.json",
#   "municities-provdist-1102300000.0.001.json",
#   "municities-provdist-1102400000.0.001.json",
#   "municities-provdist-1102500000.0.001.json",
#   "municities-provdist-1108200000.0.001.json",
#   "municities-provdist-1108600000.0.001.json",
#   "municities-provdist-1204700000.0.001.json",
#   "municities-provdist-1206300000.0.001.json",
#   "municities-provdist-1206500000.0.001.json",
#   "municities-provdist-1208000000.0.001.json",
#   "municities-provdist-1303900000.0.001.json",
#   "municities-provdist-1307400000.0.001.json",
#   "municities-provdist-1307500000.0.001.json",
#   "municities-provdist-1307600000.0.001.json",
#   "municities-provdist-1400100000.0.001.json",
#   "municities-provdist-1401100000.0.001.json",
#   "municities-provdist-1402700000.0.001.json",
#   "municities-provdist-1403200000.0.001.json",
#   "municities-provdist-1404400000.0.001.json",
#   "municities-provdist-1408100000.0.001.json",
#   "municities-provdist-1600200000.0.001.json",
#   "municities-provdist-1600300000.0.001.json",
#   "municities-provdist-1606700000.0.001.json",
#   "municities-provdist-1606800000.0.001.json",
#   "municities-provdist-1608500000.0.001.json",
#   "municities-provdist-1704000000.0.001.json",
#   "municities-provdist-1705100000.0.001.json",
#   "municities-provdist-1705200000.0.001.json",
#   "municities-provdist-1705300000.0.001.json",
#   "municities-provdist-1705900000.0.001.json",
#   "municities-provdist-1900700000.0.001.json",
#   "municities-provdist-1903600000.0.001.json",
#   "municities-provdist-1906600000.0.001.json",
#   "municities-provdist-1907000000.0.001.json",
#   "municities-provdist-1908700000.0.001.json",
#   "municities-provdist-1908800000.0.001.json",
#   "municities-provdist-1909900000.0.001.json",
#   "municities-provdist-200900000.0.001.json",
#   "municities-provdist-201500000.0.001.json",
#   "municities-provdist-203100000.0.001.json",
#   "municities-provdist-205000000.0.001.json",
#   "municities-provdist-205700000.0.001.json",
#   "municities-provdist-300800000.0.001.json",
#   "municities-provdist-301400000.0.001.json",
#   "municities-provdist-304900000.0.001.json",
#   "municities-provdist-305400000.0.001.json",
#   "municities-provdist-306900000.0.001.json",
#   "municities-provdist-307100000.0.001.json",
#   "municities-provdist-307700000.0.001.json",
#   "municities-provdist-401000000.0.001.json",
#   "municities-provdist-402100000.0.001.json",
#   "municities-provdist-403400000.0.001.json",
#   "municities-provdist-405600000.0.001.json",
#   "municities-provdist-405800000.0.001.json",
#   "municities-provdist-500500000.0.001.json",
#   "municities-provdist-501600000.0.001.json",
#   "municities-provdist-501700000.0.001.json",
#   "municities-provdist-502000000.0.001.json",
#   "municities-provdist-504100000.0.001.json",
#   "municities-provdist-506200000.0.001.json",
#   "municities-provdist-600400000.0.001.json",
#   "municities-provdist-600600000.0.001.json",
#   "municities-provdist-601900000.0.001.json",
#   "municities-provdist-603000000.0.001.json",
#   "municities-provdist-604500000.0.001.json",
#   "municities-provdist-607900000.0.001.json",
#   "municities-provdist-701200000.0.001.json",
#   "municities-provdist-702200000.0.001.json",
#   "municities-provdist-704600000.0.001.json",
#   "municities-provdist-706100000.0.001.json",
#   "municities-provdist-802600000.0.001.json",
#   "municities-provdist-803700000.0.001.json",
#   "municities-provdist-804800000.0.001.json",
#   "municities-provdist-806000000.0.001.json",
#   "municities-provdist-806400000.0.001.json",
#   "municities-provdist-807800000.0.001.json",
#   "municities-provdist-907200000.0.001.json",
#   "municities-provdist-907300000.0.001.json",
#   "municities-provdist-908300000.0.001.json",
#   "municities-provdist-990100000.0.001.json"


#     ]

#     combined_features = []

#     for file in geojson_files:
#         path = os.path.join(geojson_folder, file)
#         with open(path) as f:
#             gj = json.load(f)
#             combined_features.extend(gj['features'])

#     geojson = {
#         "type": "FeatureCollection",
#         "features": combined_features
#     }

#     geojson = rewind(geojson, rfc7946=False)

#     # 3. Plot the Choropleth Map
#     map_chart = px.choropleth(
#         FILTERED_DF,
#         geojson=geojson,
#         locations='municipality',
#         featureidkey='adm3_en',
#         color='counts',
#         hover_name=None,
#         hover_data=None,
#         color_continuous_scale='Viridis',
#     )

#     map_chart.update_traces(
#         hovertemplate="<b>%{location}</b><br>Total Enrollment: %{z:,}<extra></extra>"
#     )

#     map_chart.update_geos(
#         visible=False,
#         showland=True,
#         fitbounds="locations",
#         center={'lat': 12.8797, 'lon': 121.7740},
#         resolution=50,
#         lataxis_range=[4, 21],
#         lonaxis_range=[115, 128],
#     )

#     map_chart.update_layout(
#         margin={"r": 0, "t": 0, "l": 0, "b": 0},
#         paper_bgcolor='white',
#         plot_bgcolor='rgba(0,0,0,0)',
#         coloraxis_showscale=False,
#     )

#     return dcc.Graph(
#         figure=map_chart,
#         style={'width': '100%', 'height': '100%'},
#         config={
#             'responsive': True,
#         }
#     )


# import json
# import pandas as pd
# import plotly.express as px
# from dash import dcc, Output, Input, State, callback
# from geojson_rewind import rewind

# # Mapping of provinces to regions (use full GeoJSON naming format)
# province_to_region = {
#     # Region I
#     "PANGASINAN": "Region I (Ilocos Region)",
#     "ILOCOS NORTE": "Region I (Ilocos Region)",
#     "ILOCOS SUR": "Region I (Ilocos Region)",
#     "LA UNION": "Region I (Ilocos Region)",

#     # CAR
#     "ABRA": "Cordillera Administrative Region (CAR)",
#     "APAYAO": "Cordillera Administrative Region (CAR)",
#     "BENGUET": "Cordillera Administrative Region (CAR)",
#     "IFUGAO": "Cordillera Administrative Region (CAR)",
#     "KALINGA": "Cordillera Administrative Region (CAR)",
#     "MOUNTAIN PROVINCE": "Cordillera Administrative Region (CAR)",

#     # Region II
#     "CAGAYAN": "Region II (Cagayan Valley)",
#     "ISABELA": "Region II (Cagayan Valley)",
#     "NUEVA VIZCAYA": "Region II (Cagayan Valley)",
#     "QUIRINO": "Region II (Cagayan Valley)",
#     "BATANES": "Region II (Cagayan Valley)",

#     # Region III
#     "AURORA": "Region III (Central Luzon)",
#     "BATAAN": "Region III (Central Luzon)",
#     "BULACAN": "Region III (Central Luzon)",
#     "NUEVA ECIJA": "Region III (Central Luzon)",
#     "PAMPANGA": "Region III (Central Luzon)",
#     "TARLAC": "Region III (Central Luzon)",
#     "ZAMBALES": "Region III (Central Luzon)",

#     # Region IV-A
#     "BATANGAS": "Region IV-A (CALABARZON)",
#     "CAVITE": "Region IV-A (CALABARZON)",
#     "LAGUNA": "Region IV-A (CALABARZON)",
#     "QUEZON": "Region IV-A (CALABARZON)",
#     "RIZAL": "Region IV-A (CALABARZON)",

#     # MIMAROPA
#     "MARINDUQUE": "MIMAROPA Region",
#     "OCCIDENTAL MINDORO": "MIMAROPA Region",
#     "ORIENTAL MINDORO": "MIMAROPA Region",
#     "PALAWAN": "MIMAROPA Region",
#     "ROMBLON": "MIMAROPA Region",

#     # Region V
#     "ALBAY": "Region V (Bicol Region)",
#     "CAMARINES NORTE": "Region V (Bicol Region)",
#     "CAMARINES SUR": "Region V (Bicol Region)",
#     "CATANDUANES": "Region V (Bicol Region)",
#     "MASBATE": "Region V (Bicol Region)",
#     "SORSOGON": "Region V (Bicol Region)",

#     # Region VI
#     "AKLAN": "Region VI (Western Visayas)",
#     "ANTIQUE": "Region VI (Western Visayas)",
#     "CAPIZ": "Region VI (Western Visayas)",
#     "GUIMARAS": "Region VI (Western Visayas)",
#     "ILOILO": "Region VI (Western Visayas)",
#     "NEGROS OCCIDENTAL": "Region VI (Western Visayas)",

#     # Region VII
#     "BOHOL": "Region VII (Central Visayas)",
#     "CEBU": "Region VII (Central Visayas)",
#     "NEGROS ORIENTAL": "Region VII (Central Visayas)",
#     "SIQUIJOR": "Region VII (Central Visayas)",

#     # Region VIII
#     "BILIRAN": "Region VIII (Eastern Visayas)",
#     "EASTERN SAMAR": "Region VIII (Eastern Visayas)",
#     "LEYTE": "Region VIII (Eastern Visayas)",
#     "NORTHERN SAMAR": "Region VIII (Eastern Visayas)",
#     "SOUTHERN LEYTE": "Region VIII (Eastern Visayas)",
#     "WESTERN SAMAR": "Region VIII (Eastern Visayas)",

#     # Region IX
#     "ZAMBOANGA DEL NORTE": "Region IX (Zamboanga Peninsula)",
#     "ZAMBOANGA DEL SUR": "Region IX (Zamboanga Peninsula)",
#     "ZAMBOANGA SIBUGAY": "Region IX (Zamboanga Peninsula)",

#     # Region X
#     "BUKIDNON": "Region X (Northern Mindanao)",
#     "CAMIGUIN": "Region X (Northern Mindanao)",
#     "LANAO DEL NORTE": "Region X (Northern Mindanao)",
#     "MISAMIS OCCIDENTAL": "Region X (Northern Mindanao)",
#     "MISAMIS ORIENTAL": "Region X (Northern Mindanao)",

#     # Region XI
#     "COMPOSTELA VALLEY": "Region XI (Davao Region)",
#     "DAVAO DEL NORTE": "Region XI (Davao Region)",
#     "DAVAO DEL SUR": "Region XI (Davao Region)",
#     "DAVAO OCCIDENTAL": "Region XI (Davao Region)",
#     "DAVAO ORIENTAL": "Region XI (Davao Region)",

#     # Region XII
#     "NORTH COTABATO": "Region XII (SOCCSKSARGEN)",
#     "SOUTH COTABATO": "Region XII (SOCCSKSARGEN)",
#     "SULTAN KUDARAT": "Region XII (SOCCSKSARGEN)",
#     "SARANGANI": "Region XII (SOCCSKSARGEN)",
#     "CITY OF COTABATO": "Region XII (SOCCSKSARGEN)",
#     "CITY OF ISABELA": "Region XII (SOCCSKSARGEN)",

#     # Region XIII (Caraga)
#     "AGUSAN DEL NORTE": "Region XIII (Caraga)",
#     "AGUSAN DEL SUR": "Region XIII (Caraga)",
#     "SURIGAO DEL NORTE": "Region XIII (Caraga)",
#     "SURIGAO DEL SUR": "Region XIII (Caraga)",
#     "DINAGAT ISLANDS": "Region XIII (Caraga)",

#     # BARMM
#     "BASILAN": "Bangsamoro Autonomous Region In Muslim Mindanao (BARMM)",
#     "LANAO DEL SUR": "Bangsamoro Autonomous Region In Muslim Mindanao (BARMM)",
#     "MAGUINDANAO": "Bangsamoro Autonomous Region In Muslim Mindanao (BARMM)",
#     "SULU": "Bangsamoro Autonomous Region In Muslim Mindanao (BARMM)",
#     "TAWI-TAWI": "Bangsamoro Autonomous Region In Muslim Mindanao (BARMM)",

#     # NCR
#     "MANILA, NCR, FIRST DISTRICT": "National Capital Region (NCR)",
#     "NCR SECOND DISTRICT": "National Capital Region (NCR)",
#     "NCR THIRD DISTRICT": "National Capital Region (NCR)",
#     "NCR FOURTH DISTRICT": "National Capital Region (NCR)",
# }

# @callback(
#     Output('location_choropleth-map', 'children'),
#     Input('chart-trigger', 'data'),
#     State('filtered_values', 'data'),
# )
# def update_choropleth_map(trigger, data):
#     # 1. Filter and group by province
#     df = smart_filter(data, enrollment_db_engine)
#     df['region_name'] = df['province'].map(province_to_region)
#     df = df.dropna(subset=['region_name'])
#     df = df.groupby('region_name', as_index=False)['counts'].sum()

#     # 2. Load and rewind GeoJSON
#     with open("/Users/marke/Downloads/country.0.001.json") as f:
#         geojson = json.load(f)
#     geojson = rewind(geojson, rfc7946=False)

#     # 3. Create Choropleth
#     map_chart = px.choropleth(
#         df,
#         geojson=geojson,
#         locations='region_name',
#         featureidkey='properties.adm1_en',
#         color='counts',
#         hover_name=None,
#         hover_data=None,
#         color_continuous_scale='Viridis',
#     )

#     map_chart.update_traces(
#         hovertemplate="<b>%{location}</b><br>Total Enrollment: %{z:,}<extra></extra>"
#     )

#     map_chart.update_geos(
#         visible=False,
#         showcountries=False,
#         showcoastlines=False,
#         showland=True,
#         fitbounds="geojson",
#         resolution=50,
#         lataxis_range=[4, 22],
#         lonaxis_range=[115, 128],
#     )

#     map_chart.update_layout(
#         margin={"r": 0, "t": 0, "l": 0, "b": 0},
#         paper_bgcolor='black',
#         plot_bgcolor='rgba(0,0,0,0)',
#         coloraxis_showscale=False,
#     )

#     return dcc.Graph(
#         figure=map_chart,
#         style={'width': '100%', 'height': '100%'},
#         config={'responsive': True}
#     )


# ####regions
# @callback(
#     Output('location_choropleth-map', 'children'),
#     Input('chart-trigger', 'data'),
#     State('filtered_values', 'data'),
# )
# def update_choropleth_map(trigger, data):
#     # 1. Filtered Data
#     FILTERED_DF = smart_filter(data, enrollment_db_engine)
#     FILTERED_DF = FILTERED_DF.groupby('region', as_index=False)['counts'].sum()

#     # 2. GeoJSON (PH admin boundaries)
#     with open("src/assets/geojson/region/country.0.001.json") as f:
#         geojson = json.load(f)

#     geojson = rewind(geojson, rfc7946=False)

#     # 3. Region Name Mapping (GeoJSON naming standard)
#     region_name_map = {
#         'Region I': 'Region I (Ilocos Region)',
#         'Region II': 'Region II (Cagayan Valley)',
#         'Region III': 'Region III (Central Luzon)',
#         'Region IV-A': 'Region IV-A (CALABARZON)',
#         'Region IV-B': 'MIMAROPA Region',
#         'Region V': 'Region V (Bicol Region)',
#         'Region VI': 'Region VI (Western Visayas)',
#         'Region VII': 'Region VII (Central Visayas)',
#         'Region VIII': 'Region VIII (Eastern Visayas)',
#         'Region IX': 'Region IX (Zamboanga Peninsula)',
#         'Region X': 'Region X (Northern Mindanao)',
#         'Region XI': 'Region XI (Davao Region)',
#         'Region XII': 'Region XII (SOCCSKSARGEN)',
#         'CARAGA': 'Region XIII (Caraga)',
#         'NCR': 'National Capital Region (NCR)',
#         'CAR': 'Cordillera Administrative Region (CAR)',
#         'BARMM': 'Bangsamoro Autonomous Region In Muslim Mindanao (BARMM)',
#     }

#     FILTERED_DF['geo_region'] = FILTERED_DF['region'].map(region_name_map)
#     FILTERED_DF = FILTERED_DF.dropna(subset=['geo_region'])

#     # 4. Plotly Choropleth
#     map_chart = px.choropleth(
#         FILTERED_DF,
#         geojson=geojson,
#         locations='geo_region',
#         featureidkey='properties.adm1_en',
#         color='counts',
#         hover_name=None,
#         hover_data=None,
#         color_continuous_scale='Viridis',
        
#     )
    
#     map_chart.update_traces(
#         hovertemplate="<b>%{location}</b><br>Total Enrollment: %{z:,}<extra></extra>"
#     )


#     map_chart.update_geos(
#         visible=False,
#         # showcountries=False,
#         # showcoastlines=False,
#         showland=True,
#         fitbounds="locations",        # Ensures focus on actual geojson features
#         center = {'lat':12.8797, 'lon':121.7740},
#         resolution=50,
#         lataxis_range=[4, 21],        # Latitude range for PH
#         lonaxis_range=[115, 128],  # Longitude range for PH
#     )



#     map_chart.update_layout(
#         # title="Enrollment by Region",
#         # title_font=dict(size=20, family='Inter', color='#3C6382'),
#         # title_x=0.5,
#         margin={"r": 0, "t": 0, "l": 0, "b": 0},
#         paper_bgcolor='white',
#         plot_bgcolor='rgba(0,0,0,0)',
#         coloraxis_showscale=False,
#         # dragmode=False,
#     )

#     return dcc.Graph(
#         figure=map_chart,
#         style={'width': '100%', 'height': '100%'},
#         config={
#             'responsive': True,
#             # 'scrollZoom': False,      # Disable scroll zooming
#             # 'displayModeBar': False,  # Hide the mode bar with zoom/pan controls
#             # 'doubleClick': False,     # Disable double-click zooming
#             # 'showAxisDragHandles': False,  # Disable axis drag handles
#             # 'showTips': False,        # Disable hover tips on modebar
#         }
#     )

###province

# from dash import dcc, callback, Input, Output, State
# import plotly.express as px
# import pandas as pd
# import os
# import json
# from geojson_rewind import rewind

# @callback(
#     Output('location_choropleth-map', 'children'),
#     Input('chart-trigger', 'data'),
#     State('filtered_values', 'data'),
# )
# def update_province_choropleth(trigger, data):
#     # 1. Filter Data
#     FILTERED_DF = smart_filter(data, enrollment_db_engine)
#     FILTERED_DF = FILTERED_DF.groupby('province', as_index=False)['counts'].sum()

#     # 2. Load and combine GeoJSON files
#     geojson_folder = "src/assets/geojson/provinces"
#     geojson_files = [
#         "provdists-region-100000000.0.1",
#         "provdists-region-1000000000.0.1",
#         "provdists-region-1100000000.0.1",
#         "provdists-region-1200000000.0.1",
#         "provdists-region-1300000000.0.1",
#         "provdists-region-1400000000.0.1",
#         "provdists-region-1600000000.0.1",
#         "provdists-region-1700000000.0.1",
#         "provdists-region-1900000000.0.1",
#         "provdists-region-200000000.0.1",
#         "provdists-region-300000000.0.1",
#         "provdists-region-400000000.0.1",
#         "provdists-region-500000000.0.1",
#         "provdists-region-600000000.0.1",
#         "provdists-region-700000000.0.1",
#         "provdists-region-800000000.0.1",
#         "provdists-region-900000000.0.1",
#     ]

#     all_features = []
#     for filename in geojson_files:
#         filepath = os.path.join(geojson_folder, filename + ".json")
#         with open(filepath) as f:
#             geo = json.load(f)
#             geo = rewind(geo, rfc7946=False)
#             all_features.extend(geo['features'])

#     combined_geojson = {
#         "type": "FeatureCollection",
#         "features": all_features
#     }

#     # 3. Province Name Mapping
#     province_name_map = {
#         'Abra': 'ABRA',
#         'Agusan del Norte': 'AGUSAN DEL NORTE',
#         'Agusan del Sur': 'AGUSAN DEL SUR',
#         'Aklan': 'AKLAN',
#         'Albay': 'ALBAY',
#         'Antique': 'ANTIQUE',
#         'Apayao': 'APAYAO',
#         'Aurora': 'AURORA',
#         'Basilan': 'BASILAN',
#         'Bataan': 'BATAAN',
#         'Batanes': 'BATANES',
#         'Batangas': 'BATANGAS',
#         'Benguet': 'BENGUET',
#         'Biliran': 'BILIRAN',
#         'Bohol': 'BOHOL',
#         'Bukidnon': 'BUKIDNON',
#         'Bulacan': 'BULACAN',
#         'Cagayan': 'CAGAYAN',
#         'Camarines Norte': 'CAMARINES NORTE',
#         'Camarines Sur': 'CAMARINES SUR',
#         'Camiguin': 'CAMIGUIN',
#         'Capiz': 'CAPIZ',
#         'Catanduanes': 'CATANDUANES',
#         'Cavite': 'CAVITE',
#         'Cebu': 'CEBU',
#         'Compostela Valley': 'COMPOSTELA VALLEY',
#         'Davao de Oro': 'COMPOSTELA VALLEY',
#         'Davao del Norte': 'DAVAO DEL NORTE',
#         'Davao del Sur': 'DAVAO DEL SUR',
#         'Davao Occidental': 'DAVAO OCCIDENTAL',
#         'Davao Oriental': 'DAVAO ORIENTAL',
#         'Dinagat Islands': 'DINAGAT ISLANDS',
#         'Eastern Samar': 'EASTERN SAMAR',
#         'Guimaras': 'GUIMARAS',
#         'Ifugao': 'IFUGAO',
#         'Ilocos Norte': 'ILOCOS NORTE',
#         'Ilocos Sur': 'ILOCOS SUR',
#         'Iloilo': 'ILOILO',
#         'Isabela': 'ISABELA',
#         'Kalinga': 'KALINGA',
#         'La Union': 'LA UNION',
#         'Laguna': 'LAGUNA',
#         'Lanao del Norte': 'LANAO DEL NORTE',
#         'Lanao del Sur': 'LANAO DEL SUR',
#         'Leyte': 'LEYTE',
#         'Maguindanao del Norte': 'MAGUINDANAO',
#         'Maguindanao del Sur': 'MAGUINDANAO',
#         'Marinduque': 'MARINDUQUE',
#         'Masbate': 'MASBATE',
#         'Mountain Province': 'MOUNTAIN PROVINCE',
#         'Misamis Occidental': 'MISAMIS OCCIDENTAL',
#         'Misamis Oriental': 'MISAMIS ORIENTAL',
#         'Negros Occidental': 'NEGROS OCCIDENTAL',
#         'Negros Oriental': 'NEGROS ORIENTAL',
#         'Northern Samar': 'NORTHERN SAMAR',
#         'Nueva Ecija': 'NUEVA ECIJA',
#         'Nueva Vizcaya': 'NUEVA VIZCAYA',
#         'Occidental Mindoro': 'OCCIDENTAL MINDORO',
#         'Oriental Mindoro': 'ORIENTAL MINDORO',
#         'Palawan': 'PALAWAN',
#         'Pampanga': 'PAMPANGA',
#         'Pangasinan': 'PANGASINAN',
#         'Quezon': 'QUEZON',
#         'Quirino': 'QUIRINO',
#         'Rizal': 'RIZAL',
#         'Romblon': 'ROMBLON',
#         'Samar': 'WESTERN SAMAR',
#         'Sarangani': 'SARANGANI',
#         'Siquijor': 'SIQUIJOR',
#         'Sorsogon': 'SORSOGON',
#         'South Cotabato': 'SOUTH COTABATO',
#         'Southern Leyte': 'SOUTHERN LEYTE',
#         'Sultan Kudarat': 'SULTAN KUDARAT',
#         'Sulu': 'SULU',
#         'Surigao del Norte': 'SURIGAO DEL NORTE',
#         'Surigao del Sur': 'SURIGAO DEL SUR',
#         'Tarlac': 'TARLAC',
#         'Tawi-Tawi': 'TAWI-TAWI',
#         'Zambales': 'ZAMBALES',
#         'Zamboanga del Norte': 'ZAMBOANGA DEL NORTE',
#         'Zamboanga del Sur': 'ZAMBOANGA DEL SUR',
#         'Zamboanga Sibugay': 'ZAMBOANGA SIBUGAY',
#         'NCR, Second District (Not a Province)': 'NCR   SECOND DISTRICT',
#         'NCR, Third District (Not a Province)': 'NCR   THIRD DISTRICT',
#         'NCR, Fourth District (Not a Province)': 'NCR   FOURTH DISTRICT',
#         'NCR, City of Manila, First District (Not a Province)': 'MANILA, NCR,  FIRST DISTRICT ',
#         'City of Isabela (Not a Province)': 'CITY OF ISABELA',
#         'Cotabato': 'CITY OF COTABATO',
#     }
    
#     province_to_region = {
#     # Region I - Ilocos Region
#     'Ilocos Norte': 'Region I',
#     'Ilocos Sur': 'Region I',
#     'La Union': 'Region I',
#     'Pangasinan': 'Region I',

#     # Region II - Cagayan Valley
#     'Batanes': 'Region II',
#     'Cagayan': 'Region II',
#     'Isabela': 'Region II',
#     'Nueva Vizcaya': 'Region II',
#     'Quirino': 'Region II',

#     # Region III - Central Luzon
#     'Aurora': 'Region III',
#     'Bataan': 'Region III',
#     'Bulacan': 'Region III',
#     'Nueva Ecija': 'Region III',
#     'Pampanga': 'Region III',
#     'Tarlac': 'Region III',
#     'Zambales': 'Region III',

#     # Region IV-A - CALABARZON
#     'Batangas': 'Region IV-A',
#     'Cavite': 'Region IV-A',
#     'Laguna': 'Region IV-A',
#     'Quezon': 'Region IV-A',
#     'Rizal': 'Region IV-A',

#     # Region IV-B - MIMAROPA
#     'Marinduque': 'Region IV-B',
#     'Occidental Mindoro': 'Region IV-B',
#     'Oriental Mindoro': 'Region IV-B',
#     'Palawan': 'Region IV-B',
#     'Romblon': 'Region IV-B',

#     # Region V - Bicol Region
#     'Albay': 'Region V',
#     'Camarines Norte': 'Region V',
#     'Camarines Sur': 'Region V',
#     'Catanduanes': 'Region V',
#     'Masbate': 'Region V',
#     'Sorsogon': 'Region V',

#     # Region VI - Western Visayas
#     'Aklan': 'Region VI',
#     'Antique': 'Region VI',
#     'Capiz': 'Region VI',
#     'Guimaras': 'Region VI',
#     'Iloilo': 'Region VI',
#     'Negros Occidental': 'Region VI',

#     # Region VII - Central Visayas
#     'Bohol': 'Region VII',
#     'Cebu': 'Region VII',
#     'Negros Oriental': 'Region VII',
#     'Siquijor': 'Region VII',

#     # Region VIII - Eastern Visayas
#     'Biliran': 'Region VIII',
#     'Eastern Samar': 'Region VIII',
#     'Leyte': 'Region VIII',
#     'Northern Samar': 'Region VIII',
#     'Samar': 'Region VIII',  # aka Western Samar
#     'Southern Leyte': 'Region VIII',

#     # Region IX - Zamboanga Peninsula
#     'Zamboanga del Norte': 'Region IX',
#     'Zamboanga del Sur': 'Region IX',
#     'Zamboanga Sibugay': 'Region IX',

#     # Region X - Northern Mindanao
#     'Bukidnon': 'Region X',
#     'Camiguin': 'Region X',
#     'Lanao del Norte': 'Region X',
#     'Misamis Occidental': 'Region X',
#     'Misamis Oriental': 'Region X',

#     # Region XI - Davao Region
#     'Davao de Oro': 'Region XI',  # aka Compostela Valley
#     'Davao del Norte': 'Region XI',
#     'Davao del Sur': 'Region XI',
#     'Davao Occidental': 'Region XI',
#     'Davao Oriental': 'Region XI',

#     # Region XII - SOCCSKSARGEN
#     'Cotabato': 'Region XII',  # aka North Cotabato or Cotabato Province
#     'Sarangani': 'Region XII',
#     'South Cotabato': 'Region XII',
#     'Sultan Kudarat': 'Region XII',

#     # Region XIII - CARAGA
#     'Agusan del Norte': 'CARAGA',
#     'Agusan del Sur': 'CARAGA',
#     'Dinagat Islands': 'CARAGA',
#     'Surigao del Norte': 'CARAGA',
#     'Surigao del Sur': 'CARAGA',

#     # CAR - Cordillera Administrative Region
#     'Abra': 'CAR',
#     'Apayao': 'CAR',
#     'Benguet': 'CAR',
#     'Ifugao': 'CAR',
#     'Kalinga': 'CAR',
#     'Mountain Province': 'CAR',

#     # BARMM - Bangsamoro Autonomous Region in Muslim Mindanao
#     'Basilan': 'BARMM',
#     'Lanao del Sur': 'BARMM',
#     'Maguindanao del Norte': 'BARMM',
#     'Maguindanao del Sur': 'BARMM',
#     'Sulu': 'BARMM',
#     'Tawi-Tawi': 'BARMM',
#     'City of Isabela (Not a Province)': 'BARMM',
#     'Cotabato': 'BARMM',  # For Cotabato City (distinct from Cotabato Province)

#     # NCR - National Capital Region
#     'NCR, Second District (Not a Province)': 'NCR',
#     'NCR, Third District (Not a Province)': 'NCR',
#     'NCR, Fourth District (Not a Province)': 'NCR',
#     'NCR, City of Manila, First District (Not a Province)': 'NCR',

#     # PSO (Placeholder / Unspecified or special office)
#     'City of Cotabato': 'PSO',

#     # Notes on special cases
#     'Compostela Valley': 'Region XI',  # historical name for Davao de Oro
# }


#     inverse_map = {v: k for k, v in province_name_map.items()}
#     FILTERED_DF['geo_province'] = FILTERED_DF['province'].map(inverse_map).fillna(FILTERED_DF['province'])
#     FILTERED_DF['region'] = FILTERED_DF['geo_province'].map(province_to_region)


#     geo_provinces = [feature['properties']['adm2_en'] for feature in combined_geojson['features']]
#     FILTERED_DF = FILTERED_DF[FILTERED_DF['geo_province'].isin(geo_provinces)]

#     # 4. Plotly Choropleth
#     map_chart = px.choropleth(
#         FILTERED_DF,
#         geojson=combined_geojson,
#         locations='geo_province',
#         featureidkey='properties.adm2_en',
#         color='counts',
#         hover_name=None,
#         hover_data=None,
#         color_continuous_scale='Viridis',
#     )

#     map_chart.update_traces(
#         hovertemplate="<b>%{location}</b><br>Total Enrollment: %{z:,}<extra></extra>"
#     )

#     map_chart.update_geos(
        # visible=False,
        # showcountries=False,
        # showcoastlines=False,
        # showland=True,
        # fitbounds="locations",
        # resolution=50,
        # lataxis_range=[4, 22],
        # lonaxis_range=[115, 128],
#     )

#     map_chart.update_layout(
        # margin={"r": 0, "t": 0, "l": 0, "b": 0},
        # paper_bgcolor='black',
        # plot_bgcolor='rgba(0,0,0,0)',
        # coloraxis_showscale=False,
#     )

#     return dcc.Graph(
#         figure=map_chart,
#         style={'width': '100%', 'height': '100%'},
#         config={'responsive': True}
#     )


###################both attempt
# @callback(
#     Output('location_choropleth-map', 'children'),
#     Input('chart-trigger', 'data'),
#     State('filtered_values', 'data'),
# )
# def update_choropleth_map_with_provinces(trigger, data):
#     # 1. Filtered Data (aggregated by province, then mapped to region)
#     FILTERED_DF = smart_filter(data, enrollment_db_engine)
#     FILTERED_DF = FILTERED_DF.groupby(['region', 'province'], as_index=False)['counts'].sum()

#     # 2. GeoJSON Files (Province-level)
#     geojson_folder = "/Users/marke/Downloads/"
#     geojson_files = [
#         "provdists-region-100000000.0.001",
#         "provdists-region-1000000000.0.001",
#         "provdists-region-1100000000.0.001",
#         "provdists-region-1200000000.0.001",
#         "provdists-region-1300000000.0.001",
#         "provdists-region-1400000000.0.001",
#         "provdists-region-1600000000.0.001",
#         "provdists-region-1700000000.0.001",
#         "provdists-region-1900000000.0.001",
#         "provdists-region-200000000.0.001",
#         "provdists-region-300000000.0.001",
#         "provdists-region-400000000.0.001",
#         "provdists-region-500000000.0.001",
#         "provdists-region-600000000.0.001",
#         "provdists-region-700000000.0.001",
#         "provdists-region-800000000.0.001",
#         "provdists-region-900000000.0.001",
#     ]

#     all_features = []
#     for filename in geojson_files:
#         filepath = os.path.join(geojson_folder, filename + ".json")
#         with open(filepath) as f:
#             geo = json.load(f)
#             geo = rewind(geo, rfc7946=False)
#             all_features.extend(geo['features'])

#     combined_geojson = {
#         "type": "FeatureCollection",
#         "features": all_features
#     }

#     # 3. Province Name Mapping
#     province_name_map = {
#         'Abra': 'ABRA',
#         'Agusan del Norte': 'AGUSAN DEL NORTE',
#         'Agusan del Sur': 'AGUSAN DEL SUR',
#         'Aklan': 'AKLAN',
#         'Albay': 'ALBAY',
#         'Antique': 'ANTIQUE',
#         'Apayao': 'APAYAO',
#         'Aurora': 'AURORA',
#         'Basilan': 'BASILAN',
#         'Bataan': 'BATAAN',
#         'Batanes': 'BATANES',
#         'Batangas': 'BATANGAS',
#         'Benguet': 'BENGUET',
#         'Biliran': 'BILIRAN',
#         'Bohol': 'BOHOL',
#         'Bukidnon': 'BUKIDNON',
#         'Bulacan': 'BULACAN',
#         'Cagayan': 'CAGAYAN',
#         'Camarines Norte': 'CAMARINES NORTE',
#         'Camarines Sur': 'CAMARINES SUR',
#         'Camiguin': 'CAMIGUIN',
#         'Capiz': 'CAPIZ',
#         'Catanduanes': 'CATANDUANES',
#         'Cavite': 'CAVITE',
#         'Cebu': 'CEBU',
#         'Compostela Valley': 'COMPOSTELA VALLEY',
#         'Davao de Oro': 'COMPOSTELA VALLEY',
#         'Davao del Norte': 'DAVAO DEL NORTE',
#         'Davao del Sur': 'DAVAO DEL SUR',
#         'Davao Occidental': 'DAVAO OCCIDENTAL',
#         'Davao Oriental': 'DAVAO ORIENTAL',
#         'Dinagat Islands': 'DINAGAT ISLANDS',
#         'Eastern Samar': 'EASTERN SAMAR',
#         'Guimaras': 'GUIMARAS',
#         'Ifugao': 'IFUGAO',
#         'Ilocos Norte': 'ILOCOS NORTE',
#         'Ilocos Sur': 'ILOCOS SUR',
#         'Iloilo': 'ILOILO',
#         'Isabela': 'ISABELA',
#         'Kalinga': 'KALINGA',
#         'La Union': 'LA UNION',
#         'Laguna': 'LAGUNA',
#         'Lanao del Norte': 'LANAO DEL NORTE',
#         'Lanao del Sur': 'LANAO DEL SUR',
#         'Leyte': 'LEYTE',
#         'Maguindanao del Norte': 'MAGUINDANAO',
#         'Maguindanao del Sur': 'MAGUINDANAO',
#         'Marinduque': 'MARINDUQUE',
#         'Masbate': 'MASBATE',
#         'Mountain Province': 'MOUNTAIN PROVINCE',
#         'Misamis Occidental': 'MISAMIS OCCIDENTAL',
#         'Misamis Oriental': 'MISAMIS ORIENTAL',
#         'Negros Occidental': 'NEGROS OCCIDENTAL',
#         'Negros Oriental': 'NEGROS ORIENTAL',
#         'Northern Samar': 'NORTHERN SAMAR',
#         'Nueva Ecija': 'NUEVA ECIJA',
#         'Nueva Vizcaya': 'NUEVA VIZCAYA',
#         'Occidental Mindoro': 'OCCIDENTAL MINDORO',
#         'Oriental Mindoro': 'ORIENTAL MINDORO',
#         'Palawan': 'PALAWAN',
#         'Pampanga': 'PAMPANGA',
#         'Pangasinan': 'PANGASINAN',
#         'Quezon': 'QUEZON',
#         'Quirino': 'QUIRINO',
#         'Rizal': 'RIZAL',
#         'Romblon': 'ROMBLON',
#         'Samar': 'WESTERN SAMAR',
#         'Sarangani': 'SARANGANI',
#         'Siquijor': 'SIQUIJOR',
#         'Sorsogon': 'SORSOGON',
#         'South Cotabato': 'SOUTH COTABATO',
#         'Southern Leyte': 'SOUTHERN LEYTE',
#         'Sultan Kudarat': 'SULTAN KUDARAT',
#         'Sulu': 'SULU',
#         'Surigao del Norte': 'SURIGAO DEL NORTE',
#         'Surigao del Sur': 'SURIGAO DEL SUR',
#         'Tarlac': 'TARLAC',
#         'Tawi-Tawi': 'TAWI-TAWI',
#         'Zambales': 'ZAMBALES',
#         'Zamboanga del Norte': 'ZAMBOANGA DEL NORTE',
#         'Zamboanga del Sur': 'ZAMBOANGA DEL SUR',
#         'Zamboanga Sibugay': 'ZAMBOANGA SIBUGAY',
#         'NCR, Second District (Not a Province)': 'NCR   SECOND DISTRICT',
#         'NCR, Third District (Not a Province)': 'NCR   THIRD DISTRICT',
#         'NCR, Fourth District (Not a Province)': 'NCR   FOURTH DISTRICT',
#         'NCR, City of Manila, First District (Not a Province)': 'MANILA, NCR,  FIRST DISTRICT ',
#         'City of Isabela (Not a Province)': 'CITY OF ISABELA',
#         'Cotabato': 'CITY OF COTABATO',
#     }

#     inverse_map = {v: k for k, v in province_name_map.items()}
#     FILTERED_DF['geo_province'] = FILTERED_DF['province'].map(inverse_map).fillna(FILTERED_DF['province'])

#     geo_provinces = [feature['properties']['adm2_en'] for feature in combined_geojson['features']]
#     FILTERED_DF = FILTERED_DF[FILTERED_DF['geo_province'].isin(geo_provinces)]

#     # 4. Plotly Choropleth (Province-level within Regions)
#     map_chart = px.choropleth(
#         FILTERED_DF,
#         geojson=combined_geojson,
#         locations='geo_province',
#         featureidkey='properties.adm2_en',
#         color='counts',
#         hover_name='province',
#         hover_data={'region': True, 'counts': True},
#         color_continuous_scale='Viridis',
#     )

#     map_chart.update_traces(
#         hovertemplate="<b>%{location}</b><br>Region: %{customdata[0]}<br>Total Enrollment: %{z:,}<extra></extra>"
#     )

#     map_chart.update_geos(
#         visible=False,
#         showcountries=False,
#         showcoastlines=False,
#         showland=True,
#         fitbounds="locations",
#         resolution=50,
#         lataxis_range=[4, 22],
#         lonaxis_range=[115, 128],
#     )

#     map_chart.update_layout(
#         margin={"r": 0, "t": 0, "l": 0, "b": 0},
#         paper_bgcolor='black',
#         plot_bgcolor='rgba(0,0,0,0)',
#         coloraxis_showscale=False,
#     )

#     return dcc.Graph(
#         figure=map_chart,
#         style={'width': '100%', 'height': '100%'},
#         config={'responsive': True}
#     )


# #################################################################################



# #################################################################################
# ##  --- CHART: school sectors
# #################################################################################
@callback(
    Output('location_school_sectors', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    sector_enrollment = (
        FILTERED_DATA
        .groupby(['region', 'sector'])['counts']
        .sum()
        .reset_index()
    )

    sector_enrollment = (
        sector_enrollment
        .sort_values(['region', 'counts'], ascending=[True, True])
    )

    region_order = [
        'CAR', 'NCR', 'Region I', 'Region II', 'Region III', 'Region IV-A',
        'Region IV-B', 'Region V', 'Region VI', 'Region VII', 'Region VIII',
        'Region IX', 'Region X', 'Region XI', 'Region XII', 'CARAGA', 'BARMM'
    ]

    sector_enrollment['region'] = pd.Categorical(
        sector_enrollment['region'],
        categories=region_order,
        ordered=True
    )

    sector_order  = ['Public', 'Private', 'SUCs/LUCs', 'PSO']
    sector_colors = {
        'Public':    '#930F22',
        'Private':   '#E11C38',  
        'SUCs/LUCs': '#FF5B72',  
        'PSO':       '#FF899A'   
    }

    sector_enrollment['sector'] = pd.Categorical(
        sector_enrollment['sector'],
        categories=sector_order,
        ordered=True
    )

    sector_chart = px.bar(
        sector_enrollment,
        x='region',
        y='counts',
        color='sector',
        barmode='stack',
        category_orders={
            'region': region_order,
            'sector': sector_order
        },
        color_discrete_map=sector_colors,
        labels={
            'region': ' Region',
            'counts': ' Number of Students',
            'sector': ' School Sector',
        },
    )

    sector_chart.update_layout(
        autosize=True,
        title_font=dict(size=20, family='Inter, sans-serif', color='#3C6382'),
        title_x=0.5,
        font=dict(family='Inter, sans-serif', size=10, color='#04508c'),
        plot_bgcolor='white',
        margin=dict(l=50, r=30, t=70, b=60),
        legend=dict(
            title=None,
            orientation='h',          
            yanchor='top',
            y=1.15,                 
            xanchor='center',
            x=0.5,                         
            font=dict(size=12),
            bgcolor='white',
            bordercolor='red'
        ),

        xaxis=dict(showgrid=False, tickangle=-45),
        yaxis=dict(
            showgrid=False,
            tickformat='.1s',
            tickprefix=''
        ),
        bargap=0.1
    )

    sector_chart.update_traces(
        marker_line_color='#FFFFFF',
        marker_line_width=2
    )

    sector_chart

    return dcc.Graph(figure=sector_chart)

# #################################################################################



# #################################################################################
# ##  --- CHART: school sectors
# #################################################################################






# #################################################################################



# #################################################################################
# ##  --- CHART: Strand preferences per region
# #################################################################################
@callback(
    Output('track-preference-heatmap', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)

    # Normalize and clean data: strip whitespace, convert to lowercase
    FILTERED_DATA['track'] = FILTERED_DATA['track'].astype(str).str.strip().str.lower()
    FILTERED_DATA['strand'] = FILTERED_DATA['strand'].astype(str).str.strip().str.lower()

    # Define invalid placeholder values
    invalid_values = ['__nan__', 'nan']

    # Remove invalid track rows before grouping
    filtered_track_data = FILTERED_DATA[~FILTERED_DATA['track'].isin(invalid_values)]
    track_data = (
        filtered_track_data.groupby(['region', 'track'])['counts'].sum().reset_index()
    )
    track_pivot = track_data.pivot(index='track', columns='region', values='counts').fillna(0)

    # Remove invalid strand rows before grouping
    filtered_strand_data = FILTERED_DATA[~FILTERED_DATA['strand'].isin(invalid_values)]
    strand_data = (
        filtered_strand_data.groupby(['region', 'strand'])['counts'].sum().reset_index()
    )
    strand_pivot = strand_data.pivot(index='strand', columns='region', values='counts').fillna(0)

    # Step 4: Create subplots
    heatmap_fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03
    )

    # Heatmap for Track
    heatmap_fig.add_trace(
        go.Heatmap(
            z=track_pivot.values,
            x=track_pivot.columns.tolist(),
            y=track_pivot.index.tolist(),
            colorscale=[
                "#074889", "#0C6DC1", "#1389F0", "#00CCFF", 
                "#00F2FF", "#89FE2A", "#F9F521", "#FFB700"
            ],
            hovertemplate='Region: %{x}<br>Track: %{y}<br>Enrollees: %{z}',
            # colorbar=dict(title="Students Enrolled"),
            zmin=0,
            # colorbar=dict(title="Students Enrolled")
        ),
        row=1, col=1
    )

    # Heatmap for Strand
    heatmap_fig.add_trace(
        go.Heatmap(
            z=strand_pivot.values,
            x=strand_pivot.columns.tolist(),
            y=strand_pivot.index.tolist(),
            colorscale=[
                "#074889", "#0C6DC1", "#1389F0", "#00CCFF", 
                "#00F2FF", "#89FE2A", "#F9F521", "#FFB700"
            ],
            showscale=False,
            hovertemplate='Region: %{x}<br>Strand: %{y}<br>Enrollees: %{z}',
            zmin=0, # Only show one colorbar
        ),
        row=2, col=1
    )

    # Step 5: Update layout
    heatmap_fig.update_layout(
        height=400,
        width=600,
        font=dict(size=10, color="#04508c"),
        xaxis2=dict(title="Region", tickangle=-45),
        yaxis=dict(title="Track"),
        yaxis2=dict(title="Strand"),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # Step 6: Show the figure
    heatmap_fig

    return dcc.Graph(figure=heatmap_fig)

# #################################################################################



# #################################################################################
# ##  --- INDICATOR: Total number of enrollees
# #################################################################################

@callback(
    Output('raw-total-enrollees', 'children'),
    Output('truncated-total-enrollees', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    raw_total_enrollees = FILTERED_DATA['counts'].sum()
    truncated_total_enrollees = smart_truncate_number(raw_total_enrollees)

    raw_total_enrollees
    truncated_total_enrollees
    
    return f"{raw_total_enrollees:,} enrollees", truncated_total_enrollees

# #################################################################################



# #################################################################################
# ##  --- INDICATOR: Total number of schools
# #################################################################################

@callback(
    Output('raw-total-schools', 'children'),
    Output('truncated-total-schools', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    # Count total number of unique schools
    raw_total_schools = FILTERED_DATA['name'].nunique()
    truncated_total_schools = smart_truncate_number(raw_total_schools)

    raw_total_schools
    truncated_total_schools
    
    return f"{raw_total_schools:,} enrollees", truncated_total_schools

# #################################################################################



# #################################################################################
# ##  --- TABLE: Total number of schools
# #################################################################################

@callback(
    Output('location_highest_lowest_enrollees', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    # Step 1: Group by school and region, summing the counts
    aggregated_df = FILTERED_DATA.groupby(['name', 'region'], as_index=False)['counts'].sum()

    
# --- INSERT THIS to filter out schools with 0 enrollees ---
    aggregated_df = aggregated_df[aggregated_df['counts'] > 0]

    
    # Step 2: Get the school with highest and lowest total enrollees
    max_row = aggregated_df.loc[aggregated_df['counts'].idxmax()]
    min_row = aggregated_df.loc[aggregated_df['counts'].idxmin()]

    # Step 3: Combine them into a new DataFrame for visualization
    highest_lowest2 = pd.DataFrame([max_row, min_row])

    hi_low_fig = go.Figure(data=[go.Table(
        columnorder=[1, 2, 3],
        columnwidth=[80, 40, 50],

    header=dict(
        values=["School Name", "Region", "Total Enrollees"],
        fill_color='#E6F2FB',
        align='left',
        font=dict(family='Inter', color='#04508c', size=12),
        line_color='#B0C4DE',
        height=40  # header height
    ),
    cells=dict(
        values=[
            highest_lowest2['name'].apply(lambda x: f"{x}\n"),
            highest_lowest2['region'],
            highest_lowest2['counts']
        ],
        fill_color=['#FFFFFF', '#F7FAFC'],
        align='left',
        font=dict(family='Inter', color='#3C6382', size=12),
        line_color='#D3D3D3',
        height=90  # fixed cell height
    )
)])

    hi_low_fig.update_layout(
        autosize=True,
        
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    hi_low_fig
    
    return dcc.Graph(figure=hi_low_fig)

# #################################################################################