import requests
import pandas as pd
from datetime import datetime
import os
import time
import subprocess

# API Keys and Base URLs
OPENWEATHER_API_KEY = "c876ee350c049e89f18623aa44a229c3"
AIRQUALITY_API_KEY = "51065cca-f862-4633-bd73-c06e08cf1fe9"
NOAA_TOKEN = "DKSShogFUvkZnAZYbdPhzConFYEXjRdx"

OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"
AIRQUALITY_BASE_URL = "http://api.airvisual.com/v2/city"
NOAA_STATIONS_URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations"
NOAA_DATA_URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"

HEADERS = {"token": NOAA_TOKEN}

DATA_DIR = "data"  # Directory to save CSV files

# Helper function to save data to CSV
def save_to_csv(new_data, filename):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    filepath = os.path.join(DATA_DIR, filename)

    if os.path.exists(filepath):
        existing_data = pd.read_csv(filepath)
        new_df = pd.DataFrame(new_data)
        combined_data = pd.concat([existing_data, new_df], ignore_index=True).drop_duplicates()
    else:
        combined_data = pd.DataFrame(new_data)

    combined_data.to_csv(filepath, index=False)
    return filepath

# Fetch OpenWeatherMap Data
def fetch_openweather_data_forecast_only(city_id):
    params = {"id": city_id, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    response = requests.get(OPENWEATHER_BASE_URL, params=params)
    if response.status_code == 200:
        weather_info = [
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "temperature": entry["main"]["temp"],
                "humidity": entry["main"]["humidity"],
                "weather": entry["weather"][0]["description"]
            }
            for entry in response.json()["list"]
        ]
        filepath = save_to_csv(weather_info, "forecast_data.csv")
        print("Forecast data saved to:", filepath)
        return filepath
    else:
        print("Error fetching OpenWeatherMap data:", response.text)
        return None

# Fetch OpenWeatherMap Data (including pollution metrics)
def fetch_openweather_data(city_id, lat, lon):
    # Fetch pollution data
    pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    pollution_response = requests.get(pollution_url)

    if pollution_response.status_code == 200:
        pollution_data = pollution_response.json()
        if "list" in pollution_data and len(pollution_data["list"]) > 0:
            air_quality = pollution_data["list"][0]
            components = air_quality.get("components", {})
            pollution_metrics = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "co": components.get("co", "N/A"),
                "no2": components.get("no2", "N/A"),
                "o3": components.get("o3", "N/A"),
                "pm2_5": components.get("pm2_5", "N/A"),
                "pm10": components.get("pm10", "N/A"),
            }
            # Save pollution data to CSV
            filepath = save_to_csv([pollution_metrics], "pollution_data.csv")
            print("Pollution data saved to:", filepath)
            return filepath
        else:
            print("No pollution data found for the specified location.")
            return None
    else:
        print("Error fetching pollution data:", pollution_response.text)
        return None

def fetch_airquality_data(city, state, country):
    params = {"city": city, "state": state, "country": country, "key": AIRQUALITY_API_KEY}
    response = requests.get(AIRQUALITY_BASE_URL, params=params)
    if response.status_code == 200:
        pollution_data = [
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "aqi_us": response.json()["data"]["current"]["pollution"]["aqius"],
                "aqi_cn": response.json()["data"]["current"]["pollution"]["aqicn"],
                "main_pollutant_us": response.json()["data"]["current"]["pollution"]["mainus"],
                "main_pollutant_cn": response.json()["data"]["current"]["pollution"]["maincn"]
            }
        ]
        filepath = save_to_csv(pollution_data, "air_quality_data.csv")
        print("Air Quality data saved to:", filepath)
        return filepath
    else:
        print("Error fetching Air Quality data:", response.text)
        return None

# Fetch NOAA Data
def fetch_noaa_data():
    params = {"locationid": "FIPS:PK", "datasetid": "GHCND", "limit": 1000}
    response = requests.get(NOAA_STATIONS_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        stations = response.json().get("results", [])
        if stations:
            station_id = stations[0]["id"]  # Use the first station
            weather_params = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "datasetid": "GHCND",
                "stationid": station_id,
                "startdate": "2023-01-01",
                "enddate": "2023-12-31",
                "units": "metric",
                "limit": 1000
            }
            weather_response = requests.get(NOAA_DATA_URL, headers=HEADERS, params=weather_params)
            if weather_response.status_code == 200:
                weather_data = weather_response.json().get("results", [])
                filepath = save_to_csv(weather_data, "noaa_weather_data.csv")
                print("NOAA data saved to:", filepath)
                return filepath
            else:
                print("Error fetching NOAA weather data:", weather_response.text)
        else:
            print("No stations found for Pakistan")
    else:
        print("Error fetching NOAA stations:", response.text)
    return None

# DVC Integration
def stage_data_with_dvc(filepath):
    subprocess.run(["dvc", "add", filepath])

def commit_with_git(message):
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", message])
    subprocess.run(["git", "push", "origin", "main"])

def push_to_dvc_remote():
    subprocess.run(["dvc", "push"])

# Main loop to fetch data every 5 minutes
while True:
    print("Starting data collection...")
    CITY_ID = "1162015"  # Islamabad
    LAT = 33.6844  # Latitude of Islamabad
    LON = 73.0479  # Longitude of Islamabad
    CITY = "Islamabad"
    STATE = "Islamabad"
    COUNTRY = "Pakistan"

    forecast_file = fetch_openweather_data(CITY_ID, LAT, LON)
    forecast_file_only = fetch_openweather_data_forecast_only(CITY_ID)
    air_quality_file = fetch_airquality_data(CITY, STATE, COUNTRY)
    noaa_file = fetch_noaa_data()

    if forecast_file:
        stage_data_with_dvc(forecast_file)
    if forecast_file_only:
        stage_data_with_dvc(forecast_file_only)
    if air_quality_file:
        stage_data_with_dvc(air_quality_file)
    if noaa_file:
        stage_data_with_dvc(noaa_file)

    commit_with_git("Update weather, air quality, and NOAA data")
    push_to_dvc_remote()
    print("Data collected, versioned, and pushed successfully.")

    # Wait for 5 minutes before fetching again
    time.sleep(300) #rightnow it is 30s
