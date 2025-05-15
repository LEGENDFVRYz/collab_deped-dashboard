import os
from flask import Flask
from flask_caching import Cache
from dotenv import load_dotenv
from src.utils.get_data import auto_extract

# Load secrets from .env file
load_dotenv()

# Create Flask server
server = Flask(__name__)  
server.secret_key = os.environ.get("SECRET_KEY")    # Secret Key for cookies

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
