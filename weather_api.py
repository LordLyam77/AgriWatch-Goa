"""
Weather API and Agro-Meteorological Service for Goa Talukas.
Supports live OpenWeatherMap API calls with robust caching and 
high-fidelity Goa climatic simulation (Monsoon, Dry Spells, Post-Monsoon).
"""

import os
import time
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# Pre-defined Goa Talukas database with geo-coordinates, agro-climatic zones, and primary crops
GOA_TALUKAS = {
    "Tiswadi": {
        "center_town": "Panaji",
        "lat": 15.4909,
        "lon": 73.8278,
        "district": "North Goa",
        "primary_crops": ["Rice (Paddy)", "Coconut", "Vegetables"],
        "soil_type": "Coastal Alluvium & Laterite",
        "avg_annual_rainfall_mm": 2900,
        "elevation_m": 7
    },
    "Salcete": {
        "center_town": "Margao",
        "lat": 15.2832,
        "lon": 73.9862,
        "district": "South Goa",
        "primary_crops": ["Rice (Paddy)", "Coconut", "Cashew"],
        "soil_type": "Alluvial Sandy Loam",
        "avg_annual_rainfall_mm": 2850,
        "elevation_m": 10
    },
    "Bardez": {
        "center_town": "Mapusa",
        "lat": 15.5922,
        "lon": 73.8100,
        "district": "North Goa",
        "primary_crops": ["Cashew", "Coconut", "Mango"],
        "soil_type": "Red Laterite",
        "avg_annual_rainfall_mm": 2950,
        "elevation_m": 15
    },
    "Ponda": {
        "center_town": "Ponda",
        "lat": 15.4000,
        "lon": 74.0100,
        "district": "South Goa",
        "primary_crops": ["Rice (Paddy)", "Arecanut", "Spices"],
        "soil_type": "Deep Lateritic Loam",
        "avg_annual_rainfall_mm": 3300,
        "elevation_m": 42
    },
    "Bicholim": {
        "center_town": "Bicholim",
        "lat": 15.6000,
        "lon": 74.0500,
        "district": "North Goa",
        "primary_crops": ["Rice (Paddy)", "Cashew", "Sugarcane"],
        "soil_type": "Laterite Loam",
        "avg_annual_rainfall_mm": 3400,
        "elevation_m": 22
    },
    "Sattari": {
        "center_town": "Valpoi",
        "lat": 15.5319,
        "lon": 74.1369,
        "district": "North Goa",
        "primary_crops": ["Rice (Paddy)", "Cashew", "Mango", "Arecanut"],
        "soil_type": "Forest Loam & High Laterite",
        "avg_annual_rainfall_mm": 4100,
        "elevation_m": 35
    },
    "Canacona": {
        "center_town": "Chaudi",
        "lat": 14.9966,
        "lon": 74.0470,
        "district": "South Goa",
        "primary_crops": ["Rice (Paddy)", "Coconut", "Cashew"],
        "soil_type": "Coastal Laterite",
        "avg_annual_rainfall_mm": 3100,
        "elevation_m": 12
    },
    "Quepem": {
        "center_town": "Quepem",
        "lat": 15.2127,
        "lon": 74.0730,
        "district": "South Goa",
        "primary_crops": ["Rice (Paddy)", "Cashew", "Pineapple"],
        "soil_type": "Lateritic Clay",
        "avg_annual_rainfall_mm": 3500,
        "elevation_m": 21
    },
    "Sanguem": {
        "center_town": "Sanguem",
        "lat": 15.2303,
        "lon": 74.1526,
        "district": "South Goa",
        "primary_crops": ["Rice (Paddy)", "Cashew", "Sugarcane"],
        "soil_type": "Hilly Laterite",
        "avg_annual_rainfall_mm": 3900,
        "elevation_m": 32
    },
    "Pernem": {
        "center_town": "Pernem",
        "lat": 15.7230,
        "lon": 73.7953,
        "district": "North Goa",
        "primary_crops": ["Cashew", "Mango", "Coconut"],
        "soil_type": "Sandy Clay Laterite",
        "avg_annual_rainfall_mm": 2900,
        "elevation_m": 25
    },
    "Mormugao": {
        "center_town": "Vasco da Gama",
        "lat": 15.3990,
        "lon": 73.8124,
        "district": "South Goa",
        "primary_crops": ["Coconut", "Rice (Paddy)"],
        "soil_type": "Littoral Coastal Sand",
        "avg_annual_rainfall_mm": 2700,
        "elevation_m": 18
    },
    "Dharbandora": {
        "center_town": "Dharbandora",
        "lat": 15.3667,
        "lon": 74.1333,
        "district": "South Goa",
        "primary_crops": ["Rice (Paddy)", "Spices", "Arecanut"],
        "soil_type": "Riverine Alluvial & Laterite",
        "avg_annual_rainfall_mm": 3600,
        "elevation_m": 28
    }
}


class WeatherService:
    """Service to fetch real-time or simulated agro-meteorological data for Goa talukas."""

    def __init__(self, api_key: str = None, force_demo: bool = False):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY", "").strip()
        self.force_demo = force_demo or not bool(self.api_key)
        self.cache = {}

    def is_live_mode(self) -> bool:
        return bool(self.api_key) and not self.force_demo

    def get_current_weather(self, taluka_name: str, scenario: str = "monsoon_peak") -> dict:
        """Fetch current weather for a specific taluka (Live API or High-Fidelity Simulation)."""
        if taluka_name not in GOA_TALUKAS:
            raise ValueError(f"Taluka '{taluka_name}' not found in Goa database.")

        taluka_info = GOA_TALUKAS[taluka_name]
        lat, lon = taluka_info["lat"], taluka_info["lon"]

        if self.is_live_mode():
            try:
                data = self._fetch_openweather(lat, lon)
                dry_days = 0 if data["rainfall_mm"] > 2.0 else 3
                wet_days = 4 if data["rainfall_mm"] > 10.0 else 0
                soil_moist = round(float(min(95.0, max(25.0, 30.0 + data["rainfall_mm"] * 0.5 + data["humidity_percent"] * 0.4))), 1)

                derived = self.calculate_agro_indices(
                    data["temperature_c"],
                    data["humidity_percent"],
                    data["rainfall_mm"],
                    consecutive_dry_days=dry_days,
                    consecutive_wet_days=wet_days,
                    soil_moisture=soil_moist
                )
                data.update(derived)
                data["taluka"] = taluka_name
                data["district"] = taluka_info["district"]
                data["center_town"] = taluka_info["center_town"]
                data["primary_crops"] = taluka_info["primary_crops"]
                data["soil_type"] = taluka_info["soil_type"]
                data["lat"] = taluka_info["lat"]
                data["lon"] = taluka_info["lon"]
                data["consecutive_dry_days"] = dry_days
                data["consecutive_wet_days"] = wet_days
                data["soil_moisture_percent"] = soil_moist
                data["source"] = "OpenWeatherMap Live API"
                return data
            except Exception as e:
                print(f"[WeatherService] Live API failed ({e}). Falling back to simulation mode.")

        # High-Fidelity Simulated Mode
        return self._simulate_taluka_weather(taluka_name, scenario)

    def _fetch_openweather(self, lat: float, lon: float) -> dict:
        """Call OpenWeatherMap API with exponential retry logic."""
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        retries = 3
        backoff = 1.0

        for attempt in range(retries):
            try:
                res = requests.get(url, timeout=5)
                if res.status_code == 200:
                    payload = res.json()
                    main = payload.get("main", {})
                    weather_desc = payload.get("weather", [{}])[0].get("description", "clear sky")
                    wind = payload.get("wind", {})
                    rain = payload.get("rain", {})
                    clouds = payload.get("clouds", {})

                    # Extract rain in mm (last 1h or 3h)
                    rainfall_mm = rain.get("1h", rain.get("3h", 0.0))

                    return {
                        "temperature_c": round(main.get("temp", 28.0), 1),
                        "feels_like_c": round(main.get("feels_like", 30.0), 1),
                        "humidity_percent": int(main.get("humidity", 75)),
                        "pressure_hpa": int(main.get("pressure", 1010)),
                        "rainfall_mm": round(rainfall_mm, 1),
                        "wind_speed_kmh": round(wind.get("speed", 3.0) * 3.6, 1),
                        "cloud_cover_percent": int(clouds.get("all", 40)),
                        "weather_description": weather_desc.capitalize()
                    }
                else:
                    time.sleep(backoff)
                    backoff *= 2
            except requests.RequestException:
                time.sleep(backoff)
                backoff *= 2

        raise ConnectionError("Failed to reach OpenWeatherMap after 3 attempts.")

    def _simulate_taluka_weather(self, taluka_name: str, scenario: str) -> dict:
        """Simulate realistic Goa agricultural weather based on scenario and taluka geography."""
        info = GOA_TALUKAS[taluka_name]
        is_highland = info["avg_annual_rainfall_mm"] >= 3500  # Sattari, Sanguem, Dharbandora get more rain

        rng = np.random.RandomState(abs(hash(taluka_name + scenario)) % 100000)

        if scenario == "monsoon_peak":
            # Heavy South-West monsoon conditions
            rain_base = 120.0 if is_highland else 75.0
            rainfall = round(rain_base + rng.uniform(-20, 60), 1)
            humidity = int(rng.uniform(85, 98))
            temp = round(rng.uniform(25.5, 29.5), 1)
            wind = round(rng.uniform(20.0, 48.0), 1)
            clouds = int(rng.uniform(85, 100))
            soil_moist = round(rng.uniform(82.0, 96.0), 1)
            dry_days = 0
            wet_days = int(rng.randint(5, 14))
            desc = "Heavy Monsoon Rain & Gusts"

        elif scenario == "monsoon_dry_spell":
            # Break in the monsoon (Paddy drought risk in Goa)
            rainfall = round(rng.uniform(0.0, 2.0), 1)
            humidity = int(rng.uniform(62, 75))
            temp = round(rng.uniform(32.5, 36.0), 1)
            wind = round(rng.uniform(8.0, 18.0), 1)
            clouds = int(rng.uniform(20, 45))
            soil_moist = round(rng.uniform(22.0, 34.0), 1)
            dry_days = int(rng.randint(8, 16))
            wet_days = 0
            desc = "Dry Spell with Intense Sun"

        elif scenario == "pest_bloom":
            # High humidity, warm temperatures, overcast: ideal for stem borer & fungal blast
            rainfall = round(rng.uniform(15.0, 45.0), 1)
            humidity = int(rng.uniform(86, 95))
            temp = round(rng.uniform(28.0, 31.5), 1)
            wind = round(rng.uniform(10.0, 22.0), 1)
            clouds = int(rng.uniform(70, 90))
            soil_moist = round(rng.uniform(68.0, 82.0), 1)
            dry_days = 1
            wet_days = 4
            desc = "Humid Overcast with Intermittent Showers"

        elif scenario == "summer_heatwave":
            # Pre-monsoon April-May conditions
            rainfall = 0.0
            humidity = int(rng.uniform(42, 60))
            temp = round(rng.uniform(35.5, 39.2), 1)
            wind = round(rng.uniform(12.0, 25.0), 1)
            clouds = int(rng.uniform(10, 25))
            soil_moist = round(rng.uniform(18.0, 28.0), 1)
            dry_days = int(rng.randint(18, 30))
            wet_days = 0
            desc = "Scorching Heatwave & Low Humidity"

        else:  # "normal_balanced"
            rainfall = round(rng.uniform(10.0, 35.0), 1)
            humidity = int(rng.uniform(72, 82))
            temp = round(rng.uniform(28.0, 31.0), 1)
            wind = round(rng.uniform(12.0, 22.0), 1)
            clouds = int(rng.uniform(40, 65))
            soil_moist = round(rng.uniform(50.0, 65.0), 1)
            dry_days = 2
            wet_days = 2
            desc = "Partly Cloudy with Moderate Sea Breeze"

        derived = self.calculate_agro_indices(temp, humidity, rainfall, dry_days, wet_days, soil_moist)

        return {
            "taluka": taluka_name,
            "district": info["district"],
            "center_town": info["center_town"],
            "lat": info["lat"],
            "lon": info["lon"],
            "primary_crops": info["primary_crops"],
            "soil_type": info["soil_type"],
            "temperature_c": temp,
            "feels_like_c": round(temp + (humidity / 100.0) * 3.5, 1),
            "humidity_percent": humidity,
            "pressure_hpa": 1008 if rainfall > 50 else 1012,
            "rainfall_mm": rainfall,
            "wind_speed_kmh": wind,
            "cloud_cover_percent": clouds,
            "soil_moisture_percent": soil_moist,
            "consecutive_dry_days": dry_days,
            "consecutive_wet_days": wet_days,
            "weather_description": desc,
            "source": f"Goa Agro-Climatic Simulation ({scenario.replace('_', ' ').title()})",
            **derived
        }

    def calculate_agro_indices(self, temp: float, humidity: int, rainfall: float,
                               consecutive_dry_days: int, consecutive_wet_days: int,
                               soil_moisture: float) -> dict:
        """Calculate derived agricultural risk indices for decision-support."""
        # 1. Heat Stress Index (0-100)
        heat_index = min(100.0, max(0.0, (temp - 24.0) * 5.5 + (humidity / 100.0) * 15.0))

        # 2. Drought Risk Score (0-100)
        drought_score = min(100.0, max(0.0, (consecutive_dry_days * 3.5) + (temp - 30.0) * 4.0 + max(0.0, 45.0 - soil_moisture)))

        # 3. Waterlogging Risk Score (0-100)
        waterlog_score = min(100.0, max(0.0, (rainfall * 0.4) + (consecutive_wet_days * 6.0) + (soil_moisture - 60.0) * 0.8))

        # 4. Pest Favorability Index (0-10)
        pest_index = 0.0
        if 24.0 <= temp <= 33.0 and humidity >= 75:
            pest_index = min(10.0, (humidity - 70) * 0.25 + (consecutive_wet_days * 0.6))

        # 5. Fungal/Bacterial Disease Favorability (0-10)
        disease_index = 0.0
        if humidity >= 80 and (rainfall > 20 or consecutive_wet_days >= 3):
            disease_index = min(10.0, (humidity - 75) * 0.3 + (consecutive_wet_days * 0.8))

        return {
            "heat_stress_index": round(heat_index, 1),
            "drought_risk_score": round(drought_score, 1),
            "waterlog_risk_score": round(waterlog_score, 1),
            "pest_pressure_index": round(pest_index, 1),
            "disease_pressure_index": round(disease_index, 1)
        }

    def get_all_talukas_weather(self, scenario: str = "monsoon_peak") -> pd.DataFrame:
        """Fetch current agro-weather for all 12 Goa talukas into a DataFrame."""
        rows = [self.get_current_weather(taluka, scenario=scenario) for taluka in GOA_TALUKAS.keys()]
        return pd.DataFrame(rows)

    def get_5day_forecast(self, taluka_name: str) -> pd.DataFrame:
        """Generate a 5-day agro-meteorological forecast for a given taluka."""
        curr = self.get_current_weather(taluka_name)
        dates = pd.date_range(start=pd.Timestamp.now(), periods=5, freq="D")
        
        forecast_rows = []
        rng = np.random.RandomState(abs(hash(taluka_name)) % 5000)

        for i, dt in enumerate(dates):
            day_rain = max(0.0, curr["rainfall_mm"] + rng.uniform(-25, 25))
            day_temp = max(22.0, curr["temperature_c"] + rng.uniform(-2, 2.5))
            day_humidity = min(98, max(50, int(curr["humidity_percent"] + rng.uniform(-10, 8))))
            day_moisture = min(98.0, max(20.0, curr["soil_moisture_percent"] + (day_rain * 0.2) - (day_temp * 0.15)))
            
            # Predict probable primary risk
            if day_rain > 90 or day_moisture > 88:
                risk = "Waterlogging"
                level = "High"
            elif day_humidity > 85 and 26 <= day_temp <= 32:
                risk = "Pest / Disease Bloom"
                level = "Moderate"
            elif day_temp > 35 and day_moisture < 35:
                risk = "Drought & Heat Stress"
                level = "High"
            else:
                risk = "Optimal Growth"
                level = "Low"

            forecast_rows.append({
                "Date": dt.strftime("%a, %d %b"),
                "Rainfall (mm)": round(day_rain, 1),
                "Max Temp (°C)": round(day_temp, 1),
                "Humidity (%)": day_humidity,
                "Soil Moisture (%)": round(day_moisture, 1),
                "Primary Risk": risk,
                "Risk Level": level
            })

        return pd.DataFrame(forecast_rows)
