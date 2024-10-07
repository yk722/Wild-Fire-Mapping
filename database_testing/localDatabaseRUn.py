import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="128.189.228.90", # add my ip address
    dbname ="WIld-Fire-Mapping",
    user='postgres',
    password = "potato",
    port = 5432)

cur = conn.cursor()
with open(r'output.csv', 'r') as f:
    # Notice that we don't need the csv module.
    next(f) # Skip the header row.
    cur.copy_from(f, 'complete', sep=',')

conn.commit()
cur.close()
conn.close()