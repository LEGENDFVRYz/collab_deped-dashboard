from flask import Flask
from flask_caching import Cache
from src.utils.get_data import auto_extract

# Create Flask server
server = Flask(__name__)  


# Create Cache
cache = Cache(config={'CACHE_TYPE': 'simple'})

# Load and cache full dataset (on server)
@cache.memoize()
def load_location_data():
    # Fetch the data using SQL query
    dataframe = auto_extract([
        'region', 'division', 'district', 'province', 'municipality', 'brgy'
    ], is_specific=True, distinct=True)
    return dataframe

