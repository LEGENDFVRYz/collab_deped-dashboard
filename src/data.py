from sqlalchemy import create_engine
import pandas as pd
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from config import project_root


"""
    INITIALIZING DATABASE CONNECTION AND CUSTOM FUNCTIONS:
    
"""

# Database Engine
enrollment_db_engine = create_engine(f"sqlite:///{project_root / 'database/processed/sql/enrollment_data.db'}", echo=False)


def smart_filter(filter_info={}) -> pd.DataFrame:
    try:
        # Base query (JOIN: enrollment and sch_info)
        first_query = "SELECT * FROM enrollment LEFT JOIN sch_info USING(beis_id) WHERE 1=1"  
        params = {}
        
        first_scope = {
                'sector' : lambda x: f":sector_{x}",
                'sub_class' :lambda x: f":subclass_{x}",
                'type' :lambda x: f":type_{x}",
                'mod_coc' :lambda x: f":mod_coc_{x}"
        }
        
        second_scope = {
                'region' : lambda x: f":region_{x}",
                'province' :lambda x: f":province_{x}",
                'division' :lambda x: f":division_{x}",
                'district' :lambda x: f":district_{x}",
                'minicipality' :lambda x: f":municipality_{x}",
                'brgy' :lambda x: f":district_{x}"
        }
        
        third_scope = {
                'mod_coc' : lambda x: f":mod_coc_{x}",
                'grade' :lambda x: f":grade_{x}",
                'track' :lambda x: f":track_{x}",
                'strand' :lambda x: f":strand_{x}",
                'year' :lambda x: f":year_{x}",
        }
        
        
        # Check if there is column exist in the first_scope
        if any(key in filter_info for key in ['gender', 'sector', 'sub_class', 'type', 'mod_coc']):
            for col_key, value in filter_info.items():
                
                if col_key in ['sector', 'sub_class', 'type', 'mod_coc']:
                    ## Multiples
                    placeholders = ', '.join([first_scope[col_key](i) for i in range(len(value))])
                    params = {**params, **{first_scope[col_key](i)[1:]: v for i, v in enumerate(value)}}

                    first_query += f"\nAND {col_key} IN ({placeholders})"
                        
                if col_key in ['gender']:
                    ## Single
                    first_query += f"\nAND gender == '{filter_info['gender']}'"
        

        # JOIN: first_query + location detailes
        if any(key in filter_info for key in ['region', 'province', 'division', 'district']):
            region_query = f"""SELECT * FROM (
                {first_query}
            ) LEFT JOIN sch_region USING (region_id)
            LEFT JOIN sch_local USING (local_id)
            WHERE 1=1
            """
            for col_key, value in filter_info.items():
                if col_key in ['region', 'province', 'division', 'district', 'municipality', 'brgy']:
                    ## LOCATION
                    placeholders = ', '.join([second_scope[col_key](i) for i in range(len(value))])
                    params = {**params, **{second_scope[col_key](i)[1:]: v for i, v in enumerate(value)}}
                    
                    region_query += f"\nAND {col_key} IN ({placeholders})"
        else:
            # NO LOCATION FILTER SELECTED
            region_query = first_query
        
        
        ## JOIN: region_query + grade
        if any(key in filter_info for key in ['mod_coc', 'grade', 'strand', 'track', 'year']):
            grade_query = """SELECT * FROM (
                SELECT enroll_id, beis_id, gender, '__NaN__' as track, '__NaN__' as strand, grade, counts, year FROM enrollment
                INNER JOIN ES_enroll USING(enroll_id)

                UNION ALL

                SELECT enroll_id, beis_id, gender, '__NaN__' as track, '__NaN__' as strand, grade, counts, year FROM enrollment 
                INNER JOIN JHS_enroll USING(enroll_id)

                UNION ALL

                SELECT enroll_id, beis_id, gender, track, strand, grade, counts, year FROM enrollment 
                INNER JOIN SHS_enroll USING(enroll_id)
            )
            WHERE 1=1"""
            
            for col_key, value in filter_info.items():
                if col_key in ['mod_coc', 'grade', 'strand', 'track', 'year']:
                    ## LOCATION
                    placeholders = ', '.join([third_scope[col_key](i) for i in range(len(value))])
                    params = {**params, **{third_scope[col_key](i)[1:]: v for i, v in enumerate(value)}}

                    grade_query += f"\nAND {col_key} IN ({placeholders})"
            
            ## MAIN QUERY
            main_query = f"""
                SELECT * FROM (
                    {region_query}
                ) INNER JOIN (
                    {grade_query}
                ) USING (enroll_id, beis_id, gender)
            """
        else:
            main_query = region_query
            
            
        dataframe = pd.read_sql_query(main_query, con=enrollment_db_engine, params=params)
        return dataframe
        
        # print(grade_query)
        # print("params:\n", params)
        
    except Exception as e:
        print(f'error: {e}')
        

def get_engine():
    return enrollment_db_engine
    
    
    
if __name__ == '__main__':
    sample = {
        "sector": [
            "Private",
            "Public"
        ],
        "subclass": [
            "Non-Sectarian"
        ],
        "track": [
            "ARTS"
        ],
        # "grade": [
        #     "G8",
        #     "G9",
        #     "G10"
        # ],
        "region": [
            "MIMAROPA"
        ],
        "province": [
            "ORIENTAL MINDORO"
        ],
        "division": [
            "Calapan City"
        ],
        "district": [
            "Calapan South"
        ]
    }
    
    df = smart_filter(sample)
    df