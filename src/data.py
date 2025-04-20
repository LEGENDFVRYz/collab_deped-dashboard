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
        query = "SELECT * FROM enrollment LEFT JOIN sch_info USING(beis_id) WHERE 1=1"  
        
        # Check if gender exist in the query
        if any(key in filter_info for key in ['gender', 'sector', 'sub_class', 'type', 'mod_coc']):
            for col_key, value in filter_info.items():
                
                if col_key in ['sector', 'sub_class', 'type', 'mod_coc']:
                    ## Multiples
                    placeholders = ', '.join([f":region_{i}" for i in range(len(regions))])
                    params = {f"region_{i}": region for i, region in enumerate(regions)}
                    
                    
                elif col_key in ['gender']:
                    ## Single
                    query += f"\nAND gender == '{filter_info['gender']}'"
            
        # JOIN: sch_info table manipulation
        # query = 
        
        # dataframe = pd.read_sql_query(main_query, con=engine)
        # return dataframe
            print(query)
        
    except Exception as e:
        print(f'error: {e}')
        

def get_engine():
    return enrollment_db_engine
    
if __name__ == '__main__':
    
    sample = {
        "sector": [
            "Public",
            "Private"
            ],
            "gender": "M",
            "region": [
                "CAR"
            ],
            "province": [
                "BENGUET"
            ],
            "division": [
                "Baguio City"
            ],
            "district": [
                "District II",
                "District III"
            ]
        }
    
    # query = smart_filter(sample)
    
    
    regions = ['NCR', 'BARMM', 'PSO']

    # Generate placeholders for the IN clause
    placeholders = ', '.join([f":region_{i}" for i in range(len(regions))])
    placeholders

    # Build the SQL query
    query = f"SELECT * FROM sch_region WHERE region IN ({placeholders})"
    params = {f"region_{i}": region for i, region in enumerate(regions)}
    
    # Read the SQL query
    df = pd.read_sql(query, con=enrollment_db_engine, params=params)
    
    print(query)