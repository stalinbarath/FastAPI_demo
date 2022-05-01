import psycopg2
import pandas as pd

conn = psycopg2.connect(
    database = 'demodb',
    user = 'postgres',
    password = 'admin',
    host = '127.0.0.1',
    port = 5432)

config_data = pd.read_csv('data/FastAPI_POC.csv')