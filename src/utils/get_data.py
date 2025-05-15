from tkinter import font
from turtle import title
from numpy import append
from sqlalchemy import create_engine
import pandas as pd
import os, sys

import json
import os
import plotly.express as px
from geojson_rewind import rewind
import pandas as pd
import plotly.io as pio 
from rapidfuzz import process, fuzz
import unicodedata
import re


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from config import project_root


"""
    AUTOMATICALLY JOINED THE TABLE FOR QUERYING PURPOSES
"""


def auto_extract(requested_columns:list, is_specific=True, distinct=False) -> pd.DataFrame:
    try:
        engine = create_engine(f"sqlite:///{project_root / 'database/processed/sql/enrollment_data.db'}", echo=False)
        
        GRADE_LIST = ['ES_enroll', 'JHS_enroll', 'SHS_enroll']
        grade_cols = ['es_grade', 'jhs_grade', 'shs_grade', 'gender']
        is_distinct = ''
        
        data_record = {
            'enrollment': ['gender'],
            'ES_enroll':  ['es_grade'], 
            'JHS_enroll': ['jhs_grade'], 
            'SHS_enroll': ['shs_grade', 'strand', 'track'],
            'sch_info':   ['beis_id', 'name', 'sector', 'sub_class', 'type', 'mod_coc', 'street'],
            'sch_local':  ['municipality', 'legis_district', 'brgy'],
            'sch_region': ['region', 'division', 'province']
        }
        root_table = {
            'enrollment': ['enrollment', 'ES_enroll', 'JHS_enroll', 'SHS_enroll'],
            'sch_info':   ['sch_info', 'sch_region', 'sch_local']
        }
        data_keys = {
            'sch_local':  'local_id',
            'sch_region': 'region_id',
        }
        
        
        if 'counts' in requested_columns and all(col not in requested_columns for col in grade_cols[:3]):   # automatic all grade levels
            requested_columns += grade_cols[:3]
            
        if distinct:
            is_distinct = 'DISTINCT'
        
        # Determine the related tables to be merge based on requested columns
        related_table = []
        for table_name, ref_columns in data_record.items():
            if (set(requested_columns) & set(ref_columns)):
                related_table.append(table_name)
        
        
        # Determine the root table
        roots = []
        for root, ref_tables in root_table.items():
            if (set(related_table) & set(ref_tables)):
                roots.append(root)
        related_table = [t for t in related_table if t not in roots] # remove the root table in related
        
        
        ###### HANDLES THE JOINING THE GRADE DATA ########
        related_sch_table = [x for x in related_table if x not in GRADE_LIST]
        related_grade_table = [x for x in related_table if x in GRADE_LIST]
        
        # print(related_table)
        # print(related_grade_table)
        # print(roots)
        
        
        ###### HANDLES THE JOINING OF SCHOOL INFORMATION ########
        if related_sch_table:
            left_join = "\n".join([
                f"LEFT JOIN {t} USING ({data_keys[t]})"
                for t in related_sch_table
            ])
        else:
            left_join = ''
        
        ###### HANDLES THE CASES IF TWO ROOTS ONLY ########
        if set(roots) == set(["enrollment", "sch_info"]):
            roots = [
                "(SELECT * FROM enrollment LEFT JOIN sch_info USING (beis_id))"
            ]
        
        
        ### -- Grade Query
        all_g_query = []
        if len(related_grade_table) == 1 and related_grade_table[0] == 'SHS_enroll':
            ## If SHS only is selected
            all_g_query.append(f"""
                SELECT * FROM enrollment
                LEFT JOIN SHS_enroll USING (enroll_id)
            """)
        elif related_grade_table:
            ## multiple grade is selected
            for grade in related_grade_table:
                if grade == 'SHS_enroll':
                    cols = 'enroll_id,beis_id,gender,grade,counts,year'
                else:
                    cols = '*'
                    
                g_query = f"""
                SELECT {cols} FROM enrollment
                LEFT JOIN {grade} USING (enroll_id)
                """
                all_g_query.append(g_query)
                
        
        ### -- School Info Query
        for id in grade_cols:
            if id in requested_columns: requested_columns.append('grade'); break
        target_cols = [x for x in requested_columns if x not in grade_cols]
        
        sch_query = lambda x: f"""
            SELECT {is_distinct} {x}
            FROM {roots[0]}
            {
                left_join
            }
        """
        
        ### main query
        # print(">>>", ', '.join(target_cols))
        if len(all_g_query) == 0:
            main_query = sch_query(', '.join(target_cols) if is_specific else '*')
        else:
            grouped_grade = '\nUNION ALL\n'.join(all_g_query)
            main_query = f"""
                SELECT {is_distinct} {', '.join(target_cols) if is_specific else '*'} 
                FROM ({sch_query('*')})
                LEFT JOIN (
                    {grouped_grade}
                ) USING (enroll_id, beis_id, gender)
                WHERE grade IS NOT NULL
            """
        # print(main_query)
        
        dataframe = pd.read_sql_query(main_query, con=engine)
        return dataframe
        
    except Exception as e:
        print(f'error: SQL QUERY FAILED')
        
    
if __name__ == '__main__':
    df = auto_extract(['province', 'counts'], is_specific=False)
    df
    

    # # ----------------------------------------------------
    # # 1. Extract and Prepare DataFrame
    # # ----------------------------------------------------

    # FILTERED_DF = auto_extract(['municipality', 'counts'], is_specific=False)
    


    # print(combined_geojson['features'][0]['properties'])
    # geo_names = set([f['properties']['MUNICIPALI'] for f in combined_geojson['features']])
    # df_names = set(FILTERED_DF['final_municipality'].unique())

    # print("Missing in GeoJSON:", df_names - geo_names)
    # print("Extra in GeoJSON:", geo_names - df_names)




    

    # # ----------------------------------------------------
    # # 6. Plot Choropleth
    # # ----------------------------------------------------

    # map_chart = px.choropleth(
    #     FILTERED_DF,
    #     geojson=combined_geojson,
    #     locations='municipality',
    #     featureidkey='properties.MUNICIPALI',
    #     color='counts',
    #     hover_name='municipality',
    #     hover_data=['counts'],
    #     color_continuous_scale='Viridis',
    # )

    # map_chart.update_geos(fitbounds="locations", visible=False)
    # map_chart.update_layout(title="Enrollment by Municipality", margin={"r": 0, "t": 30, "l": 0, "b": 0})
    # map_chart.show(renderer="browser")

    # ==========================================
    
    # FILTERED_DF = auto_extract(['municipality', 'counts'], is_specific=False)
    # FILTERED_DF = FILTERED_DF.groupby('municipality', as_index=False)['counts'].sum()
    
    # unique_municipalities = FILTERED_DF['municipality'].drop_duplicates().tolist()
    # print("Municipalities in DataFrame:", len(unique_municipalities))
    # for municipality in sorted(unique_municipalities):
    #     print(municipality)
    
    # geojson_folder = "/Users/marke/Downloads/muni/"
    # geojson_files = [
    #     "ABRA.geojson",
    #     "AGUSAN DEL NORTE.geojson",
    #     "AGUSAN DEL SUR.geojson",
    #     "AKLAN.geojson",
    #     "ALBAY.geojson",
    #     "ANTIQUE.geojson",
    #     "APAYAO.geojson",
    #     "AURORA.geojson",
    #     "BASILAN.geojson",
    #     "BATAAN.geojson",
    #     "BATANES.geojson",
    #     "BATANGAS.geojson",
    #     "BENGUET.geojson",
    #     "BILIRAN.geojson",
    #     "BOHOL.geojson",
    #     "BUKIDNON.geojson",
    #     "BULACAN.geojson",
    #     "CAGAYAN.geojson",
    #     "CAMARINES NORTE.geojson",
    #     "CAMARINES SUR.geojson",
    #     "CAMIGUIN.geojson",
    #     "CAPIZ.geojson",
    #     "CATANDUANES.geojson",
    #     "CAVITE.geojson",
    #     "CEBU.geojson",
    #     "CITY OF ISABELA.geojson",
    #     "COMPOSTELA VALLEY.geojson",
    #     "DAVAO DEL NORTE.geojson",
    #     "DAVAO DEL SUR.geojson",
    #     "DAVAO ORIENTAL.geojson",
    #     "DINAGAT ISLANDS.geojson",
    #     "EASTERN SAMAR.geojson",
    #     "FIRST DISTRICT.geojson",
    #     "FOURTH DISTRICT.geojson",
    #     "GUIMARAS.geojson",
    #     "IFUGAO.geojson",
    #     "ILOCOS NORTE.geojson",
    #     "ILOCOS SUR.geojson",
    #     "ILOILO.geojson",
    #     "ISABELA.geojson",
    #     "KALINGA.geojson",
    #     "LA UNION.geojson",
    #     "LAGUNA.geojson",
    #     "LANAO DEL NORTE.geojson",
    #     "LANAO DEL SUR.geojson",
    #     "LEYTE.geojson",
    #     "MAGUINDANAO.geojson",
    #     "MARINDUQUE.geojson",
    #     "MASBATE.geojson",
    #     "MISAMIS OCCIDENTAL.geojson",
    #     "MISAMIS ORIENTAL.geojson",
    #     "MOUNTAIN PROVINCE.geojson",
    #     "NEGROS OCCIDENTAL.geojson",
    #     "NEGROS ORIENTAL.geojson",
    #     "NORTH COTABATO.geojson",
    #     "NORTHERN SAMAR.geojson",
    #     "NUEVA ECIJA.geojson",
    #     "NUEVA VIZCAYA.geojson",
    #     "OCCIDENTAL MINDORO.geojson",
    #     "ORIENTAL MINDORO.geojson",
    #     "PALAWAN.geojson",
    #     "PAMPANGA.geojson",
    #     "PANGASINAN.geojson",
    #     "QUEZON.geojson",
    #     "QUIRINO.geojson",
    #     "RIZAL.geojson",
    #     "ROMBLON.geojson",
    #     "SAMAR (WESTERN SAMAR).geojson",
    #     "SARANGANI.geojson",
    #     "SECOND DISTRICT.geojson",
    #     "SIQUIJOR.geojson",
    #     "SORSOGON.geojson",
    #     "SOUTH COTABATO.geojson",
    #     "SOUTHERN LEYTE.geojson",
    #     "SULTAN KUDARAT.geojson",
    #     "SULU.geojson",
    #     "SURIGAO DEL NORTE.geojson",
    #     "SURIGAO DEL SUR.geojson",
    #     "TARLAC.geojson",
    #     "TAWI-TAWI.geojson",
    #     "THIRD DISTRICT.geojson",
    #     "ZAMBALES.geojson",
    #     "ZAMBOANGA DEL NORTE.geojson",
    #     "ZAMBOANGA DEL SUR.geojson",
    #     "ZAMBOANGA SIBUGAY.geojson"
    # ]

    # all_features = []
    # for filename in geojson_files:
    #     filepath = os.path.join(geojson_folder, filename)
    #     with open(filepath) as f:
    #         geo = json.load(f)
            
    #         if geo.get("type") == "FeatureCollection":
    #             all_features.extend(geo["features"])
            
    #         elif geo.get("type") == "Feature":
    #             all_features.append(geo)

    #         elif geo.get("type") == "GeometryCollection":
    #             for geometry in geo.get("geometries", []):
    #                 feature = {
    #                     "type": "Feature",
    #                     "geometry": geometry,
    #                     "properties": {}  # Empty properties; customize if needed
    #                 }
    #                 all_features.append(feature)
            
    #         else:
    #             print(f" Unexpected GeoJSON type in {filename}.json → {geo.get('type')}")


    # combined_geojson = {
    #     "type": "FeatureCollection",
    #     "features": all_features
    # }
    
    # geo_municipalities = [feature['properties']['MUNICIPALI'] for feature in combined_geojson['features'] if feature['properties'].get('MUNICIPALI')]

    # print("Municipalities in GeoJSON:", len(set(geo_municipalities)))
    # print("Sample GeoJSON names:", sorted(set(geo_municipalities))[:10])

    # # Normalize names for better matching
    # FILTERED_DF['normalized_municipality'] = FILTERED_DF['municipality'].str.strip().str.title()
    # geo_municipalities_normalized = [m.strip().title() for m in geo_municipalities if m]

    # # # Keep only those present in GeoJSON
    # FILTERED_DF = FILTERED_DF[FILTERED_DF['normalized_municipality'].isin(geo_municipalities_normalized)]

    # # Plot choropleth
    # map_chart = px.choropleth(
    #     FILTERED_DF,
    #     geojson=combined_geojson,
    #     locations='municipality',
    #     featureidkey='properties.MUNICIPALI',
    #     color='counts',
    #     hover_name='municipality',
    #     hover_data=['counts'],
    #     color_continuous_scale='Viridis',
    # )

    # map_chart.update_traces(
    #     hovertemplate="<b>%{location}</b><br>Total Enrollment: %{z:,}<extra></extra>"
    # )


    # map_chart.update_geos(
    #     visible=False,
    #     # showcountries=False,
    #     # showcoastlines=False,
    #     showland=True,
    #     fitbounds="locations",        # Ensures focus on actual geojson features
    #     center = {'lat':12.8797, 'lon':121.7740},
    #     resolution=50,
    #     lataxis_range=[4, 21],        # Latitude range for PH
    #     lonaxis_range=[115, 128],  # Longitude range for PH
    # )



    # map_chart.update_layout(
    #     # title="Enrollment by Region",
    #     # title_font=dict(size=20, family='Inter', color='#3C6382'),
    #     # title_x=0.5,
    #     margin={"r": 0, "t": 0, "l": 0, "b": 0},
    #     paper_bgcolor='white',
    #     plot_bgcolor='rgba(0,0,0,0)',
    #     coloraxis_showscale=False,
    #     # dragmode=False,
    # )
    
    # map_chart.show(renderer="browser")



    # from rapidfuzz import process, fuzz
    # import unicodedata
    # import re

    # def normalize_municipality(name):
    #     if not name:
    #         return ""
        
    #     name = re.sub(r"\s*\(.*?\)", "", name).strip()
    #     if name.lower().startswith("city of "):
    #         name = name[8:] + " City"
    #     elif name.lower().startswith("city "):
    #         name = name[5:] + " City"
    #     elif name.lower().startswith("cityof "):
    #         name = name[7:] + " City"

    #     # Normalize Unicode
    #     name = unicodedata.normalize('NFKD', name)
    #     name = ''.join(c for c in name if not unicodedata.combining(c))
        
    #     return name.title()

    # # Normalize
    # df_normalized = [normalize_municipality(m) for m in unique_municipalities]
    # geo_normalized = [normalize_municipality(m) for m in geo_municipalities if m]

    # # Use RapidFuzz to match names that aren't in the direct intersection
    # df_set = set(df_normalized)
    # geo_set = set(geo_normalized)

    # # Exact matches
    # matches = sorted(df_set & geo_set)

    # # Fuzzy matches for ones not matched exactly
    # in_df_not_in_geo = sorted(df_set - geo_set)

    # fuzzy_matches = []
    # for name in in_df_not_in_geo:
    #     best_match, score, _ = process.extractOne(name, geo_set, scorer=fuzz.ratio)
    #     if score >= 85:
    #         fuzzy_matches.append((name, best_match, score))

    # # Show fuzzy match results
    # print("\n🔍 Fuzzy Matches (Score ≥ 85):")
    # for original, matched, score in fuzzy_matches:
    #     print(f" 🔁 {original} ↔ {matched} ({score}%)")

    # # Optional: remove fuzzy matches from unmatched
    # fuzzy_matched_names = {name for name, _, _ in fuzzy_matches}
    # remaining_unmatched = sorted(df_set - geo_set - fuzzy_matched_names)

    # print(f"\n❌ Still Unmatched ({len(remaining_unmatched)}):")
    # for m in remaining_unmatched:
    #     print(" ❌", m)
        
    #     # Prepare output
    # {
    #     "exact_matches": sorted(list(exact_matches)),
    #     "unmatched_provinces": unmatched_provinces,
    #     "fuzzy_matches": fuzzy_matches
    # }
    
    # print(FILTERED_DF.to_string())


    # unique_provinces = FILTERED_DF['province'].drop_duplicates().tolist()
    # for province in unique_provinces:
    #     print(province)    
    # ================================================================================================================
#     FILTERED_DF = auto_extract(['province', 'counts'], is_specific=False)
#     FILTERED_DF = FILTERED_DF.groupby('province', as_index=False)['counts'].sum()
        
#         # Print for debug
#     unique_provinces = FILTERED_DF['province'].drop_duplicates().tolist()
#     print("Provinces in DataFrame:", len(unique_provinces))
#     for province in sorted(unique_provinces):
#         print(province)

#     # Folder where all region-wise GeoJSON files are stored
#     geojson_folder = "/Users/marke/Downloads/lowres/"
#     geojson_files = [
#         "provinces-region-ph010000000.0.001.json",
#         "provinces-region-ph020000000.0.001.json",
#         "provinces-region-ph030000000.0.001.json",
#         "provinces-region-ph040000000.0.001.json",
#         "provinces-region-ph050000000.0.001.json",
#         "provinces-region-ph060000000.0.001.json",
#         "provinces-region-ph070000000.0.001.json",
#         "provinces-region-ph080000000.0.001.json",
#         "provinces-region-ph090000000.0.001.json",
#         "provinces-region-ph100000000.0.001.json",
#         "provinces-region-ph110000000.0.001.json",
#         "provinces-region-ph120000000.0.001.json",
#         "provinces-region-ph130000000.0.001.json",
#         "provinces-region-ph140000000.0.001.json",
#         "provinces-region-ph150000000.0.001.json",
#         "provinces-region-ph160000000.0.001.json",
#         "provinces-region-ph170000000.0.001.json",
#         "provinces-region-ph180000000.0.001.json",

#     ]

#     # Combine all province GeoJSONs into one FeatureCollection
#     all_features = []
#     for filename in geojson_files:
#         filepath = os.path.join(geojson_folder, filename)
#         with open(filepath) as f:
#             geo = json.load(f)
#             geo = rewind(geo, rfc7946=False)
#             all_features.extend(geo['features'])

#     combined_geojson = {
#         "type": "FeatureCollection",
#         "features": all_features
#     }

#     # Extract province names from GeoJSON
#     geo_provinces = [feature['properties']['ADM2_EN'] for feature in combined_geojson['features']]
#     print("Provinces in GeoJSON:", len(set(geo_provinces)))
#     print("Provinces in DataFrame:", len(set(FILTERED_DF['province'])))

#     # Normalize for comparison
#     df_norm = {name.strip().title() for name in unique_provinces}
#     geo_norm = {name.strip().title() for name in geo_provinces}

#     # Find unmatched from DataFrame
#     unmatched = sorted(df_norm - geo_norm)

#     print("\n❌ Unmatched provinces from DataFrame not found in GeoJSON:")
#     for prov in unmatched:
#         print(f"- {prov}")

    
#     def normalize_province(name):
#         if not name:
#             return ""
#         name = name.strip()

#         # Common fixes
#         name = name.replace("Ncr", "NCR")
#         name = re.sub(r"(?i)^city of\s+", "", name)
#         # name = re.sub(r",\s*NCR.*", "NCR", name)  # e.g., "Manila, NCR, First District" → "Manila NCR"
#         name = unicodedata.normalize('NFKD', name)
#         name = ''.join(c for c in name if not unicodedata.combining(c))
#         return name.title()

#     # Normalize both lists
#     df_normalized = [normalize_province(name) for name in unique_provinces]
#     geo_normalized = [normalize_province(name) for name in geo_provinces]

#     # Convert to sets
#     df_set = set(df_normalized)
#     geo_set = set(geo_normalized)

#     # Exact matches
#     matched = sorted(df_set & geo_set)
#     unmatched = sorted(df_set - geo_set)

#     print("\n✅ Matched provinces:")
#     for prov in matched:
#         print(f"  ✅ {prov}")

#     # Fuzzy match for unmatched
#     fuzzy_matches = []
#     for name in unmatched:
#         best_match, score, _ = process.extractOne(name, geo_set, scorer=fuzz.ratio)
#         if score >= 50:
#             fuzzy_matches.append((name, best_match, score))

#     # Output fuzzy matches
#     print("\n🔁 Fuzzy matched provinces:")
#     for original, matched, score in fuzzy_matches:
#         print(f"  🔁 {original} ↔ {matched} ({score}%)")

#     # Remaining unmatched after fuzzy match
#     fuzzy_matched_names = {original for original, _, _ in fuzzy_matches}
#     still_unmatched = sorted(set(unmatched) - fuzzy_matched_names)

#     print("\n❌ Still unmatched provinces:")
#     for prov in still_unmatched:
#         print(f"  ❌ {prov}")
        
        
#         # Step: Create mapping from fuzzy matches
#     fuzzy_match_dict_prov = {original: matched for original, matched, _ in fuzzy_matches}

#     # Step: Normalize and apply fuzzy match to province column in DF
#     FILTERED_DF['normalized_province'] = FILTERED_DF['province'].apply(normalize_province)

#     FILTERED_DF['final_province'] = FILTERED_DF['normalized_province'].apply(
#         lambda x: fuzzy_match_dict_prov.get(x, x)  # Use fuzzy match if exists, else use normalized
#     )

#     # Step: Normalize GeoJSON province names (no uppercasing)
#     geo_provinces_normalized_final = [normalize_province(p) for p in geo_provinces if p]

#     # Step: Filter DataFrame to matching provinces
#     FILTERED_DF = FILTERED_DF[
#         FILTERED_DF['final_province'].isin(geo_provinces_normalized_final)
#     ]

#     # Step: Print unmatched final provinces (optional debug)
#     unmatched_final = set(FILTERED_DF['final_province']) - set(geo_provinces_normalized_final)
#     if unmatched_final:
#         print("\n⚠️ Unmatched final provinces still not in GeoJSON:")
#         for p in sorted(unmatched_final):
#             print("  ❌", p)



    
#     # 4. Plotly Choropleth
#     map_chart = px.choropleth(
#         FILTERED_DF,
#         geojson=combined_geojson,
#         locations='final_province',
#         featureidkey='properties.ADM2_EN',
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
    
#     map_chart.show(renderer="browser")
# ===========================================================================================================================
    # FILTERED_DF = smart_filter(data, enrollment_db_engine)
    # FILTERED_DF = auto_extract(['province', 'counts'], is_specific=False)
    # FILTERED_DF = FILTERED_DF.groupby('province', as_index=False)['counts'].sum()

    # unique_provinces = FILTERED_DF['province'].drop_duplicates().tolist()
    # for province in unique_provinces:
    #     print(province)    
        
    #     # Print for debug
    # unique_provinces = FILTERED_DF['province'].drop_duplicates().tolist()
    # print("Provinces in DataFrame:", len(unique_provinces))
    # for province in sorted(unique_provinces):
    #     print(province)

    # # Folder where all region-wise GeoJSON files are stored
    # geojson_folder = "/Users/marke/Downloads/"
    # geojson_files = [
        # "provdists-region-100000000.0.001",
        # "provdists-region-1000000000.0.001",
        # "provdists-region-1100000000.0.001",
        # "provdists-region-1200000000.0.001",
        # "provdists-region-1300000000.0.001",
        # "provdists-region-1400000000.0.001",
        # "provdists-region-1600000000.0.001",
        # "provdists-region-1700000000.0.001",
        # "provdists-region-1900000000.0.001",
        # "provdists-region-200000000.0.001",
        # "provdists-region-300000000.0.001",
        # "provdists-region-400000000.0.001",
        # "provdists-region-500000000.0.001",
        # "provdists-region-600000000.0.001",
        # "provdists-region-700000000.0.001",
        # "provdists-region-800000000.0.001",
        # "provdists-region-900000000.0.001",
    # ]

    # # Combine all province GeoJSONs into one FeatureCollection
    # all_features = []
    # for filename in geojson_files:
    #     filepath = os.path.join(geojson_folder, filename + ".json")
    #     with open(filepath) as f:
    #         geo = json.load(f)
    #         geo = rewind(geo, rfc7946=False)  # Ensure proper winding
    #         all_features.extend(geo['features'])

    # combined_geojson = {
    #     "type": "FeatureCollection",
    #     "features": all_features
    # }

    # # Extract province names from GeoJSON
    # geo_provinces = [feature['properties']['adm2_en'] for feature in combined_geojson['features']]
    # print("Provinces in GeoJSON:", len(set(geo_provinces)))
    # print("Provinces in DataFrame:", set(FILTERED_DF['province']))


    # # Normalize casing and whitespace
    # FILTERED_DF['normalized_province'] = FILTERED_DF['province'].str.strip().str.title()
    # geo_provinces_normalized = [prov.strip().title() for prov in geo_provinces if prov]


    # # Keep only matching provinces
    # FILTERED_DF = FILTERED_DF[FILTERED_DF['normalized_province'].isin(geo_provinces_normalized)]
    
    # # 4. Plotly Choropleth
    # map_chart = px.choropleth(
    #     FILTERED_DF,
    #     geojson=combined_geojson,
    #     locations='normalized_province',
    #     featureidkey='properties.adm2_en',
    #     color='counts',
    #     hover_name=None,
    #     hover_data=None,
    #     color_continuous_scale='Viridis',
        
    # )
    
    # map_chart.update_traces(
    #     hovertemplate="<b>%{location}</b><br>Total Enrollment: %{z:,}<extra></extra>"
    # )


    # map_chart.update_geos(
    #     visible=False,
    #     # showcountries=False,
    #     # showcoastlines=False,
    #     showland=True,
    #     fitbounds="locations",        # Ensures focus on actual geojson features
    #     center = {'lat':12.8797, 'lon':121.7740},
    #     resolution=50,
    #     lataxis_range=[4, 21],        # Latitude range for PH
    #     lonaxis_range=[115, 128],  # Longitude range for PH
    # )



    # map_chart.update_layout(
    #     # title="Enrollment by Region",
    #     # title_font=dict(size=20, family='Inter', color='#3C6382'),
    #     # title_x=0.5,
    #     margin={"r": 0, "t": 0, "l": 0, "b": 0},
    #     paper_bgcolor='white',
    #     plot_bgcolor='rgba(0,0,0,0)',
    #     coloraxis_showscale=False,
    #     # dragmode=False,
    # )

