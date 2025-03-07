import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from datetime import datetime



load_dotenv()
api_key= os.getenv("API_KEY")

def format_time(time_str):
    """Format the time string to a more readable format."""
    time_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
    date= time_obj.strftime('%d-%m-%Y')
    time= time_obj.strftime('%I:%M %p')
    return date, time

@dataclass
class WeatherData:
    name: str
    date: str
    temperature: float
    feels_like: float
    humidity: int
    windspeed: int
    weatherCode: str
    weatherDescription: str



weatherCodes={
      "0": "Unknown",
      "10000": "Clear, Sunny",
      "11000": "Mostly Clear",
      "11010": "Partly Cloudy",
      "11020": "Mostly Cloudy",
      "10010": "Cloudy",
      "11030": "Partly Cloudy and Mostly Clear",
      "21000": "Light Fog",
      "21010": "Mostly Clear and Light Fog",
      "21020": "Partly Cloudy and Light Fog",
      "21030": "Mostly Cloudy and Light Fog",
      "21060": "Mostly Clear and Fog",
      "21070": "Partly Cloudy and Fog",
      "21080": "Mostly Cloudy and Fog",
      "20000": "Fog",
      "42040": "Partly Cloudy and Drizzle",
      "42030": "Mostly Clear and Drizzle",
      "42050": "Mostly Cloudy and Drizzle",
      "40000": "Drizzle",
      "42000": "Light Rain",
      "42130": "Mostly Clear and Light Rain",
      "42140": "Partly Cloudy and Light Rain",
      "42150": "Mostly Cloudy and Light Rain",
      "42090": "Mostly Clear and Rain",
      "42080": "Partly Cloudy and Rain",
      "42100": "Mostly Cloudy and Rain",
      "40010": "Rain",
      "42110": "Mostly Clear and Heavy Rain",
      "42020": "Partly Cloudy and Heavy Rain",
      "42120": "Mostly Cloudy and Heavy Rain",
      "42010": "Heavy Rain",
      "51150": "Mostly Clear and Flurries",
      "51160": "Partly Cloudy and Flurries",
      "51170": "Mostly Cloudy and Flurries",
      "50010": "Flurries",
      "51000": "Light Snow",
      "51020": "Mostly Clear and Light Snow",
      "51030": "Partly Cloudy and Light Snow",
      "51040": "Mostly Cloudy and Light Snow",
      "51220": "Drizzle and Light Snow",
      "51050": "Mostly Clear and Snow",
      "51060": "Partly Cloudy and Snow",
      "51070": "Mostly Cloudy and Snow",
      "50000": "Snow",
      "51010": "Heavy Snow",
      "51190": "Mostly Clear and Heavy Snow",
      "51200": "Partly Cloudy and Heavy Snow",
      "51210": "Mostly Cloudy and Heavy Snow",
      "51100": "Drizzle and Snow",
      "51080": "Rain and Snow",
      "51140": "Snow and Freezing Rain",
      "51120": "Snow and Ice Pellets",
      "60000": "Freezing Drizzle",
      "60030": "Mostly Clear and Freezing drizzle",
      "60020": "Partly Cloudy and Freezing drizzle",
      "60040": "Mostly Cloudy and Freezing drizzle",
      "62040": "Drizzle and Freezing Drizzle",
      "62060": "Light Rain and Freezing Drizzle",
      "62050": "Mostly Clear and Light Freezing Rain",
      "62030": "Partly Cloudy and Light Freezing Rain",
      "62090": "Mostly Cloudy and Light Freezing Rain",
      "62000": "Light Freezing Rain",
      "62130": "Mostly Clear and Freezing Rain",
      "62140": "Partly Cloudy and Freezing Rain",
      "62150": "Mostly Cloudy and Freezing Rain",
      "60010": "Freezing Rain",
      "62120": "Drizzle and Freezing Rain",
      "62200": "Light Rain and Freezing Rain",
      "62220": "Rain and Freezing Rain",
      "62070": "Mostly Clear and Heavy Freezing Rain",
      "62020": "Partly Cloudy and Heavy Freezing Rain",
      "62080": "Mostly Cloudy and Heavy Freezing Rain",
      "62010": "Heavy Freezing Rain",
      "71100": "Mostly Clear and Light Ice Pellets",
      "71110": "Partly Cloudy and Light Ice Pellets",
      "71120": "Mostly Cloudy and Light Ice Pellets",
      "71020": "Light Ice Pellets",
      "71080": "Mostly Clear and Ice Pellets",
      "71070": "Partly Cloudy and Ice Pellets",
      "71090": "Mostly Cloudy and Ice Pellets",
      "70000": "Ice Pellets",
      "71050": "Drizzle and Ice Pellets",
      "71060": "Freezing Rain and Ice Pellets",
      "71150": "Light Rain and Ice Pellets",
      "71170": "Rain and Ice Pellets",
      "71030": "Freezing Rain and Heavy Ice Pellets",
      "71130": "Mostly Clear and Heavy Ice Pellets",
      "71140": "Partly Cloudy and Heavy Ice Pellets",
      "71160": "Mostly Cloudy and Heavy Ice Pellets",
      "71010": "Heavy Ice Pellets",
      "80010": "Mostly Clear and Thunderstorm",
      "80030": "Partly Cloudy and Thunderstorm",
      "80020": "Mostly Cloudy and Thunderstorm",
      "80000": "Thunderstorm",
      "10001": "Clear",
      "11001": "Mostly Clear",
      "11011": "Partly Cloudy",
      "11021": "Mostly Cloudy",
      "10011": "Cloudy",
      "11031": "Partly Cloudy and Mostly Clear",
      "21001": "Light Fog",
      "21011": "Mostly Clear and Light Fog",
      "21021": "Partly Cloudy and Light Fog",
      "21031": "Mostly Cloudy and Light Fog",
      "21061": "Mostly Clear and Fog",
      "21071": "Partly Cloudy and Fog",
      "21081": "Mostly Cloudy and Fog",
      "20001": "Fog",
      "42041": "Partly Cloudy and Drizzle",
      "42031": "Mostly Clear and Drizzle",
      "42051": "Mostly Cloudy and Drizzle",
      "40001": "Drizzle",
      "42001": "Light Rain",
      "42131": "Mostly Clear and Light Rain",
      "42141": "Partly Cloudy and Light Rain",
      "42151": "Mostly Cloudy and Light Rain",
      "42091": "Mostly Clear and Rain",
      "42081": "Partly Cloudy and Rain",
      "42101": "Mostly Cloudy and Rain",
      "40011": "Rain",
      "42111": "Mostly Clear and Heavy Rain",
      "42021": "Partly Cloudy and Heavy Rain",
      "42121": "Mostly Cloudy and Heavy Rain",
      "42011": "Heavy Rain",
      "51151": "Mostly Clear and Flurries",
      "51161": "Partly Cloudy and Flurries",
      "51171": "Mostly Cloudy and Flurries",
      "50011": "Flurries",
      "51001": "Light Snow",
      "51021": "Mostly Clear and Light Snow",
      "51031": "Partly Cloudy and Light Snow",
      "51041": "Mostly Cloudy and Light Snow",
      "51221": "Drizzle and Light Snow",
      "51051": "Mostly Clear and Snow",
      "51061": "Partly Cloudy and Snow",
      "51071": "Mostly Cloudy and Snow",
      "50001": "Snow",
      "51011": "Heavy Snow",
      "51191": "Mostly Clear and Heavy Snow",
      "51201": "Partly Cloudy and Heavy Snow",
      "51211": "Mostly Cloudy and Heavy Snow",
      "51101": "Drizzle and Snow",
      "51081": "Rain and Snow",
      "51141": "Snow and Freezing Rain",
      "51121": "Snow and Ice Pellets",
      "60001": "Freezing Drizzle",
      "60031": "Mostly Clear and Freezing drizzle",
      "60021": "Partly Cloudy and Freezing drizzle",
      "60041": "Mostly Cloudy and Freezing drizzle",
      "62041": "Drizzle and Freezing Drizzle",
      "62061": "Light Rain and Freezing Drizzle",
      "62051": "Mostly Clear and Light Freezing Rain",
      "62031": "Partly cloudy and Light Freezing Rain",
      "62091": "Mostly Cloudy and Light Freezing Rain",
      "62001": "Light Freezing Rain",
      "62131": "Mostly Clear and Freezing Rain",
      "62141": "Partly Cloudy and Freezing Rain",
      "62151": "Mostly Cloudy and Freezing Rain",
      "60011": "Freezing Rain",
      "62121": "Drizzle and Freezing Rain",
      "62201": "Light Rain and Freezing Rain",
      "62221": "Rain and Freezing Rain",
      "62071": "Mostly Clear and Heavy Freezing Rain",
      "62021": "Partly Cloudy and Heavy Freezing Rain",
      "62081": "Mostly Cloudy and Heavy Freezing Rain",
      "62011": "Heavy Freezing Rain",
      "71101": "Mostly Clear and Light Ice Pellets",
      "71111": "Partly Cloudy and Light Ice Pellets",
      "71121": "Mostly Cloudy and Light Ice Pellets",
      "71021": "Light Ice Pellets",
      "71081": "Mostly Clear and Ice Pellets",
      "71071": "Partly Cloudy and Ice Pellets",
      "71091": "Mostly Cloudy and Ice Pellets",
      "70001": "Ice Pellets",
      "71051": "Drizzle and Ice Pellets",
      "71061": "Freezing Rain and Ice Pellets",
      "71151": "Light Rain and Ice Pellets",
      "71171": "Rain and Ice Pellets",
      "71031": "Freezing Rain and Heavy Ice Pellets",
      "71131": "Mostly Clear and Heavy Ice Pellets",
      "71141": "Partly Cloudy and Heavy Ice Pellets",
      "71161": "Mostly Cloudy and Heavy Ice Pellets",
      "71011": "Heavy Ice Pellets",
      "80011": "Mostly Clear and Thunderstorm",
      "80031": "Partly Cloudy and Thunderstorm",
      "80021": "Mostly Cloudy and Thunderstorm",
      "80001": "Thunderstorm"
    }

def get_weather(location, api_key):
    try:

        response= requests.get(f'https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={api_key}')
        response.raise_for_status()
        resp= response.json()
        # base_weather_code = str(resp.get('data').get('values').get('weatherCode'))
        # weather_code = f"{base_weather_code}{a}"

        # # Check if specific day/night code exists, otherwise fallback to base code
        # if weather_code not in weatherCodes:
        #     weather_code = base_weather_code


        # time_comparison for night and day
        time_= format_time(resp.get('data').get('time'))
        time_start = datetime.strptime("12:30 AM", "%I:%M %p").time()
        time_end = datetime.strptime("12:30 PM", "%I:%M %p").time()
        time_str = datetime.strptime(time_[1], '%I:%M %p').time()
        a= 0
        if time_str > time_start and time_str < time_end:
            a= 0
        else:
            a= 1

        weatherCode= (str(resp.get('data').get('values').get('weatherCode'))+str(a))       
        weatherDescription= weatherCodes.get(weatherCode, "unknown")
        data= WeatherData(
            name= resp.get('location').get('name'),
            date= time_[0],
            temperature= resp.get('data').get('values').get('temperature'),
            feels_like= resp.get('data').get('values').get('temperatureApparent'),
            humidity= resp.get('data').get('values').get('humidity'),  
            weatherCode= weatherCode,      
            windspeed= resp.get('data').get('values').get('windSpeed'),
            weatherDescription= weatherDescription         
        )
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except KeyError as e:
        print(f"Missing key in the response data: {e}")
        return None