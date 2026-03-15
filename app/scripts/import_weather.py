import pandas as pd
import sqlite3

conn = sqlite3.connect("travel.db")

# load dataset
weather = pd.read_csv("datasets/clean_weather.csv")

# load cities table
cities = pd.read_sql("SELECT city_id, city_name FROM cities", conn)

# match weather cities to database cities
weather = weather.merge(
    cities,
    left_on="city",
    right_on="city_name",
    how="left"
)

# keep only columns that exist in the database
weather = weather[[
    "city_id",
    "temperature",
    "humidity",
    "wind_kph",
    "precipitation",
    "visibility",
    "air_quality_pm25",
    "condition",
    "last_updated"
]]

# insert into database
weather.to_sql("weather", conn, if_exists="append", index=False)

print("Weather data imported successfully")

conn.close()