import pandas as pd
import sqlite3

conn = sqlite3.connect("travel.db")

tourism = pd.read_csv("datasets/clean_tourism.csv")

countries = tourism[["country_code", "country"]].drop_duplicates()
countries.columns = ["country_code", "country_name"]

countries.to_sql("countries", conn, if_exists="append", index=False)

print("Countries imported")

conn.close()