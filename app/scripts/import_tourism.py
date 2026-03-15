import pandas as pd
import sqlite3

conn = sqlite3.connect("travel.db")

tourism = pd.read_csv("datasets/clean_tourism.csv")

tourism = tourism[["country_code", "year", "tourist_arrivals"]]

tourism.to_sql("tourism_statistics", conn, if_exists="append", index=False)

print("Tourism statistics imported")

conn.close()