import pandas as pd

# Load dataset
df = pd.read_csv("datasets/Tourism_Statistics.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Identify year columns
year_columns = [col for col in df.columns if col.isdigit()]

clean_rows = []

# Loop through each country
for _, row in df.iterrows():

    country = row["Country Name"]
    country_code = row["Country Code"]

    last_year = None
    last_value = None

    # Scan years from newest to oldest
    for year in reversed(year_columns):
        value = row[year]

        if pd.notna(value):
            last_year = int(year)
            last_value = int(float(value))
            break

    if last_year is not None:
        clean_rows.append({
            "country": country,
            "country_code": country_code,
            "year": last_year,
            "tourist_arrivals": last_value
        })

# Create cleaned dataframe
clean_df = pd.DataFrame(clean_rows)

# Remove aggregated regions (keep real countries)
clean_df = clean_df[clean_df["country_code"].str.len() == 3]

# Save dataset
clean_df.to_csv("datasets/clean_tourism.csv", index=False)

print("Tourism dataset cleaned successfully")
print("Rows:", len(clean_df))