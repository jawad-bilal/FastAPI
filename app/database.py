import psycopg
from dotenv import load_dotenv
import os
from psycopg.rows import dict_row

load_dotenv()

conn = psycopg.connect(
    host=os.getenv("DATABASE_HOST"),
    dbname=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    port=os.getenv("DATABASE_PORT"),
)

cursor = conn.cursor(row_factory=dict_row)

if conn:
    print("Database connection successful")
else:
    print("Database connection failed")