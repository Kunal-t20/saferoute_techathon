import requests

OSRM_URL = "http://router.project-osrm.org/route/v1/driving/"


def get_route(start_coords: dict, end_coords: dict):
    """
    Get real road route between two coordinates using OSRM.
    Returns list of route points.
    """

    try:
        start = f"{start_coords['lng']},{start_coords['lat']}"
        end = f"{end_coords['lng']},{end_coords['lat']}"

        url = f"{OSRM_URL}{start};{end}?overview=full&geometries=geojson"

        response = requests.get(url)
        data = response.json()

        if "routes" not in data or len(data["routes"]) == 0:
            return []

        geometry = data["routes"][0]["geometry"]["coordinates"]

        # convert to lat/lng dict format
        route_points = [
            {"lat": coord[1], "lng": coord[0]}
            for coord in geometry
        ]

        return route_points

    except Exception as e:
        print("Routing error:", e)
        return []
