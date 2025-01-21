import requests
import csv
from datetime import datetime

# Define API Key and endpoint
API_KEY = "CDX9ASBQJN5JZXYYU29WK3Q28"  # Updated API Key
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"  # Visual Crossing API endpoint

# Define function to fetch data for a specific date range
def fetch_weather_data(location, start_date, end_date):
    url = f"{BASE_URL}{location}/{start_date}/{end_date}"
    params = {
        "key": API_KEY,
        "unitGroup": "metric",  # Use metric units for Celsius
        "include": "days"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        try:
            results = []
            for day_data in data["days"]:
                # Reformat date to dd-mm-yyyy
                date = datetime.strptime(day_data["datetime"], "%Y-%m-%d").strftime("%d-%m-%Y")
                min_temp = day_data["tempmin"]
                max_temp = day_data["tempmax"]
                results.append((date, min_temp, max_temp))
            return results
        except (KeyError, IndexError):
            print(f"Error parsing data for range {start_date} to {end_date}")
            return []
    else:
        print(f"Failed to fetch data for range {start_date} to {end_date}: {response.status_code} - {response.text}")
        return []

# Main function to fetch data for the specified range and save to CSV
def save_weather_data_to_csv(location):
    start_date = "2020-01-01"  # Start date for the range
    end_date = "2022-08-25"    # End date for the range

    filename = f"historical_weather_data_{location.replace(',', '_').replace(' ', '_')}.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Min Temperature (C)", "Max Temperature (C)"])

        results = fetch_weather_data(location, start_date, end_date)
        for result in results:
            writer.writerow(result)

    print(f"Data saved to {filename}")

# Run the script
save_weather_data_to_csv("Dehradun,IN")
