from numpy import append
from sqlalchemy import create_engine
import pandas as pd
import os, sys

# import json
# import os
# import plotly.express as px
# from geojson_rewind import rewind
# import pandas as pd
# import plotly.io as pio


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
    df = auto_extract(['region'], is_specific=False)
    df
    
    ############################################ PROVINCE
    # # Set Plotly renderer
    # pio.renderers.default = "browser"

    # # Load your province-level data (replace this with actual loading logic)
    # FILTERED_DF = auto_extract(['counts', 'province'], is_specific=True)
    # FILTERED_DF = FILTERED_DF.groupby('province', as_index=False)['counts'].sum()

    # # Folder where all region-wise GeoJSON files are stored
    # geojson_folder = "/Users/marke/Downloads/"
    # geojson_files = [
    #     "provdists-region-100000000.0.001",
    #     "provdists-region-1000000000.0.001",
    #     "provdists-region-1100000000.0.001",
    #     "provdists-region-1200000000.0.001",
    #     "provdists-region-1300000000.0.001",
    #     "provdists-region-1400000000.0.001",
    #     "provdists-region-1600000000.0.001",
    #     "provdists-region-1700000000.0.001",
    #     "provdists-region-1900000000.0.001",
    #     "provdists-region-200000000.0.001",
    #     "provdists-region-300000000.0.001",
    #     "provdists-region-400000000.0.001",
    #     "provdists-region-500000000.0.001",
    #     "provdists-region-600000000.0.001",
    #     "provdists-region-700000000.0.001",
    #     "provdists-region-800000000.0.001",
    #     "provdists-region-900000000.0.001",
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
    # print("Provinces in GeoJSON:", set(geo_provinces))
    # print("Provinces in DataFrame:", set(FILTERED_DF['province']))

    # # Full province name mapping
    # province_name_map = {
    #     'Abra': 'ABRA',
    #     'Agusan del Norte': 'AGUSAN DEL NORTE',
    #     'Agusan del Sur': 'AGUSAN DEL SUR',
    #     'Aklan': 'AKLAN',
    #     'Albay': 'ALBAY',
    #     'Antique': 'ANTIQUE',
    #     'Apayao': 'APAYAO',
    #     'Aurora': 'AURORA',
    #     'Basilan': 'BASILAN',
    #     'Bataan': 'BATAAN',
    #     'Batanes': 'BATANES',
    #     'Batangas': 'BATANGAS',
    #     'Benguet': 'BENGUET',
    #     'Biliran': 'BILIRAN',
    #     'Bohol': 'BOHOL',
    #     'Bukidnon': 'BUKIDNON',
    #     'Bulacan': 'BULACAN',
    #     'Cagayan': 'CAGAYAN',
    #     'Camarines Norte': 'CAMARINES NORTE',
    #     'Camarines Sur': 'CAMARINES SUR',
    #     'Camiguin': 'CAMIGUIN',
    #     'Capiz': 'CAPIZ',
    #     'Catanduanes': 'CATANDUANES',
    #     'Cavite': 'CAVITE',
    #     'Cebu': 'CEBU',
    #     'Compostela Valley': 'COMPOSTELA VALLEY',
    #     'Davao de Oro': 'COMPOSTELA VALLEY',
    #     'Davao del Norte': 'DAVAO DEL NORTE',
    #     'Davao del Sur': 'DAVAO DEL SUR',
    #     'Davao Occidental': 'DAVAO OCCIDENTAL',
    #     'Davao Oriental': 'DAVAO ORIENTAL',
    #     'Dinagat Islands': 'DINAGAT ISLANDS',
    #     'Eastern Samar': 'EASTERN SAMAR',
    #     'Guimaras': 'GUIMARAS',
    #     'Ifugao': 'IFUGAO',
    #     'Ilocos Norte': 'ILOCOS NORTE',
    #     'Ilocos Sur': 'ILOCOS SUR',
    #     'Iloilo': 'ILOILO',
    #     'Isabela': 'ISABELA',
    #     'Kalinga': 'KALINGA',
    #     'La Union': 'LA UNION',
    #     'Laguna': 'LAGUNA',
    #     'Lanao del Norte': 'LANAO DEL NORTE',
    #     'Lanao del Sur': 'LANAO DEL SUR',
    #     'Leyte': 'LEYTE',
    #     'Maguindanao del Norte': 'MAGUINDANAO',
    #     'Maguindanao del Sur': 'MAGUINDANAO',
    #     'Marinduque': 'MARINDUQUE',
    #     'Masbate': 'MASBATE',
    #     'Mountain Province': 'MOUNTAIN PROVINCE',
    #     'Misamis Occidental': 'MISAMIS OCCIDENTAL',
    #     'Misamis Oriental': 'MISAMIS ORIENTAL',
    #     'Northern Samar': 'NORTHERN SAMAR',
    #     'Nueva Ecija': 'NUEVA ECIJA',
    #     'Nueva Vizcaya': 'NUEVA VIZCAYA',
    #     'Occidental Mindoro': 'OCCIDENTAL MINDORO',
    #     'Oriental Mindoro': 'ORIENTAL MINDORO',
    #     'Palawan': 'PALAWAN',
    #     'Pampanga': 'PAMPANGA',
    #     'Pangasinan': 'PANGASINAN',
    #     'Quezon': 'QUEZON',
    #     'Quirino': 'QUIRINO',
    #     'Rizal': 'RIZAL',
    #     'Romblon': 'ROMBLON',
    #     'Samar': 'WESTERN SAMAR',
    #     'Sarangani': 'SARANGANI',
    #     'Siquijor': 'SIQUIJOR',
    #     'Sorsogon': 'SORSOGON',
    #     'South Cotabato': 'SOUTH COTABATO',
    #     'Southern Leyte': 'SOUTHERN LEYTE',
    #     'Sultan Kudarat': 'SULTAN KUDARAT',
    #     'Sulu': 'SULU',
    #     'Surigao del Norte': 'SURIGAO DEL NORTE',
    #     'Surigao del Sur': 'SURIGAO DEL SUR',
    #     'Tarlac': 'TARLAC',
    #     'Tawi-Tawi': 'TAWI-TAWI',
    #     'Zambales': 'ZAMBALES',
    #     'Zamboanga del Norte': 'ZAMBOANGA DEL NORTE',
    #     'Zamboanga del Sur': 'ZAMBOANGA DEL SUR',
    #     'Zamboanga Sibugay': 'ZAMBOANGA SIBUGAY',
    #     'NCR, Second District (Not a Province)': 'NCR   SECOND DISTRICT',
    #     'NCR, Third District (Not a Province)': 'NCR   THIRD DISTRICT',
    #     'NCR, Fourth District (Not a Province)': 'NCR   FOURTH DISTRICT',
    #     'NCR, City of Manila, First District (Not a Province)': 'MANILA, NCR,  FIRST DISTRICT ',
    #     'City of Isabela (Not a Province)': 'CITY OF ISABELA',
    #     'City of Cotabato': 'CITY OF COTABATO',
    # }

    # # Map DF province names to GeoJSON
    # inverse_map = {v: k for k, v in province_name_map.items()}
    # FILTERED_DF['geo_province'] = FILTERED_DF['province'].map(inverse_map).fillna(FILTERED_DF['province'])

    # # Drop rows where geo_province not in GeoJSON
    # FILTERED_DF = FILTERED_DF[FILTERED_DF['geo_province'].isin(geo_provinces)]

    # # Plot choropleth
    # map_chart = px.choropleth(
    #     FILTERED_DF,
    #     geojson=combined_geojson,
    #     locations='geo_province',
    #     featureidkey='properties.adm2_en',
    #     color='counts',
    #     hover_name='province',
    #     hover_data=['counts'],
    #     color_continuous_scale='Viridis',
    # )

    # map_chart.update_geos(fitbounds="locations", visible=False)
    # map_chart.update_layout(title="Enrollment by Province", margin={"r": 0, "t": 30, "l": 0, "b": 0})
    # map_chart.show(renderer="browser")

    
    
  ############################3 REGION  
#     pio.renderers.default = "browser"
    
# # Load your enrollment data
# # This is a temporary dataframe for testing charts
#     FILTERED_DF = auto_extract(['counts', 'region'], is_specific=True)
#     FILTERED_DF = FILTERED_DF.groupby('region', as_index=False)['counts'].sum()

#     # Load GeoJSON (municipality level for PH)
#     with open("/Users/marke/Downloads/country.0.001.json") as f:
#         geojson = json.load(f)

#     geojson = rewind(geojson, rfc7946=False)

#     # Print all REGION names in GeoJSON
#     geo_regions = [feature['properties']['adm1_en'] for feature in geojson['features']]
#     print(set(geo_regions))

#     # Print all region names in your DF
#     print(set(FILTERED_DF['region']))

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

#     # Map region names to GeoJSON-compatible names
#     FILTERED_DF['geo_region'] = FILTERED_DF['region'].map(region_name_map)
#     FILTERED_DF = FILTERED_DF.dropna(subset=['geo_region'])

#     # Plot the map
#     map_chart = px.choropleth(
#         FILTERED_DF,
#         geojson=geojson,
#         locations='geo_region',
#         featureidkey='properties.adm1_en',
#         color='counts',
#         hover_name='region',
#         hover_data=['counts'],
#         color_continuous_scale='Viridis',
#     )

#     map_chart.update_geos(fitbounds="locations", visible=False)
#     map_chart.update_layout(title="Enrollment by Region", margin={"r": 0, "t": 30, "l": 0, "b": 0})
#     map_chart.show(renderer="browser")


