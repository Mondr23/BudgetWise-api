import pandas as pd

df = pd.read_csv("datasets/weather.csv")

df = df[[
"country",
"location_name",
"latitude",
"longitude",
"temperature_celsius",
"humidity",
"wind_kph",
"precip_mm",
"visibility_km",
"air_quality_PM2.5",
"condition_text",
"last_updated"
]]

df.columns = [
"country",
"city",
"latitude",
"longitude",
"temperature",
"humidity",
"wind_kph",
"precipitation",
"visibility",
"air_quality_pm25",
"condition",
"last_updated"
]

df = df.dropna()

df.to_csv("datasets/clean_weather.csv", index=False)

print("Weather dataset cleaned")