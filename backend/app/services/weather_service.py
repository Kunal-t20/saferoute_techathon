import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(lat: float, lng: float) -> str:
    """
    Returns simple weather label:
    'clear', 'rain', 'fog', 'cloudy'
    """

    try:
        params = {
            "latitude": lat,
            "longitude": lng,
            "current_weather": True
        }

        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        if "current_weather" not in data:
            return "clear"

        weather_code = data["current_weather"]["weathercode"]

        return map_weather_code(weather_code)

    except Exception as e:
        print("Weather fetch error:", e)
        return "clear"


def map_weather_code(code: int) -> str:
    """
    Open-Meteo weather code mapping simplified
    """

    # Clear
    if code in [0]:
        return "clear"

    # Cloudy
    if code in [1, 2, 3]:
        return "cloudy"

    # Fog
    if code in [45, 48]:
        return "fog"

    # Rain / Drizzle / Thunder
    if code in [
        51, 53, 55,
        61, 63, 65,
        80, 81, 82,
        95, 96, 99
    ]:
        return "rain"

    return "clear"


def weather_risk_multiplier(weather: str) -> int:
    """
    Convert weather → risk bonus
    """

    mapping = {
        "clear": 0,
        "cloudy": 5,
        "fog": 15,
        "rain": 20
    }

    return mapping.get(weather, 0)
