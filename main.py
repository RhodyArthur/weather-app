from dotenv import load_dotenv
import os
from weather import WeatherApp


def get_api_key() -> str:
    """
    Load API key from environment or prompt user.
    Raises ValueError if no key is provided.
    """
    load_dotenv()
    api_key = os.getenv("API_KEY")

    if not api_key:
        api_key = input("Enter your OpenWeatherMap API key: ").strip()

    if not api_key:
        raise ValueError("API key is required to run the application.")

    return api_key


def prompt_city() -> str:
    """
    Prompt user for a city name.
    Returns empty string if user wants to quit.
    """
    city = input("\nEnter city name (or 'quit' to exit): ").strip()
    return "" if city.lower() == "quit" else city


def main() -> None:
    """Main CLI application loop."""
    try:
        api_key = get_api_key()
        app = WeatherApp(api_key)
    except ValueError as e:
        print(f"Error: {e}")
        return

    print("🌤️  Weather CLI App Started")

    while True:
        city = prompt_city()

        if not city:
            print("Goodbye 👋")
            break

        try:
            weather = app.get_current_weather(city)
            if weather:
                app.display_weather(weather)
            else:
                print("⚠️  Could not retrieve weather data.")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
