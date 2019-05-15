import os
from configparser import ConfigParser
import queries

SCRIPT_DIR = os.path.dirname(__file__)

def get_session():
    # Read the configuration from the database.ini file
    parser = ConfigParser()
    parser.read('database.ini')
    if parser.has_section('database'):
        params = parser._sections['database']
        connection_string = queries.uri(**params)
    else:
        raise Exception(f'Section "database" not found in file database.ini')
    # Set the queries.Session object as a field on the class for reuse
    return queries.Session(connection_string)