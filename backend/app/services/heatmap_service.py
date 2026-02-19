import pandas as pd

DATA_PATH = r"F:\Projects\techathon\backend\app\models\clustered.csv"


def get_heatmap_data():

    df = pd.read_csv(DATA_PATH)

    # Standard column names
    df.columns = df.columns.str.lower()

    # Remove noise
    df = df[df["cluster_id"] != -1]

    # ---------- CLUSTER AGGREGATION ----------
    grouped = df.groupby("cluster_id").agg({
        "latitude": "mean",
        "longitude": "mean",
        "cluster_id": "count"
    }).rename(columns={"cluster_id": "intensity"}).reset_index()

    # risk label
    def risk_label(intensity):
        if intensity > 70:
            return "high"
        elif intensity > 40:
            return "medium"
        return "low"

    grouped["risk"] = grouped["intensity"].apply(risk_label)

    heatmap_points = []

    # ---------- CLUSTER POINTS ----------
    for _, row in grouped.iterrows():
        heatmap_points.append({
            "lat": round(row["latitude"], 5),
            "lng": round(row["longitude"], 5),
            "intensity": int(row["intensity"]),
            "risk": row["risk"],
            "type": "cluster"
        })

    # ---------- SAMPLE ACCIDENT DOTS ----------
    sample_df = df.sample(min(500, len(df)))  # prevent overload

    for _, row in sample_df.iterrows():
        heatmap_points.append({
            "lat": round(row["latitude"], 5),
            "lng": round(row["longitude"], 5),
            "intensity": 1,
            "risk": "low",
            "type": "accident"
        })

    return heatmap_points
