import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn