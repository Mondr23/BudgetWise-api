import pandas as pd
from app.database import SessionLocal
from app.models.city import City
from app.models.country import Country
from app.models.weather import Weather

# --- LOAD DATA ---
weather_df = pd.read_csv("datasets/clean_weather.csv")

#  KEEP ONLY ONE ROW PER CITY + COUNTRY (the last Value)
weather_df = weather_df.drop_duplicates(subset=["city", "country"])

db = SessionLocal()

def normalize(text):
    return str(text).strip().title()

inserted = 0
skipped = 0

for _, row in weather_df.iterrows():

    city_name = normalize(row["city"])
    country_name = normalize(row["country"])
    condition = str(row["condition"]).strip()

    # --- GET COUNTRY ---
    country = db.query(Country).filter_by(
        country_name=country_name
    ).first()

    if not country:
        skipped += 1
        continue

    # --- GET CITY ---
    city = db.query(City).filter_by(
        city_name=city_name,
        country_code=country.country_code
    ).first()

    if not city:
        skipped += 1
        continue

    #  CHECK IF CITY ALREADY HAS WEATHER
    existing = db.query(Weather).filter_by(
        city_id=city.city_id
    ).first()

    if existing:
        continue  # skip (only one allowed)

    # --- INSERT ---
    new_weather = Weather(
        city_id=city.city_id,
        condition=condition
    )

    db.add(new_weather)
    inserted += 1

db.commit()
db.close()

print(f" Inserted {inserted} weather records (1 per city)")
print(f" Skipped {skipped}")