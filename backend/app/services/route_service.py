import pandas as pd
from math import radians, cos, sin, asin, sqrt

from app.services.weather_service import get_weather, weather_risk_multiplier
from app.services.hazard_service import get_hazards
from app.services.explaination_service import generate_explanation

DATA_PATH = r"F:\Projects\techathon\backend\app\models\clustered.csv"

# ==================================================
# GLOBAL HOTSPOT CACHE (LOAD ONCE)
# ==================================================
hotspots_cache = None


def load_hotspots():
    global hotspots_cache

    if hotspots_cache is None:
        df = pd.read_csv(DATA_PATH)
        df.columns = df.columns.str.strip().str.lower()
        df = df[df["cluster_id"] != -1]

        hotspots_cache = df.groupby("cluster_id").agg({
            "latitude": "mean",
            "longitude": "mean",
            "cluster_id": "count"
        }).rename(columns={"cluster_id": "intensity"}).reset_index()

    return hotspots_cache


# ==================================================
# DISTANCE FUNCTION
# ==================================================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + \
        cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))
    return R * c


# ==================================================
# ROUTE SAMPLING (PERFORMANCE BOOST)
# ==================================================
def sample_route(route_points, max_points=150):
    if len(route_points) <= max_points:
        return route_points

    step = len(route_points) // max_points
    return route_points[::step]


# ==================================================
# MAIN RISK ENGINE
# ==================================================
def calculate_route_risk(route_points: list):

    hotspots = load_hotspots()
    route_points = sample_route(route_points)

    risk_score = 0
    hotspot_hits = 0
    hazard_hits = 0

    hotspot_seen = set()
    hazard_seen = set()

    # ==================================================
    # WEATHER RISK
    # ==================================================
    first = route_points[0]
    weather_label = get_weather(first["lat"], first["lng"])
    risk_score += weather_risk_multiplier(weather_label)

    # ==================================================
    # LOAD HAZARDS
    # ==================================================
    hazards = get_hazards()

    # ==================================================
    # ROUTE ANALYSIS
    # ==================================================
    for point in route_points:

        lat = point["lat"]
        lng = point["lng"]

        # ---------- HOTSPOTS ----------
        for idx, hotspot in hotspots.iterrows():

            dist = haversine(
                lat,
                lng,
                hotspot["latitude"],
                hotspot["longitude"]
            )

            if dist < 2:  # within 2km

                if idx not in hotspot_seen:
                    risk_score += hotspot["intensity"] * 0.4
                    hotspot_hits += 1
                    hotspot_seen.add(idx)

        # ---------- HAZARDS ----------
        for i, hz in enumerate(hazards):

            dist_hz = haversine(
                lat,
                lng,
                hz["lat"],
                hz["lng"]
            )

            if dist_hz < 1:  # within 1km

                if i not in hazard_seen:
                    risk_score += 20
                    hazard_hits += 1
                    hazard_seen.add(i)

    # ==================================================
    # NORMALIZE
    # ==================================================
    risk_score = min(risk_score, 100)

    if risk_score > 70:
        level = "high"
    elif risk_score > 40:
        level = "medium"
    else:
        level = "low"

    risk_percentage = int(risk_score)

    explanation = generate_explanation(
        risk_percentage=risk_percentage,
        hotspot_hits=hotspot_hits,
        weather=weather_label,
        hazard_hits=hazard_hits
    )

    return {
        "risk_percentage": risk_percentage,
        "level": level,
        "hotspot_hits": hotspot_hits,
        "hazard_hits": hazard_hits,
        "weather": weather_label,
        "explanation": explanation
    }
