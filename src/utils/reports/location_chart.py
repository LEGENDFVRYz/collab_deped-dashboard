from enum import auto
from turtle import title, width
from unicodedata import category
import numpy as np
import pandas as pd
import dash
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, callback, Output, Input, State, Patch
from plotly.subplots import make_subplots 

import json
from pathlib import Path
import re, os, sys
import plotly.express as px
from geojson_rewind import rewind
import pandas as pd
import plotly.io as pio 
from rapidfuzz import process, fuzz
import unicodedata
import re
    
# important part
from src.data import enrollment_db_engine, smart_filter

# Extra Utilities
from src.utils.extras_utils import smart_truncate_number

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import project_root


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
    Output('edrg-graph-title', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    FILTERED_DATA = FILTERED_DATA[['beis_id', 'brgy', 'municipality', 'district', 'division', 'province', 'region', 'counts', 'gender']]
    # print("triggered dispilinr")
    
    ## LOCATION SCOPE
    locs = ['beis_id', 'brgy', 'municipality', 'district', 'division', 'province', 'region']
    tag = "default"
    min_loc = 6

    for i, loc in enumerate(locs[1:]):
        if loc in data:
            min_loc = i
            break

    loc_scope = locs[min_loc]
    
    
    ## TITLE
    # try:
    #     values = data.get(locs[min_loc + 1], [])
    #     if len(values) > 1:
    #         tag = ["Distribution Breakdown for the ", html.Span(["Chosen Location"], className="lfury-highlight"),]
    #     else:
    #         tag = ["Distribution Breakdown by ", html.Span([f"{loc_scope.capitalize()} of {values[0]}"], className="lfury-highlight")]
    # except (IndexError, KeyError, TypeError):
    #     tag = ["Distribution Breakdown by ", html.Span([f"{loc_scope.capitalize()} of {values[0]}"], className="lfury-highlight")]
    
    try:
        values = data.get(locs[min_loc + 1], [])
        if len(values) > 1:
            tag = [
                "Distribution Breakdown for the ",
                html.Span([" Chosen Location "], className="lfury-highlight"),
            ]
        else:
            tag = [
                "Distribution Breakdown by ",
                html.Span([f" {loc_scope.capitalize()} of {values[0]} "], className="lfury-highlight"),
            ]
    except (IndexError, KeyError, TypeError):
        # Fall back to a default string or empty value
        tag = [
            "Distribution Breakdown by ",
            html.Span([f" {loc_scope.capitalize()} of Philippines "], className="lfury-highlight"),
        ]
    
    # Step 1: Group by region and gender
    total_counts = FILTERED_DATA.groupby(loc_scope, observed=True)['counts'].sum().reset_index()
    total_counts = total_counts.sort_values(by='counts', ascending=True)

    # Step 2: Group by region and gender, and calculate counts
    gender_region = FILTERED_DATA.groupby([loc_scope, 'gender'], observed=True)['counts'].sum().reset_index()

    # Step 3: Ensure that the 'loc_scope' in gender_region has the same ordering as in total_counts
    gender_region[loc_scope] = pd.Categorical(
        gender_region[loc_scope], 
        categories=total_counts[loc_scope].tolist(), 
        ordered=True
    )
    
    # Step 4: Optionally, sort gender_region based on the ordered loc_scope categories
    gender_region = gender_region.sort_values(by=loc_scope)
    
    # Step 2: Define brand colors
    brand_colors = {
        'M': '#5DB7FF',
        # 'F': '#FF5B72',
        'F': '#e11c38',
    }

    # Add dynamic text labels inside the bar segments
    gender_region['text_label'] = gender_region['counts'].apply(smart_truncate_number)
    totals = gender_region.groupby(loc_scope)['counts'].sum().reset_index()
    totals['text'] = totals['counts'].apply(smart_truncate_number)
    
    
    gender_region_fig = px.bar(
        gender_region,
        x='counts',
        y=loc_scope,
        color='gender',
        orientation='h',
        barmode='stack',
        text='text_label',  # <- Set dynamic text
        labels={
            'counts': 'Number of Enrollees',
            'gender': 'Gender'
        },
        color_discrete_map=brand_colors
    )
    
    gender_region_fig.update_traces(
        textposition='inside',
        insidetextanchor='end',
        textfont=dict(
            color='white',
            family='Inter Bold',
            size=12
        ),
        cliponaxis=False
    )

    
    # # Step 3: Create the stacked bar chart
    # gender_region_fig = px.bar(
    #     gender_region,
    #     x='counts',
    #     y=loc_scope,
    #     color='gender',
    #     orientation='h',
    #     barmode='stack',
    #     labels={
    #         'counts': 'Number of Enrollees',
    #         # Removed 'region' label to prevent it from auto-setting y-axis title
    #         'gender': 'Gender'
    #     },
    #     color_discrete_map=brand_colors
    # )
    
    # # Step 4: Calculate total per region for annotations
    # region_totals = gender_region.groupby(loc_scope, observed=True)['counts'].sum().reset_index()

    # # Step 5: Add truncated total annotations
    # for _, row in region_totals.iterrows():
    #     short_text = smart_truncate_number(row['counts'])  # Your truncation logic
    #     gender_region_fig.add_annotation(
    #         x=row['counts'] + 1,
    #         y=row[loc_scope],
    #         text=short_text,
    #         hovertext=str(row['counts']),
    #         showarrow=False,
    #         font=dict(color="#667889", family='Inter Bold'),
    #         xanchor="left",
    #         yanchor="middle",
    #     )

    # Step 6: Customize layout (explicitly clear y-axis title)
    gender_region_fig.update_layout(
        yaxis=dict(
            automargin=True,
            title=None,
            ticksuffix="   "
        ),
        xaxis=dict(
            showline=True,
            linecolor='black',   # or any visible color like '#667889'
            linewidth=1          # optional, default is 1
        ),
        legend=dict(
            orientation="h",       # horizontal layout
            yanchor="top",         # anchor from top of legend box
            y=-0.15,                # position legend below x-axis label
            xanchor="center",      # center the legend horizontally
            x=0.5,                 # center relative to plot width
        ),
        xaxis_title="Number of Students",
        yaxis_title="",  # Remove the default "Region" title
        legend_title="Gender",
        # tickpadding=10,
        font=dict(color="#667889", family='Inter'),
        margin=dict(l=0, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        barcornerradius=6,
    )

    return dcc.Graph(figure=gender_region_fig), tag

#################################################################################




# #################################################################################
# ##  --- CHART: enrollment density (students per location)
# #################################################################################

@callback(
    Output('location_choropleth-map', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
)
def update_municipality_choropleth_map(trigger, data):
    # 1. Filter the DataFrame
    FILTERED_DF = smart_filter(data, enrollment_db_engine)
    FILTERED_DF = FILTERED_DF.groupby('municipality', as_index=False)['counts'].sum()

    unique_municipalities = FILTERED_DF['municipality'].drop_duplicates().tolist()
    print("Municipalities in DataFrame:", len(unique_municipalities))
    for municipality in sorted(unique_municipalities):
        print(municipality)

    # ----------------------------------------------------
    # 2. Load and Combine All GeoJSON Files
    # ----------------------------------------------------

    geojson_folder = "/Users/marke/Downloads/muni/"
    geojson_files = [
        "ABRA.geojson", "AGUSAN DEL NORTE.geojson", "AGUSAN DEL SUR.geojson", "AKLAN.geojson", "ALBAY.geojson",
        "ANTIQUE.geojson", "APAYAO.geojson", "AURORA.geojson", "BASILAN.geojson", "BATAAN.geojson",
        "BATANES.geojson", "BATANGAS.geojson", "BENGUET.geojson", "BILIRAN.geojson", "BOHOL.geojson",
        "BUKIDNON.geojson", "BULACAN.geojson", "CAGAYAN.geojson", "CAMARINES NORTE.geojson", "CAMARINES SUR.geojson",
        "CAMIGUIN.geojson", "CAPIZ.geojson", "CATANDUANES.geojson", "CAVITE.geojson", "CEBU.geojson",
        "CITY OF ISABELA.geojson", "COMPOSTELA VALLEY.geojson", "DAVAO DEL NORTE.geojson", "DAVAO DEL SUR.geojson",
        "DAVAO ORIENTAL.geojson", "DINAGAT ISLANDS.geojson", "EASTERN SAMAR.geojson", "FIRST DISTRICT.geojson",
        "FOURTH DISTRICT.geojson", "GUIMARAS.geojson", "IFUGAO.geojson", "ILOCOS NORTE.geojson", "ILOCOS SUR.geojson",
        "ILOILO.geojson", "ISABELA.geojson", "KALINGA.geojson", "LA UNION.geojson", "LAGUNA.geojson",
        "LANAO DEL NORTE.geojson", "LANAO DEL SUR.geojson", "LEYTE.geojson", "MAGUINDANAO.geojson",
        "MARINDUQUE.geojson", "MASBATE.geojson", "MISAMIS OCCIDENTAL.geojson", "MISAMIS ORIENTAL.geojson",
        "MOUNTAIN PROVINCE.geojson", "NEGROS OCCIDENTAL.geojson", "NEGROS ORIENTAL.geojson", "NORTH COTABATO.geojson",
        "NORTHERN SAMAR.geojson", "NUEVA ECIJA.geojson", "NUEVA VIZCAYA.geojson", "OCCIDENTAL MINDORO.geojson",
        "ORIENTAL MINDORO.geojson", "PALAWAN.geojson", "PAMPANGA.geojson", "PANGASINAN.geojson", "QUEZON.geojson",
        "QUIRINO.geojson", "RIZAL.geojson", "ROMBLON.geojson", "SAMAR (WESTERN SAMAR).geojson", "SARANGANI.geojson",
        "SECOND DISTRICT.geojson", "SIQUIJOR.geojson", "SORSOGON.geojson", "SOUTH COTABATO.geojson",
        "SOUTHERN LEYTE.geojson", "SULTAN KUDARAT.geojson", "SULU.geojson", "SURIGAO DEL NORTE.geojson",
        "SURIGAO DEL SUR.geojson", "TARLAC.geojson", "TAWI-TAWI.geojson", "THIRD DISTRICT.geojson",
        "ZAMBALES.geojson", "ZAMBOANGA DEL NORTE.geojson", "ZAMBOANGA DEL SUR.geojson", "ZAMBOANGA SIBUGAY.geojson"
    ]

    all_features = []

    for filename in geojson_files:
        filepath = os.path.join(geojson_folder, filename)
        with open(filepath) as f:
            geo = json.load(f)

            if geo.get("type") == "FeatureCollection":
                all_features.extend(geo["features"])
            elif geo.get("type") == "Feature":
                all_features.append(geo)
            elif geo.get("type") == "GeometryCollection":
                for geometry in geo.get("geometries", []):
                    feature = {
                        "type": "Feature",
                        "geometry": geometry,
                        "properties": {}
                    }
                    all_features.append(feature)
            else:
                print(f"Unexpected GeoJSON type in {filename} → {geo.get('type')}")

    combined_geojson = {
        "type": "FeatureCollection",
        "features": all_features
    }

    geo_municipalities = [
        feature['properties']['MUNICIPALI']
        for feature in combined_geojson['features']
        if feature['properties'].get('MUNICIPALI')
    ]

    print("Municipalities in GeoJSON:", len(set(geo_municipalities)))
    print("Sample GeoJSON names:", sorted(set(geo_municipalities))[:10])

    # ----------------------------------------------------
    # 3. Normalize Municipality Names
    # ----------------------------------------------------

    def normalize_municipality(name):
        if not name:
            return ""
        name = re.sub(r"\s*\(.*?\)", "", name).strip()
        if name.lower().startswith("city of "):
            name = name[8:] + " City"
        elif name.lower().startswith("city "):
            name = name[5:] + " City"
        elif name.lower().startswith("cityof "):
            name = name[7:] + " City"

        name = unicodedata.normalize('NFKD', name)
        name = ''.join(c for c in name if not unicodedata.combining(c))
        return name.title()

    df_normalized = [normalize_municipality(m) for m in unique_municipalities]
    geo_normalized = [normalize_municipality(m) for m in geo_municipalities if m]

    df_set = set(df_normalized)
    geo_set = set(geo_normalized)

    # ----------------------------------------------------
    # 4. Matching Municipality Names
    # ----------------------------------------------------

    matches = sorted(df_set & geo_set)

    in_df_not_in_geo = sorted(df_set - geo_set)

    fuzzy_matches = []
    for name in in_df_not_in_geo:
        best_match, score, _ = process.extractOne(name, geo_set, scorer=fuzz.ratio)
        if score >= 70:
            fuzzy_matches.append((name, best_match, score))

    print("\n🔍 Fuzzy Matches (Score ≥ 85):")
    for original, matched, score in fuzzy_matches:
        print(f" 🔁 {original} ↔ {matched} ({score}%)")

    fuzzy_matched_names = {name for name, _, _ in fuzzy_matches}
    remaining_unmatched = sorted(df_set - geo_set - fuzzy_matched_names)

    print(f"\n❌ Still Unmatched ({len(remaining_unmatched)}):")
    for m in remaining_unmatched:
        print(" ❌", m)

    # ----------------------------------------------------
    # 5. Filter DataFrame to Matching Municipalities Only
    # ----------------------------------------------------
    FILTERED_DF['normalized_municipality'] = FILTERED_DF['municipality'].apply(normalize_municipality)
    
    geo_municipalities_normalized = [normalize_municipality(m) for m in geo_municipalities if m]

    FILTERED_DF = FILTERED_DF[
        FILTERED_DF['normalized_municipality'].isin(geo_municipalities_normalized)
    ]
    
    # Create a dictionary for fuzzy matched names
    fuzzy_match_dict = {original: matched for original, matched, _ in fuzzy_matches}

    # Update the `FILTERED_DF` with the fuzzy matched names
    FILTERED_DF['final_municipality'] = FILTERED_DF['normalized_municipality'].apply(
        lambda name: fuzzy_match_dict.get(name, name)  # Use fuzzy match if available
    )

    # Update GeoJSON municipality names to match final municipality names
    geo_municipalities_final = [fuzzy_match_dict.get(name, name) for name in geo_municipalities_normalized]

    # Filter DataFrame to final municipalities
    FILTERED_DF = FILTERED_DF[FILTERED_DF['final_municipality'].isin(geo_municipalities_final)]
    FILTERED_DF['final_municipality'] = FILTERED_DF['final_municipality'].str.upper()
    # FILTERED_DF['normalized_municipality'] = FILTERED_DF['normalized_municipality'].str.upper()

    print(set(FILTERED_DF['final_municipality']) - {
        feature['properties']['MUNICIPALI'] for feature in combined_geojson['features']
    })

    
    # ----------------------------------------------------
    # Plot Choropleth with the final municipalities
    # ----------------------------------------------------

    map_chart = px.choropleth(
        FILTERED_DF,
        geojson=combined_geojson,
        locations='municipality',
        featureidkey='properties.MUNICIPALI',
        color='counts',
        hover_name='final_municipality',
        hover_data=['counts'],
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
    


# @callback(
#     Output('location_choropleth-map', 'children'),
#     Input('chart-trigger', 'data'),
#     State('filtered_values', 'data'),
# )
# def update_province_choropleth_map(trigger, data):
#     FILTERED_DF = smart_filter(data, enrollment_db_engine)
    

#     FILTERED_DF = FILTERED_DF.groupby('province', as_index=False)['counts'].sum()

#     unique_provinces = FILTERED_DF['province'].drop_duplicates().tolist()
#     for province in unique_provinces:
#         print(province)    
        
#         # Print for debug
#     unique_provinces = FILTERED_DF['province'].drop_duplicates().tolist()
#     print("Provinces in DataFrame:", len(unique_provinces))
#     for province in sorted(unique_provinces):
#         print(province)

#     # Folder where all region-wise GeoJSON files are stored
#     geojson_folder = "/Users/marke/Downloads/low/"
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

#     # Combine all province GeoJSONs into one FeatureCollection
#     all_features = []
#     for filename in geojson_files:
#         filepath = os.path.join(geojson_folder, filename + ".json")
#         with open(filepath) as f:
#             geo = json.load(f)
#             geo = rewind(geo, rfc7946=False)  # Ensure proper winding
#             all_features.extend(geo['features'])

#     combined_geojson = {
#         "type": "FeatureCollection",
#         "features": all_features
#     }

#     # Extract province names from GeoJSON
#     geo_provinces = [feature['properties']['adm2_en'] for feature in combined_geojson['features']]
#     print("Provinces in GeoJSON:", len(set(geo_provinces)))
#     print("Provinces in DataFrame:", set(FILTERED_DF['province']))


#     # Normalize casing and whitespace
#     FILTERED_DF['normalized_province'] = FILTERED_DF['province'].str.strip().str.title()
#     geo_provinces_normalized = [prov.strip().title() for prov in geo_provinces if prov]


#     # Keep only matching provinces
#     FILTERED_DF = FILTERED_DF[FILTERED_DF['normalized_province'].isin(geo_provinces_normalized)]
    
#     # 4. Plotly Choropleth
#     map_chart = px.choropleth(
#         FILTERED_DF,
#         geojson=combined_geojson,
#         locations='normalized_province',
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

    locs = ['brgy', 'municipality', 'district', 'division', 'province', 'region']

    min_loc = 5

    for i, loc in enumerate(locs[1:]):
        if loc in data:
            min_loc = i
            break

    loc_scope = locs[min_loc]
    
    
    
    sector_enrollment = (
        FILTERED_DATA
        .groupby([loc_scope, 'sector'], observed=True)['counts']
        .sum()
        .reset_index()
    )

    sector_enrollment = (
        sector_enrollment
        .sort_values([loc_scope, 'counts'], ascending=[True, True])
    )

    # region_order = [
    #     'CAR', 'NCR', 'Region I', 'Region II', 'Region III', 'Region IV-A',
    #     'Region IV-B', 'Region V', 'Region VI', 'Region VII', 'Region VIII',
    #     'Region IX', 'Region X', 'Region XI', 'Region XII', 'CARAGA', 'BARMM'
    # ]

    # sector_enrollment['region'] = pd.Categorical(
    #     sector_enrollment['region'],
    #     categories=region_order,
    #     ordered=True
    # )

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
        x=loc_scope,
        y='counts',
        color='sector',
        barmode='stack',
        category_orders={
            # 'region': region_order,
            'sector': sector_order
        },
        color_discrete_map=sector_colors,
        labels={
            loc_scope: loc_scope.capitalize(),
            'counts': 'Number of Students',
            'sector': 'School Sector',
        },
    )

    sector_chart.update_layout(
        autosize=True,
        title=None,  # Remove the main chart title
        font=dict(family='Inter, sans-serif', size=14, color='#3C6382'),
        plot_bgcolor='rgba(255,255,255,0.5)',
        margin=dict(l=50, r=30, t=70, b=60),
        legend=dict(
            title=None,
            orientation='h',
            yanchor='bottom',
            y=-0.9,
            xanchor='center',
            x=0.5,
            font=dict(size=12),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        ),
        xaxis=dict(
            title=None,         # Remove x-axis title
            showgrid=False,
            tickangle=-45,
            tickfont=dict(size=10, color="#667889"),
        ),
        yaxis=dict(
            title=None,         # Remove y-axis title
            showgrid=False,
            tickformat='.1s',
            tickprefix='',
            tickfont=dict(size=10, color="#667889"),
        ),
        bargap=0.1
    )

    # sector_chart.update_traces(
    #     marker_line_color='#FFFFFF',
    #     marker_line_width=2
    # )

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
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    locs = ['brgy', 'municipality', 'district', 'division', 'province', 'region']

    min_loc = 5

    for i, loc in enumerate(locs[1:]):
        if loc in data:
            min_loc = i
            break

    loc_scope = locs[min_loc]
    
    # Cleaning
    clean_df = FILTERED_DATA[FILTERED_DATA['grade'].isin(['G11', 'G12'])].copy()
    # clean_df['track'] = clean_df['track'].cat.remove_unused_categories()
    clean_df['track'] = clean_df['track'].cat.remove_unused_categories()
    
    # Step 2: Group and SUM the 'counts' for track-level heatmap
    track_data = clean_df.groupby([loc_scope, 'track'], observed=True)['counts'].sum().reset_index()
    track_pivot = track_data.pivot(index='track', columns=loc_scope, values='counts').fillna(0)

    # Step 3: Group and SUM the 'counts' for strand-level heatmap
    clean_df = clean_df[clean_df['strand'] != '__NaN__']
    clean_df['strand'] = clean_df['strand'].cat.remove_unused_categories()
    strand_data = clean_df.groupby([loc_scope, 'strand'], observed=True)['counts'].sum().reset_index()
    strand_pivot = strand_data.pivot(index='strand', columns=loc_scope, values='counts').fillna(0)
    
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
            name='',  # <--- add this line
            hovertemplate='Region: %{x}<br>Track: %{y}<br>Enrollees: %{z}',
            colorbar=dict(
                # title="Students Enrolled"
                len=1.06
                ),
            zmin=0,
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
            name='',  # <--- add this line
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
        title_text=None,
        xaxis2=dict(title=None, tickangle=-45, tickfont=dict(size=10, color="#9DADBD")),
        yaxis=dict(title=None, tickfont=dict(size=10, color="#667889")),
        yaxis2=dict(title=None,tickfont=dict(size=10, color="#667889")),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return dcc.Graph(figure=heatmap_fig)

# #################################################################################



# #################################################################################
# ##  --- INDICATOR: Total number of enrollees
# #################################################################################

@callback(
    Output('raw-average-enrollees', 'children'),
    Output('truncated-average-enrollees', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)

    locs = ['brgy', 'municipality', 'district', 'division', 'province', 'region']

    min_loc = 5

    for i, loc in enumerate(locs[1:]):
        if loc in data:
            min_loc = i
            break

    loc_scope = locs[min_loc]
    
    FILTERED_DATA = FILTERED_DATA[[loc_scope, 'counts']]
    df_grouped = FILTERED_DATA.groupby(loc_scope, as_index=False, observed=True)['counts'].sum()

    # Median enrollees per school
    median_enrollees_per_school = int(df_grouped['counts'].mean())
    
    truncated_total_enrollees = smart_truncate_number(median_enrollees_per_school)

    return f"{median_enrollees_per_school:,} enrollees", truncated_total_enrollees




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

    # # get the median
    # median_enrolless = FILTERED_DATA['counts'].median()
    
    # # Filter and compute ratio of enrollees below the median
    # below_median_sum = FILTERED_DATA[FILTERED_DATA['counts'] < median_enrolless]['counts'].sum()

    # # Ratio of enrollees below 50%
    # ratio_below_50 = below_median_sum / raw_total_enrollees if raw_total_enrollees > 0 else 0
        
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
    
    return f"{raw_total_schools:,} schools", truncated_total_schools

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
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)

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
        # autosize=True, 
        height=220,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    return dcc.Graph(
        figure=hi_low_fig,
        config={
            "responsive": True,
            # "staticPlot": True  # disables zoom, pan, hover, etc.
        },
        style={
            "width": "100%",
            # "height": "200px",     # fixed height to prevent overflow
            # "overflow": "hidden"   # ensure no scroll
        }
    )

# #################################################################################


@callback(
    Output('enrollment-by-years', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)
    
    df = FILTERED_DATA[['brgy', 'municipality', 'district', 'division', 'province', 'region', 'counts', 'year']]
    
    locs = ['brgy', 'municipality', 'district', 'division', 'province', 'region']
    min_loc = 5

    for i, loc in enumerate(locs[1:]):
        if loc in data:
            min_loc = i
            break

    loc_scope = locs[min_loc]

    df['year'] = df['year'].astype(str)
    df_grouped = df.groupby([loc_scope, 'year'], as_index=False)['counts'].sum()

    sorted_regions = sorted(df_grouped[loc_scope].unique())
    df_grouped[loc_scope] = pd.Categorical(df_grouped[loc_scope], categories=sorted_regions, ordered=True)
    df_grouped = df_grouped.sort_values(by=[loc_scope, 'year'])

    changes_chart = px.line(
        df_grouped,
        x='year',
        y='counts',
        color=loc_scope,
        markers=True
    )

    changes_chart.update_layout(
        title=None,
        xaxis_title="Year",
        yaxis_title=None,
        xaxis=dict(type='category'),
        margin=dict(t=20, b=20),
    )

    return dcc.Graph(
        figure=changes_chart,
        config={"responsive": True},
        style={"width": "100%", "marginBottom": "10px"}
    )


@callback(
    Output('total-enrollment-by-year', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)
    
    df = FILTERED_DATA[['region', 'counts', 'year']]
    national_enrollment = df.groupby('year', as_index=False)['counts'].sum()

    enrollment_bar = px.bar(
        national_enrollment,
        x='year',
        y='counts',
    )

    enrollment_bar.update_layout(
        title=None,
        xaxis_title="Academic Year",
        yaxis_title=None,
        bargap=0.2,
        xaxis=dict(type='category'),
        margin=dict(t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return dcc.Graph(
        figure=enrollment_bar,
        config={"responsive": True},
        style={"width": "100%"}
    )





@callback(
    Output('highest-avg-enroll', 'children'),
    Output('year-text', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)
    
    # Extract required columns
    FILTERED_DF = FILTERED_DATA[['region', 'year', 'counts']]

    # Aggregate by year
    yearly_counts = FILTERED_DF.groupby('year')['counts'].sum()

    # Get highest year and value
    highest_year = yearly_counts.idxmax()
    highest_value = yearly_counts.max()

    # Optional: truncate number if needed
    truncated_highest_value = smart_truncate_number(highest_value)

    # Optional: print or return
    return f"{truncated_highest_value} Students", f"Academic Year {highest_year} - {highest_year+1}"




@callback(
    Output('high-avg-enroll', 'children'),
    Output('low-avg-enroll', 'children'),
    Output('high-tag-loc', 'children'),
    Output('low-tag-loc', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)
    
    # Extract required columns
    FILTERED_DF = FILTERED_DATA[['region', 'year', 'counts']]

    # Group by region and year, then compute total enrollments per year per region
    region_yearly_counts = FILTERED_DF.groupby(['region', 'year'])['counts'].sum().reset_index()

    # Now compute the average enrollment over the years for each region
    region_avg_enrollment = region_yearly_counts.groupby('region')['counts'].mean()

    # Find region with highest and lowest average enrollment
    highest_avg_region = region_avg_enrollment.idxmax()
    highest_avg_value = region_avg_enrollment.max()

    lowest_avg_region = region_avg_enrollment.idxmin()
    lowest_avg_value = region_avg_enrollment.min()

    # Truncate values if needed
    truncated_highest_avg = smart_truncate_number(highest_avg_value)
    truncated_lowest_avg = smart_truncate_number(lowest_avg_value)

    # Output (or return these values)
    return f"{truncated_highest_avg}", f"{truncated_lowest_avg}", f"{highest_avg_region}", f"{lowest_avg_region}"




@callback(
    Output('cloroplet', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DF = smart_filter(data, enrollment_db_engine)
    
    # Extract required columns
    # FILTERED_DF = FILTERED_DATA[['region', 'year', 'counts']]

    
    # FILTERED_DF = auto_extract(['province', 'counts'], is_specific=False)
    FILTERED_DF = FILTERED_DF.groupby('province', as_index=False)['counts'].sum()
        
        # Print for debug
    unique_provinces = FILTERED_DF['province'].drop_duplicates().tolist()
    print("Provinces in DataFrame:", len(unique_provinces))
    for province in sorted(unique_provinces):
        print(province)

    # Folder where all region-wise GeoJSON files are stored
    geojson_folder = project_root / "src/assets/_geojson/province"
    
    geojson_files = [
        "provinces-region-ph010000000.0.001.json",
        "provinces-region-ph020000000.0.001.json",
        "provinces-region-ph030000000.0.001.json",
        "provinces-region-ph040000000.0.001.json",
        "provinces-region-ph050000000.0.001.json",
        "provinces-region-ph060000000.0.001.json",
        "provinces-region-ph070000000.0.001.json",
        "provinces-region-ph080000000.0.001.json",
        "provinces-region-ph090000000.0.001.json",
        "provinces-region-ph100000000.0.001.json",
        "provinces-region-ph110000000.0.001.json",
        "provinces-region-ph120000000.0.001.json",
        "provinces-region-ph130000000.0.001.json",
        "provinces-region-ph140000000.0.001.json",
        "provinces-region-ph150000000.0.001.json",
        "provinces-region-ph160000000.0.001.json",
        "provinces-region-ph170000000.0.001.json",
        "provinces-region-ph180000000.0.001.json",

    ]

    # Combine all province GeoJSONs into one FeatureCollection
    all_features = []
    for filename in geojson_files:
        filepath = os.path.join(geojson_folder, filename)
        with open(filepath) as f:
            geo = json.load(f)
            geo = rewind(geo, rfc7946=False)
            all_features.extend(geo['features'])

    combined_geojson = {
        "type": "FeatureCollection",
        "features": all_features
    }

    # Extract province names from GeoJSON
    geo_provinces = [feature['properties']['ADM2_EN'] for feature in combined_geojson['features']]
    print("Provinces in GeoJSON:", len(set(geo_provinces)))
    print("Provinces in DataFrame:", len(set(FILTERED_DF['province'])))

    # Normalize for comparison
    df_norm = {name.strip().title() for name in unique_provinces}
    geo_norm = {name.strip().title() for name in geo_provinces}

    # Find unmatched from DataFrame
    unmatched = sorted(df_norm - geo_norm)

    print("\n❌ Unmatched provinces from DataFrame not found in GeoJSON:")
    for prov in unmatched:
        print(f"- {prov}")

    
    def normalize_province(name):
        if not name:
            return ""
        name = name.strip()

        # Common fixes
        name = name.replace("Ncr", "NCR")
        name = re.sub(r"(?i)^city of\s+", "", name)
        # name = re.sub(r",\s*NCR.*", "NCR", name)  # e.g., "Manila, NCR, First District" → "Manila NCR"
        name = unicodedata.normalize('NFKD', name)
        name = ''.join(c for c in name if not unicodedata.combining(c))
        return name.title()

    # Normalize both lists
    df_normalized = [normalize_province(name) for name in unique_provinces]
    geo_normalized = [normalize_province(name) for name in geo_provinces]

    # Convert to sets
    df_set = set(df_normalized)
    geo_set = set(geo_normalized)

    # Exact matches
    matched = sorted(df_set & geo_set)
    unmatched = sorted(df_set - geo_set)

    print("\n✅ Matched provinces:")
    for prov in matched:
        print(f"  ✅ {prov}")

    # Fuzzy match for unmatched
    fuzzy_matches = []
    for name in unmatched:
        best_match, score, _ = process.extractOne(name, geo_set, scorer=fuzz.ratio)
        if score >= 50:
            fuzzy_matches.append((name, best_match, score))

    # Output fuzzy matches
    print("\n🔁 Fuzzy matched provinces:")
    for original, matched, score in fuzzy_matches:
        print(f"  🔁 {original} ↔ {matched} ({score}%)")

    # Remaining unmatched after fuzzy match
    fuzzy_matched_names = {original for original, _, _ in fuzzy_matches}
    still_unmatched = sorted(set(unmatched) - fuzzy_matched_names)

    print("\n❌ Still unmatched provinces:")
    for prov in still_unmatched:
        print(f"  ❌ {prov}")
        
        
        # Step: Create mapping from fuzzy matches
    fuzzy_match_dict_prov = {original: matched for original, matched, _ in fuzzy_matches}

    # Step: Normalize and apply fuzzy match to province column in DF
    FILTERED_DF['normalized_province'] = FILTERED_DF['province'].apply(normalize_province)

    FILTERED_DF['final_province'] = FILTERED_DF['normalized_province'].apply(
        lambda x: fuzzy_match_dict_prov.get(x, x)  # Use fuzzy match if exists, else use normalized
    )

    # Step: Normalize GeoJSON province names (no uppercasing)
    geo_provinces_normalized_final = [normalize_province(p) for p in geo_provinces if p]

    # Step: Filter DataFrame to matching provinces
    FILTERED_DF = FILTERED_DF[
        FILTERED_DF['final_province'].isin(geo_provinces_normalized_final)
    ]

    # Step: Print unmatched final provinces (optional debug)
    unmatched_final = set(FILTERED_DF['final_province']) - set(geo_provinces_normalized_final)
    if unmatched_final:
        print("\n⚠️ Unmatched final provinces still not in GeoJSON:")
        for p in sorted(unmatched_final):
            print("  ❌", p)


    # 4. Plotly Choropleth
    map_chart = px.choropleth(
        FILTERED_DF,
        geojson=combined_geojson,
        locations='final_province',
        featureidkey='properties.ADM2_EN',
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
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False,
        height=900,
        width=700,
        # dragmode=False,
    )
    
    # map_chart.show(renderer="browser")
    return dcc.Graph(
        figure=map_chart,
        config={"responsive": True},
        # style={"width": "100%"}
    )