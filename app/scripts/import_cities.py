import pandas as pd
from app.database import SessionLocal
from app.models.city import City
from app.models.country import Country 

# --- LOAD DATASETS ---
cost = pd.read_csv("datasets/clean_travel_cost.csv")
weather = pd.read_csv("datasets/clean_weather.csv")

# --- DB SESSION ---
db = SessionLocal()

# --- NORMALIZE FUNCTION ---
def normalize(text):
    return str(text).strip().title()

# --- STORE UNIQUE CITIES ---
cities = set()

# --- FROM COST DATA ---
for _, row in cost.iterrows():
    city = normalize(row["city"])
    country = normalize(row["country"])

    if city and country:
        cities.add((city, country))

# --- FROM WEATHER DATA ---
for _, row in weather.iterrows():
    city = normalize(row["city"])
    country = normalize(row["country"])

    if city and country:
        cities.add((city, country))


# --- INSERT ---
count = 0
skipped = 0

for city_name, country_name in cities:

    #  GET COUNTRY FROM DB 
    country = db.query(Country).filter_by(country_name=country_name).first()

    if not country:
        skipped += 1
        continue  # skip if country not found

    code = country.country_code

    # --- CHECK DUPLICATE CITY ---
    existing = db.query(City).filter_by(
        city_name=city_name,
        country_code=code
    ).first()

    if not existing:
        db.add(City(
            city_name=city_name,
            country_code=code
        ))
        count += 1


db.commit()
db.close()

print(f" Inserted {count} unique cities")
print(f" Skipped {skipped} (missing country match)")