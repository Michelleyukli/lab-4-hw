import psycopg2
import os

try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    print("Connection successful")
except Exception as e:
    print("Error connecting to the database:", e)
finally:
    if conn:
        conn.close()
