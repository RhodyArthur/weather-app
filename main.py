from dotenv import load_dotenv
import os
from weather import WeatherApp

def main():
    """
    Main CLI loop
    Ask user for city name
    Display weather
    Ask if they want to check another city
    """
    load_dotenv()
    api_key = os.getenv("API_KEY") or input("Enter your OpenWeatherMap API key: ")
    app = WeatherApp(api_key)
    
    while True:
        city = input("\nEnter city name (or 'quit' to exit): ")
        if city.lower() == 'quit':
            break
        
        # Get and display weather
        # Handle errors gracefully
        
        pass

if __name__ == "__main__":
    main()