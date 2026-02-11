import pandas as pd
from math import radians, cos, sin, asin, sqrt

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

    # FIX 1
    df.columns = df.columns.str.strip().str.lower()

    df = df[df['cluster_id'] != -1]

    hotspots = df.groupby('cluster_id').agg({
        'latitude': 'mean',
        'longitude': 'mean',
        'cluster_id': 'count'
    }).rename(columns={'cluster_id': 'intensity'}).reset_index()

    risk_score = 0
    hotspot_hits = 0

    for point in route_points:

        # FIX 2 safe access
        lat = point.lat if hasattr(point, 'lat') else point['lat']
        lng = point.lng if hasattr(point, 'lng') else point['lng']

        for _, hotspot in hotspots.iterrows():
            dist = haversine(
                lat, lng,
                hotspot['latitude'], hotspot['longitude']
            )

            if dist < 2:
                risk_score += hotspot['intensity'] * 0.01
                hotspot_hits += 1

    if risk_score > 70:
        level = "high"
    elif risk_score > 40:
        level = "medium"
    else:
        level = "low"

    return {
        "risk_percentage": min(int(risk_score), 100),
        "level": level,
        "hotspot_hits": hotspot_hits
    }
