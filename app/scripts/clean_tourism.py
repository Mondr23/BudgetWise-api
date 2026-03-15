import pandas as pd

df = pd.read_csv("datasets/tourism.csv")

df = df[df["Indicator Name"] == "International tourism, number of arrivals"]

df = df.melt(
id_vars=["Country Name","Country Code"],
var_name="year",
value_name="tourist_arrivals"
)

df.columns = [
"country",
"country_code",
"year",
"tourist_arrivals"
]

df = df.dropna()

df.to_csv("datasets/clean_tourism.csv", index=False)

print("Tourism dataset cleaned")