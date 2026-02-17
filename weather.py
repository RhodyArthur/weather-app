import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

class WeatherApp:
    """
    Command-line weather application
    """
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self, api_key, token=None):
        self.api_key = api_key

        try:
            retry = Retry(total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504],)
            adapter = HTTPAdapter(max_retries=retry)

            self.session = requests.Session()
            self.session.mount('https://', adapter)
            self.headers = {"Content-Type":"application/json"}

            if token:
                self.headers['Authorization'] = f"Bearer {token}"
            self.session.headers.update(self.headers)
        except Exception as e:
            print(e)
            return None
    
    def get_current_weather(self, city):
        """
        Get current weather for a city
        Display: temperature, description, humidity, wind speed
        Handle city not found error
        """
        url = f"{self.BASE_URL}/weather"
        try:
            response = self.session.get(url, params={"q":city, "appid":self.api_key}, timeout=5)
            if response.status_code == 404:
                print("City not found")
                return None
            response.raise_for_status()
            data = response.json()
            weather_info = {
                "temperature": data.get("main", {}).get("temp"),
                "description": data.get("weather", [{}])[0].get("description"),
                "humidity": data.get("main", {}).get("humidity"),
                "wind": data.get("wind", {}).get("speed"),
            }
            return weather_info
        except requests.RequestException as e:
            print(f"Error fetching weather data by city: {e}")
            return None
    
    def get_forecast(self, city, days=5):
        """
        Get weather forecast
        Display forecast for next N days
        """
        forecast_url = f"{self.BASE_URL}/forecast"
        try:
            r = self.session.get(forecast_url, params={'q':city, 'cnt':days, 'appid':self.api_key}, timeout=5)
            if r.status_code == 404:
                print("Failed to forecast")
                return None
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            print(f"Error forecasting weather data for next N days: {e}")
            return None
    
    def get_weather_by_coordinates(self, lat, lon):
        """
        Get weather by latitude and longitude
        """
        url = f"{self.BASE_URL}/weather"
        try:
            response = self.session.get(url, params={"lat":lat, "lon":lon, "appid":self.api_key}, timeout=5)
            if response.status_code == 404:
                print("City not found")
                return None
            response.raise_for_status()
            data = response.json()
            weather_info = {
                "id": data.get("weather", [{}])[0].get("id"),
                "main": data.get("weather", [{}])[0].get("main"),
                "description": data.get("weather", [{}])[0].get("description"),
                "icon": data.get("weather", [{}])[0].get("icon"),
            }
            return weather_info
        except requests.RequestException as e:
            print(f"Error fetching weather data by latiitude and longitude: {e}")
            return None
    
    def display_weather(self, weather_data):
        """
        Format and display weather data nicely
        Include emoji for weather conditions (☀️ ☁️ 🌧️ ⛈️ ❄️)
        Accepts either a dict (single weather) or list (forecast summaries)
        """
        def get_emoji(description):
            desc = description.lower()
            if 'clear' in desc:
                return '☀️'
            elif 'cloud' in desc:
                return '☁️'
            elif 'rain' in desc or 'drizzle' in desc:
                return '🌧️'
            elif 'thunder' in desc:
                return '⛈️'
            elif 'snow' in desc:
                return '❄️'
            else:
                return ''

        if isinstance(weather_data, dict):
            temp = weather_data.get('temperature')
            desc = weather_data.get('description') or weather_data.get('main') or ''
            humidity = weather_data.get('humidity')
            wind = weather_data.get('wind')
            print("Weather:", desc, get_emoji(desc))
            if temp is not None:
                print(f"Temperature: {temp}°C")
            if humidity is not None:
                print(f"Humidity: {humidity}%")
            if wind is not None:
                print(f"Wind Speed: {wind} m/s")
            if 'description' in weather_data:
                print(f"Description: {weather_data['description']}")
        elif isinstance(weather_data, list):
            for day in weather_data:
                date = day.get('date', '')
                temp = day.get('avg_temp')
                desc = day.get('description', '')
                humidity = day.get('avg_humidity')
                wind = day.get('avg_wind')
                print(f"Date: {date}")
                print(f"  Weather: {desc} {get_emoji(desc)}")
                if temp is not None:
                    print(f"  Avg Temp: {temp:.1f}°C")
                if humidity is not None:
                    print(f"  Avg Humidity: {humidity:.0f}%")
                if wind is not None:
                    print(f"  Avg Wind: {wind:.1f} m/s")
                print()
        else:
            raise ValueError('weather_data must be a dict or a list of dicts')
            
        
