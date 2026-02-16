import pandas as pd
from math import radians, cos, sin, asin, sqrt

from app.services.weather_service import get_weather, weather_risk_multiplier
from app.services.hazard_service import get_hazards
from app.services.explaination_service import generate_explanation

DATA_PATH = r"F:\Projects\techathon\backend\app\models\clustered.csv"


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c


def calculate_route_risk(route_points: list):

    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    df = df[df['cluster_id'] != -1]

    hotspots = df.groupby('cluster_id').agg({
        'latitude': 'mean',
        'longitude': 'mean',
        'cluster_id': 'count'
    }).rename(columns={'cluster_id': 'intensity'}).reset_index()

    risk_score = 0
    hotspot_hits = 0
    hazard_hits = 0

    # -------- WEATHER --------
    first = route_points[0]
    lat0 = first['lat']
    lng0 = first['lng']

    weather_label = get_weather(lat0, lng0)
    risk_score += weather_risk_multiplier(weather_label)

    # -------- HAZARDS --------
    hazards = get_hazards()

    for point in route_points:

        lat = point['lat']
        lng = point['lng']

        # HOTSPOTS
        for _, hotspot in hotspots.iterrows():
            dist = haversine(lat, lng, hotspot['latitude'], hotspot['longitude'])

            if dist < 2:
                risk_score += hotspot['intensity'] * 0.01
                hotspot_hits += 1

        # HAZARDS
        for hz in hazards:
            dist_hz = haversine(lat, lng, hz['lat'], hz['lng'])

            if dist_hz < 1:
                risk_score += 25
                hazard_hits += 1

    # -------- LEVEL --------
    if risk_score > 70:
        level = "high"
    elif risk_score > 40:
        level = "medium"
    else:
        level = "low"

    risk_percentage = min(int(risk_score), 100)

    # -------- EXPLANATION --------
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
