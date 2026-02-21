# weather app

# WeatherApp

A command-line weather application in Python that fetches and displays current weather and forecasts using the OpenWeatherMap API.

## Features

- Get current weather by city name
- Get weather by latitude and longitude
- Get multi-day weather forecast for a city
- Nicely formatted output with weather condition emojis (☀️ ☁️ 🌧️ ⛈️ ❄️)
- Robust error handling and retry logic

## Requirements

- Python 3.7+
- `requests` library
- OpenWeatherMap API key

## Installation

1. Clone this repository:
   ```sh
   git clone <repo-url>
   cd weather-app
   ```
2. Install dependencies:
   ```sh
   pip install requests
   ```

## Usage

1. Obtain a free API key from [OpenWeatherMap](https://openweathermap.org/api).
2. Update your code to provide the API key when initializing `WeatherApp`.

### Example

```python
from weather import WeatherApp

api_key = 'YOUR_API_KEY'
app = WeatherApp(api_key)

# Get current weather by city
weather = app.get_current_weather('London')
app.display_weather(weather)

# Get forecast
forecast = app.get_forecast('London', days=3)
app.display_weather(forecast)

# Get weather by coordinates
coords_weather = app.get_weather_by_coordinates(51.5074, -0.1278)
app.display_weather(coords_weather)
```

## Output Example

```
Weather: Clear ☀️
Temperature: 25°C
Humidity: 40%
Wind Speed: 3 m/s
Description: clear sky
```

## Notes

- Make sure your API key is kept secure and not shared publicly.
- The forecast feature uses the 5-day/3-hour forecast endpoint and summarizes by day.

## License

MIT License