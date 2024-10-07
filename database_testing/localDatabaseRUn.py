import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost", # add my ip address
    dbname ="WIld-Fire-Mapping",
    user='postgres',
    password = "potato",
    port = 5432)

cur = conn.cursor()

query = """
SELECT latitude, longitude, FRP FROM ire WHERE frp >300;
"""
#df = pd.read_sql(query, conn)

cur.execute(query)
while True:
    row = cur.fetchone()
    if row is None:  # No more rows
        break
    latitude, longitude, frp = row
    print(f"Latitude: {latitude}, Longitude: {longitude}, FRP: {frp}")
    print(latitude)
    print(longitude)
    print(frp)
    
cur.close()
conn.close()