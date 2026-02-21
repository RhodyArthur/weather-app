import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class WeatherApp:
    """
    Production-style Weather API client using OpenWeatherMap.
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str, token: str | None = None, timeout: int = 5):
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.timeout = timeout
        self.session = self._create_session(token)


    def _create_session(self, token: str | None) -> requests.Session:
        session = requests.Session()

        retry_strategy = Retry(
            total=5,
            backoff_factor=1.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        headers = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        session.headers.update(headers)
        return session

    def _request(self, endpoint: str, params: dict) -> dict | None:
        url = f"{self.BASE_URL}/{endpoint}"
        params["appid"] = self.api_key

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)

            if response.status_code == 404:
                print("Resource not found.")
                return None

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None


    def get_current_weather(self, city: str) -> dict | None:
        data = self._request("weather", {"q": city})
        if not data:
            return None

        return self._extract_current_weather(data)

    def get_weather_by_coordinates(self, lat: float, lon: float) -> dict | None:
        data = self._request("weather", {"lat": lat, "lon": lon})
        if not data:
            return None

        return self._extract_weather_summary(data)

    def get_forecast(self, city: str, count: int = 5) -> dict | None:
        return self._request("forecast", {"q": city, "cnt": count})

    @staticmethod
    def _extract_current_weather(data: dict) -> dict:
        return {
            "temperature": data.get("main", {}).get("temp"),
            "description": data.get("weather", [{}])[0].get("description"),
            "humidity": data.get("main", {}).get("humidity"),
            "wind": data.get("wind", {}).get("speed"),
        }

    @staticmethod
    def _extract_weather_summary(data: dict) -> dict:
        return {
            "id": data.get("weather", [{}])[0].get("id"),
            "main": data.get("weather", [{}])[0].get("main"),
            "description": data.get("weather", [{}])[0].get("description"),
            "icon": data.get("weather", [{}])[0].get("icon"),
        }

    @staticmethod
    def _get_emoji(description: str) -> str:
        desc = description.lower()

        if "clear" in desc:
            return "☀️"
        if "cloud" in desc:
            return "☁️"
        if "rain" in desc or "drizzle" in desc:
            return "🌧️"
        if "thunder" in desc:
            return "⛈️"
        if "snow" in desc:
            return "❄️"
        return ""

    def display_weather(self, weather_data: dict | list) -> None:
        if isinstance(weather_data, dict):
            self._display_single(weather_data)
        elif isinstance(weather_data, list):
            self._display_forecast(weather_data)
        else:
            raise ValueError("weather_data must be a dict or list of dicts")

    def _display_single(self, data: dict) -> None:
        desc = data.get("description") or data.get("main") or ""
        emoji = self._get_emoji(desc)

        print(f"Weather: {desc} {emoji}")

        if temp := data.get("temperature"):
            print(f"Temperature: {temp}°C")

        if humidity := data.get("humidity"):
            print(f"Humidity: {humidity}%")

        if wind := data.get("wind"):
            print(f"Wind Speed: {wind} m/s")

    def _display_forecast(self, forecast: list[dict]) -> None:
        for day in forecast:
            desc = day.get("description", "")
            emoji = self._get_emoji(desc)

            print(f"Date: {day.get('date', '')}")
            print(f"  Weather: {desc} {emoji}")

            if temp := day.get("avg_temp"):
                print(f"  Avg Temp: {temp:.1f}°C")

            if humidity := day.get("avg_humidity"):
                print(f"  Avg Humidity: {humidity:.0f}%")

            if wind := day.get("avg_wind"):
                print(f"  Avg Wind: {wind:.1f} m/s")

            print()
