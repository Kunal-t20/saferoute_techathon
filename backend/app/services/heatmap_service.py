import pandas as pd

DATA_PATH =r"F:\Projects\techathon\backend\app\models\clustered.csv"

def get_heatmap_data():

    df = pd.read_csv(DATA_PATH)

    # Standard column names
    df.columns = df.columns.str.lower()

    # Remove noise cluster (-1)
    df = df[df['cluster_id'] != -1]

    # Group by cluster
    grouped = df.groupby('cluster_id').agg({
        'latitude': 'mean',
        'longitude': 'mean',
        'risk_score': 'mean',
        'cluster_id': 'count'
    }).rename(columns={'cluster_id': 'intensity'}).reset_index()

    # Risk labeling
    def risk_label(score):
        if score > 70:
            return "high"
        elif score > 40:
            return "medium"
        return "low"

    grouped['risk'] = grouped['risk_score'].apply(risk_label)

    # Final API format
    heatmap_points = []
    for _, row in grouped.iterrows():
        heatmap_points.append({
            "lat": round(row['latitude'], 5),
            "lng": round(row['longitude'], 5),
            "intensity": int(row['intensity']),
            "risk": row['risk']
        })

    return heatmap_points
