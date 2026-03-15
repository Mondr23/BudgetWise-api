-- COUNTRIES
CREATE TABLE countries (
    country_code TEXT PRIMARY KEY,
    country_name TEXT NOT NULL
);

-- CITIES
CREATE TABLE cities (
    city_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL,
    country_code TEXT,
    latitude REAL,
    longitude REAL,
    FOREIGN KEY(country_code) REFERENCES countries(country_code)
);

-- AIRPORTS
CREATE TABLE airports (
    airport_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    iata TEXT,
    icao TEXT,
    city_id INTEGER,
    latitude REAL,
    longitude REAL,
    timezone TEXT,
    FOREIGN KEY(city_id) REFERENCES cities(city_id)
);

-- WEATHER
CREATE TABLE weather (
    weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id INTEGER,
    temperature REAL,
    humidity REAL,
    wind_kph REAL,
    precipitation REAL,
    visibility REAL,
    air_quality_pm25 REAL,
    condition TEXT,
    last_updated TEXT,
    FOREIGN KEY(city_id) REFERENCES cities(city_id)
);

-- TOURISM STATISTICS
CREATE TABLE tourism_statistics (
    tourism_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code TEXT,
    year INTEGER,
    tourist_arrivals INTEGER,
    FOREIGN KEY(country_code) REFERENCES countries(country_code)
);

-- TRAVEL COSTS
CREATE TABLE travel_costs (
    cost_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id INTEGER,
    meal_price REAL,
    coffee_price REAL,
    beer_price REAL,
    transport_ticket REAL,
    taxi_km REAL,
    rent_city_center REAL,
    avg_salary REAL,
    daily_accommodation REAL,
    daily_cost_estimate REAL,
    FOREIGN KEY(city_id) REFERENCES cities(city_id)
);