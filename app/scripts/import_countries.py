import pandas as pd
from app.database import SessionLocal
from app.models.country import Country

# --- LOAD DATASETS ---
tourism = pd.read_csv("datasets/clean_tourism.csv")
cost = pd.read_csv("datasets/clean_travel_cost.csv")
weather = pd.read_csv("datasets/clean_weather.csv")

db = SessionLocal()

# --- NORMALIZE ---
def normalize(name):
    return str(name).strip().title()

# --- STORE UNIQUE ---
countries_by_code = {}
countries_by_name = {}

# --- STEP 1: USE TOURISM (BEST SOURCE) ---
for _, row in tourism.iterrows():
    name = normalize(row["country"])
    code = str(row["country_code"]).strip()

    if not name or not code:
        continue

    countries_by_code[code] = name
    countries_by_name[name] = code

# --- STEP 2: ADD MISSING COUNTRIES ONLY ---
def add_country_if_missing(name):
    name = normalize(name)

    if not name:
        return

    # already exists → skip
    if name in countries_by_name:
        return

    # generate fallback code
    code = name[:2].upper()

    # 🔥 FIX: avoid duplicate codes
    if code in countries_by_code:
        return  # skip instead of crashing

    countries_by_code[code] = name
    countries_by_name[name] = code


# --- DATASET 2 ---
for _, row in cost.iterrows():
    add_country_if_missing(row["country"])

# --- DATASET 3 ---
for _, row in weather.iterrows():
    add_country_if_missing(row["country"])


# --- INSERT INTO DB ---
inserted = 0

for code, name in countries_by_code.items():

    existing = db.query(Country).filter_by(country_code=code).first()

    if not existing:
        db.add(Country(
            country_code=code,
            country_name=name
        ))
        inserted += 1

db.commit()
db.close()

print(f" Inserted {inserted} countries safely")