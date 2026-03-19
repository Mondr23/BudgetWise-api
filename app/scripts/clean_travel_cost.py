import pandas as pd

df = pd.read_csv("datasets/travel_cost.csv")

# --- SPLIT CITY AND COUNTRY ---
# Example: "Saint Petersburg, Russia"
df[["city", "country"]] = df["City"].str.split(",", n=1, expand=True)

# clean spaces
df["city"] = df["city"].str.strip()
df["country"] = df["country"].str.strip()

# --- SELECT COLUMNS ---
df = df[[
    "city",
    "country",
    "Meal, Inexpensive Restaurant",
    "Cappuccino (regular)",
    "Domestic Beer (0.5 liter draught)",
    "One-way Ticket (Local Transport)",
    "Taxi 1km (Normal Tariff)",
    "Apartment (1 bedroom) in City Centre",
    "Average Monthly Net Salary (After Tax)"
]]

# --- RENAME COLUMNS ---
df.columns = [
    "city",
    "country",
    "meal_price",
    "coffee_price",
    "beer_price",
    "transport_ticket",
    "taxi_km",
    "rent_city_center",
    "avg_salary"
]

# --- DAILY ACCOMMODATION ---
df["daily_accommodation"] = (df["rent_city_center"] / 30) * 1.5

# --- DAILY COST ESTIMATE ---
df["daily_cost_estimate"] = (
    df["meal_price"] +
    df["coffee_price"] +
    df["transport_ticket"] +
    df["daily_accommodation"]
)

# --- CLEAN DATA ---
df = df.dropna()

# --- SAVE ---
df.to_csv("datasets/clean_travel_cost.csv", index=False)

print("✅ Travel cost dataset cleaned with city + country")


# Convert monthly rent to estimated tourist daily accommodation cost
# Long-term rental prices are usually lower than short-term accommodation
# (Airbnb / hotel stays). Studies of short-term rental markets show that
# nightly prices are typically 40%–100% higher than equivalent long-term
# rent due to service fees, cleaning costs, and flexible stays.
#
# Source examples:
# - AirDNA Short-Term Rental Market Reports
#   https://www.airdna.co/blog/short-term-rental-data
# - BudgetYourTrip Travel Cost Methodology
#   https://www.budgetyourtrip.com
# - Numbeo Cost of Living Methodology
#   https://www.numbeo.com/cost-of-living/methodology.jsp
#
# Therefore we approximate tourist accommodation as 1.5× the long-term
# daily rent (a midpoint within the 40–100% range).