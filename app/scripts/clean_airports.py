import pandas as pd

df = pd.read_csv("datasets/airports.csv")

df = df[[
"Name",
"City",
"Country",
"IATA",
"ICAO",
"Latitude",
"Longitude",
"Timezone"
]]

df.columns = [
"name",
"city",
"country",
"iata",
"icao",
"latitude",
"longitude",
"timezone"
]

df = df.dropna(subset=["city","country"])

df.to_csv("datasets/clean_airports.csv", index=False)

print("Airports dataset cleaned")