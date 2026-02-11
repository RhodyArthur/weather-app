import requests
import json

class WeatherApp:
    """
    Command-line weather application
    """
    BASE_URL = "http://api.openweathermap.org/data/2.5"
    
    def __init__(self, api_key, token=None):
        self.api_key = api_key
        self.session = requests.Session()
        self.headers = {"acontent-type":"application/json"}

        if token:
            self.headers['Authorization'] = f"Bearer {token}"
        self.session.headers.update(self.headers)
    
    def get_current_weather(self, city):
        """
        Get current weather for a city
        Display: temperature, description, humidity, wind speed
        Handle city not found error
        """
        pass
    
    def get_forecast(self, city, days=5):
        """
        Get weather forecast
        Display forecast for next N days
        """
        pass
    
    def get_weather_by_coordinates(self, lat, lon):
        """
        Get weather by latitude and longitude
        """
        pass
    
    def display_weather(self, weather_data):
        """
        Format and display weather data nicely
        Include emoji for weather conditions (☀️ ☁️ 🌧️ ⛈️ ❄️)
        """
        pass