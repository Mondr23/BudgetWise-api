import pandas as pd
import sqlite3

conn = sqlite3.connect("travel.db")

# -------------------------
# LOAD DATASETS
# -------------------------

airports = pd.read_csv("datasets/clean_airports.csv")
weather = pd.read_csv("datasets/clean_weather.csv")
travel_cost = pd.read_csv("datasets/clean_travel_cost.csv")

# -------------------------
# EXTRACT CITY + COUNTRY
# -------------------------

# airports dataset
airports_cities = airports[["city", "country"]]

# weather dataset
weather_cities = weather[["city", "country"]]

# travel cost dataset
# cities look like "Paris, France"
# split city and country safely
travel_split = travel_cost["city"].str.split(",", expand=True)

# first column = city
city_col = travel_split[0].str.strip()

# last column = country
country_col = travel_split.iloc[:, -1].str.strip()

travel_cities = pd.DataFrame({
    "city": city_col,
    "country": country_col
})

# -------------------------
# COMBINE ALL CITIES
# -------------------------

cities = pd.concat([
    airports_cities,
    weather_cities,
    travel_cities
])

cities = cities.drop_duplicates()

# -------------------------
# MATCH WITH COUNTRIES TABLE
# -------------------------

countries = pd.read_sql("SELECT * FROM countries", conn)

cities = cities.merge(
    countries,
    left_on="country",
    right_on="country_name",
    how="left"
)

# -------------------------
# FINAL FORMAT
# -------------------------

cities["latitude"] = None
cities["longitude"] = None

cities = cities[[
    "city",
    "country_code",
    "latitude",
    "longitude"
]]

cities.columns = [
    "city_name",
    "country_code",
    "latitude",
    "longitude"
]

cities = cities.drop_duplicates()

# -------------------------
# INSERT INTO DATABASE
# -------------------------

#cities.to_sql("cities", conn, if_exists="replace", index=False)
cities.to_sql("cities", conn, if_exists="append", index=False)

print("Cities table rebuilt successfully")

conn.close()