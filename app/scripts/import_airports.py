import pandas as pd
import sqlite3

conn = sqlite3.connect("travel.db")

# load dataset
airports = pd.read_csv("datasets/clean_airports.csv")

# load cities table
cities = pd.read_sql("SELECT city_id, city_name FROM cities", conn)

# match airport city to database city
airports = airports.merge(
    cities,
    left_on="city",
    right_on="city_name",
    how="left"
)

# warn about missing cities
missing = airports[airports["city_id"].isna()]

if len(missing) > 0:
    print("Warning: airports with unknown cities:")
    print(missing["city"].unique())

# remove rows without city_id
airports = airports.dropna(subset=["city_id"])

# keep only columns that exist in database
airports = airports[[
    "name",
    "iata",
    "icao",
    "city_id",
    "latitude",
    "longitude",
    "timezone"
]]

# insert into database
airports.to_sql("airports", conn, if_exists="append", index=False)

print("Airports imported successfully")

conn.close()