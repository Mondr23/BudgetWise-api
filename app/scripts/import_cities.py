import pandas as pd
import sqlite3

conn = sqlite3.connect("travel.db")

travel_cost = pd.read_csv("datasets/clean_travel_cost.csv")
weather = pd.read_csv("datasets/clean_weather.csv")

cities = pd.concat([
    travel_cost[["city"]],
    weather[["city"]]
]).drop_duplicates()

cities["country_code"] = None
cities["latitude"] = None
cities["longitude"] = None

cities.columns = ["city_name", "country_code", "latitude", "longitude"]

cities.to_sql("cities", conn, if_exists="append", index=False)

print("Cities imported")

conn.close()