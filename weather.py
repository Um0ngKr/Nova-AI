import requests
from config import WEATHER_API_KEY, DEFAULT_CITY
from voice import speak
from utils import extract_city


def get_weather(command: str) -> bool:
    if not WEATHER_API_KEY:
        speak("Weather is not configured. Add your OpenWeatherMap API key to the dot env file.")
        return True

    city = extract_city(command) or DEFAULT_CITY

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": WEATHER_API_KEY,
                "units": "metric",
            },
            timeout=10,
        )

        if response.status_code == 401:
            print("[Weather error] 401: API key invalid or not activated.")
            speak("Your weather API key is invalid or not activated yet. Please check it.")
            return True

        if response.status_code == 404:
            print(f"[Weather error] 404: City not found: {city!r}")
            speak(f"I could not find the city {city}. Please try another city.")
            return True

        response.raise_for_status()
        data = response.json()

        temp = round(data["main"]["temp"])
        feels = round(data["main"]["feels_like"])
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        actual_city = data.get("name", city)

        print(f"[Weather] City: {actual_city}, temperature: {temp} C")

        speak(
            f"In {actual_city}, it is {temp} degrees Celsius with {description}. "
            f"It feels like {feels} degrees, and humidity is {humidity} percent."
        )

    except requests.HTTPError as exc:
        print(f"[Weather HTTP error] {exc}")
        speak("The weather service returned an error. Please check the terminal.")

    except requests.RequestException as exc:
        print(f"[Weather connection error] {exc}")
        speak("I could not connect to the weather service. Please check your internet.")

    except (KeyError, IndexError, ValueError) as exc:
        print(f"[Weather response error] {exc}")
        speak("The weather service returned unexpected information.")

    return True
