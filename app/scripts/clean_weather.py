import pandas as pd

df = pd.read_csv("datasets/weather.csv")

df = df[[
"country",
"location_name",
"condition_text"
]]

df.columns = [
"country",
"city",
"condition",
]

df = df.dropna()

df.to_csv("datasets/clean_weather.csv", index=False)

print("Weather dataset cleaned")