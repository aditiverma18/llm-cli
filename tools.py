import requests
import time
def add(a,b):
    return a+b

def multiply(a,b):
    return a*b

def get_current_time():
    local_time=time.localtime()
    formatted_time=time.strftime("%Y-%m-%d %H:%M:%S",local_time)
    return formatted_time


def get_location(city):
  params={
    "name": city,
    "count": 1,
    "language": "en",
    "format": "json"
  }
  url="https://geocoding-api.open-meteo.com/v1/search"
  response=requests.get(url,params=params,timeout=5)
  response.raise_for_status()
  data=response.json()

  if not data.get("results"):
    return None

  location=data["results"][0]
  return location

def get_weather(latitude, longitude):
        weather_params={
          "latitude": latitude, 
          "longitude": longitude, 
          "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        }
        url_2="https://api.open-meteo.com/v1/forecast"
        response_2=requests.get(url_2,params=weather_params,timeout=5)
        response_2.raise_for_status()
        weather_data=response_2.json()
        
        return weather_data

def get_weather_tool(city):
    location=get_location(city)
    if location is None:
       return f"Sorry, I couldn't find a city named '{city}'."
    
    latitude=location["latitude"]
    longitude=location["longitude"]

    weather_data=get_weather(latitude,longitude)
    current=weather_data["current"]
    current_units=weather_data["current_units"]

    weather_codes={
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm with slight or moderate rain",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
        }
    weather_code=current["weather_code"]
    weather_description=weather_codes.get(weather_code, "Unknown weather code")
    return f"""City: {location["name"]}  Temperature: {current['temperature_2m']} {current_units['temperature_2m']}
    Relative Humidity: {current['relative_humidity_2m']} {current_units['relative_humidity_2m']}
    Wind Speed: {current['wind_speed_10m']} {current_units['wind_speed_10m']}  code: Weather_description: {weather_description}"""

    
    
