import requests

BASE_URL = "https://nominatim.openstreetmap.org/search"


def geocode_address(address: str):
    try:
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "safe-route-ai-app"
        }

        response = requests.get(BASE_URL, params=params, headers=headers)
        data = response.json()

        if not data:
            return None

        return {
            "lat": float(data[0]["lat"]),
            "lng": float(data[0]["lon"])
        }

    except Exception as e:
        print("Geocode error:", e)
        return None
