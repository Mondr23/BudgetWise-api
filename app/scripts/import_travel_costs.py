import pandas as pd
import sqlite3

conn = sqlite3.connect("travel.db")

# load dataset
travel_cost = pd.read_csv("datasets/clean_travel_cost.csv")

# load cities table
cities = pd.read_sql("SELECT city_id, city_name FROM cities", conn)

# match dataset city with database city
travel_cost = travel_cost.merge(
    cities,
    left_on="city",
    right_on="city_name",
    how="left"
)

# warn about cities not found
missing = travel_cost[travel_cost["city_id"].isna()]

if len(missing) > 0:
    print("Warning: cities not found in cities table:")
    print(missing["city"].unique())

# remove rows without city_id
travel_cost = travel_cost.dropna(subset=["city_id"])

# keep only columns used by the database
travel_cost = travel_cost[[
    "city_id",
    "meal_price",
    "coffee_price",
    "beer_price",
    "transport_ticket",
    "taxi_km",
    "rent_city_center",
    "avg_salary",
    "daily_accommodation",
    "daily_cost_estimate"
]]

# insert into database
travel_cost.to_sql("travel_costs", conn, if_exists="append", index=False)

print("Travel costs imported successfully")

conn.close()