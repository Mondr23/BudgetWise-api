import pandas as pd

df = pd.read_csv("datasets/travel_cost.csv")

df = df[[
"City",
"Meal, Inexpensive Restaurant",
"Cappuccino (regular)",
"Domestic Beer (0.5 liter draught)",
"One-way Ticket (Local Transport)",
"Taxi 1km (Normal Tariff)",
"Apartment (1 bedroom) in City Centre",
"Average Monthly Net Salary (After Tax)"
]]

df.columns = [
"city",
"meal_price",
"coffee_price",
"beer_price",
"transport_ticket",
"taxi_km",
"rent_city_center",
"avg_salary"
]

df["daily_cost_estimate"] = (
df["meal_price"] +
df["coffee_price"] +
df["transport_ticket"]
)

df = df.dropna()

df.to_csv("datasets/clean_travel_cost.csv", index=False)

print("Travel cost dataset cleaned")